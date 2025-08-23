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
            alert["category"],
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
                alert["category"],
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
                file = Dedupe.normalize_file_path(alert.get("file"))

                if identity not in alert_map:
                    alert_map[identity] = {
                        "key": alert["key"],  # keep the first key seen
                        "type": alert["type"],
                        "severity": alert["severity"],
                        "category": alert["category"],
                        "file": file,
                        "start": alert.get("start"),
                        "end": alert.get("end"),
                        "releases": [release],
                        "props": alert.get("props", []),
                        "action": alert["action"]
                    }
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
        if batched:
            grouped = Dedupe.consolidate_by_batch_index(packages)
        else:
            grouped = Dedupe.consolidate_by_order(packages)
        return [Dedupe.consolidate_and_merge_alerts(group) for group in grouped.values()]

    @staticmethod
    def consolidate_by_batch_index(packages: List[Dict[str, Any]]) -> dict[int, list[dict[str, Any]]]:
        grouped: Dict[int, List[Dict[str, Any]]] = defaultdict(list)
        for pkg in packages:
            grouped[pkg["batchIndex"]].append(pkg)
        return grouped

    @staticmethod
    def consolidate_by_order(packages: List[Dict[str, Any]]) -> dict[int, list[dict[str, Any]]]:
        grouped: Dict[int, List[Dict[str, Any]]] = defaultdict(list)
        batch_index = 0
        package_purl = None
        try:
            for pkg in packages:
                name = pkg["name"]
                version = pkg["version"]
                namespace = pkg.get("namespace")
                ecosystem = pkg.get("type")
                new_purl = f"pkg:{ecosystem}/"
                if namespace:
                    new_purl += f"{namespace}/"
                new_purl += f"{name}@{version}"
                if package_purl is None:
                    package_purl = new_purl
                if package_purl != new_purl:
                    batch_index += 1
                pkg["batchIndex"] = batch_index
                grouped[pkg["batchIndex"]].append(pkg)
        except Exception as error:
            log.error(error)
        return grouped