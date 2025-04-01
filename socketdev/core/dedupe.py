from collections import defaultdict
from typing import Dict, List, Any


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
                        "releases": [release]
                    }
                else:
                    if release not in alert_map[identity]["releases"]:
                        alert_map[identity]["releases"].append(release)

        base = package_group[0]
        return {
            "id": base.get("id"),
            "author": base.get("author"),
            "size": base.get("size"),
            "type": base.get("type"),
            "name": base.get("name"),
            "namespace": base.get("namespace"),
            "version": base.get("version"),
            "releases": sorted(releases),
            "alerts": list(alert_map.values()),
            "score": base.get("score", {}),
            "license": base.get("license"),
            "licenseDetails": base.get("licenseDetails", []),
            "batchIndex": base.get("batchIndex"),
            "purl": f"pkg:{base.get('type', 'unknown')}/{base.get('name', 'unknown')}@{base.get('version', '0.0.0')}"
        }

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
            print(error)
        return grouped