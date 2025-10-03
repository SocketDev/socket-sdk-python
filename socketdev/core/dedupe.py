from collections import defaultdict
from typing import Dict, List, Any
from socketdev.log import log


class Dedupe:
    @staticmethod
    def normalize_file_path(path: str) -> str:
        return path.split("/", 1)[-1] if path and "/" in path else path or ""

    @staticmethod
    def alert_key(alert: dict) -> tuple:
        return (
            alert["type"],
            alert["severity"],
            alert.get("category"),
            Dedupe.normalize_file_path(alert.get("file")),
            alert.get("start"),
            alert.get("end")
        )

    @staticmethod
    def consolidate_and_merge_alerts(package_group: List[Dict[str, Any]]) -> Dict[str, Any]:
        def alert_identity(alert: dict) -> tuple:
            return (
                alert["type"],
                alert["severity"],
                alert.get("category"),
                Dedupe.normalize_file_path(alert.get("file")),
                alert.get("start"),
                alert.get("end")
            )

        alert_map: Dict[tuple, dict] = {}
        releases = set()
        for pkg in package_group:
            release = pkg.get("release") if pkg.get("release") is not None else pkg.get("type")
            releases.add(release)

            for alert in pkg.get("alerts", []):
                identity = alert_identity(alert)

                if identity not in alert_map:
                    # Build alert dict with only fields that exist in the original alert
                    consolidated_alert = {
                        "key": alert["key"],  # keep the first key seen
                        "type": alert["type"],
                        "severity": alert["severity"],
                        "releases": [release],
                        "props": alert.get("props", []),
                        "action": alert["action"]
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
                    if release not in alert_map[identity]["releases"]:
                        alert_map[identity]["releases"].append(release)

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