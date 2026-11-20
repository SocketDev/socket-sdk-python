from collections import defaultdict
from typing import Dict, List, Any
from socketdev.log import log

# Props that name the advisory behind a vulnerability alert. Every advisory of
# one severity on a package shares an alert type (``criticalCVE``, ``cve`` and
# so on), so these are what tell two of them apart.
ADVISORY_ID_PROPS = ("ghsaId", "ghsa_id", "cveId", "cve_id", "cve")

# Policy actions from least to most severe. Unknown or missing actions rank
# below "ignore" so any real action replaces them.
ACTION_RANK = {"ignore": 0, "monitor": 1, "warn": 2, "error": 3}


class Dedupe:
    @staticmethod
    def normalize_file_path(path: str) -> str:
        return path.split("/", 1)[-1] if path and "/" in path else path or ""

    @staticmethod
    def advisory_id(alert: dict) -> str:
        """The alert's GHSA or CVE identifier, upper-cased, or "" if it has none."""
        props = alert.get("props")
        if not isinstance(props, dict):
            return ""
        for prop_name in ADVISORY_ID_PROPS:
            value = props.get(prop_name)
            if isinstance(value, (list, tuple)):
                value = next((v for v in value if isinstance(v, str) and v.strip()), "")
            if isinstance(value, str) and value.strip():
                return value.strip().upper()
        return ""

    @staticmethod
    def action_rank(action: Any) -> int:
        return ACTION_RANK.get(action, -1) if isinstance(action, str) else -1

    @staticmethod
    def alert_key(alert: dict) -> tuple:
        return (
            alert.get("type"),
            alert.get("severity"),
            alert.get("category"),
            Dedupe.normalize_file_path(alert.get("file")),
            alert.get("start"),
            alert.get("end"),
            Dedupe.advisory_id(alert),
        )

    @staticmethod
    def consolidate_and_merge_alerts(package_group: List[Dict[str, Any]]) -> Dict[str, Any]:
        alert_map: Dict[tuple, dict] = {}
        releases = set()
        for pkg in package_group:
            release = pkg.get("release") if pkg.get("release") is not None else pkg.get("type")
            releases.add(release)

            for alert in pkg.get("alerts", []):
                identity = Dedupe.alert_key(alert)

                if identity not in alert_map:
                    # Build alert dict with only fields that exist in the original alert.
                    # Use .get() for key/type/severity/action so synthetic status rows
                    # (e.g. pendingScan/notFound), which are built server-side from a
                    # minimal {type, key} base, don't raise KeyError here.
                    consolidated_alert = {
                        "key": alert.get("key"),  # keep the first key seen
                        "type": alert.get("type"),
                        "severity": alert.get("severity"),
                        "releases": [release],
                        "props": alert.get("props", []),
                        "action": alert.get("action")
                    }
                    
                    # Only include optional fields if they exist in the original alert
                    if "category" in alert:
                        consolidated_alert["category"] = alert["category"]
                    if "file" in alert:
                        consolidated_alert["file"] = Dedupe.normalize_file_path(alert["file"])
                    if "start" in alert:
                        consolidated_alert["start"] = alert["start"]
                    if "end" in alert:
                        consolidated_alert["end"] = alert["end"]
                    
                    alert_map[identity] = consolidated_alert
                else:
                    merged = alert_map[identity]
                    if release not in merged["releases"]:
                        merged["releases"].append(release)
                    # Keep the most severe action seen for this alert, so a
                    # release that blocks is never hidden behind one that doesn't.
                    if Dedupe.action_rank(alert.get("action")) > Dedupe.action_rank(merged.get("action")):
                        merged["action"] = alert.get("action")

        base = package_group[0]
        base["releases"] = sorted(releases)
        base["alerts"] = list(alert_map.values())
        
        # Use inputPurl if available and complete, otherwise construct proper purl with namespace
        if "inputPurl" in base and "@" in base["inputPurl"]:
            # inputPurl has version, use it as-is
            base["purl"] = base["inputPurl"]
        else:
            # Construct purl properly with namespace and version
            purl_type = base.get('type', 'unknown')
            namespace = base.get('namespace')
            name = base.get('name', 'unknown')
            version = base.get('version', '0.0.0')
            
            # Start with inputPurl if available (without version) or construct from scratch
            if "inputPurl" in base and not "@" in base["inputPurl"]:
                # inputPurl exists but lacks version, append it
                base["purl"] = f"{base['inputPurl']}@{version}"
            else:
                # Construct complete purl from components
                if namespace:
                    base["purl"] = f"pkg:{purl_type}/{namespace}/{name}@{version}"
                else:
                    base["purl"] = f"pkg:{purl_type}/{name}@{version}"
        
        return base

    @staticmethod
    def dedupe(packages: List[Dict[str, Any]], batched: bool = True) -> List[Dict[str, Any]]:
        # Always group by inputPurl now, but keep the batched parameter for backward compatibility
        grouped = Dedupe.consolidate_by_input_purl(packages)
        results = []
        for group in grouped.values():
            result = Dedupe.consolidate_and_merge_alerts(group)
            # Remove batchIndex from the result
            if "batchIndex" in result:
                del result["batchIndex"]
            results.append(result)
        return results

    @staticmethod
    def consolidate_by_input_purl(packages: List[Dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
        """Group packages by their inputPurl field"""
        grouped: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
        
        # Handle both list of packages and nested structure
        if packages and isinstance(packages[0], list):
            # If we get a nested list, flatten it
            flat_packages = []
            for sublist in packages:
                if isinstance(sublist, list):
                    flat_packages.extend(sublist)
                else:
                    flat_packages.append(sublist)
            packages = flat_packages
        
        for pkg in packages:
            # inputPurl should always exist now, fallback to purl if not found
            group_key = pkg.get("inputPurl", pkg.get("purl", str(hash(str(pkg)))))
            grouped[group_key].append(pkg)
        return grouped