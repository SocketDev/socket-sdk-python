import socketdev
import json
from socketdev.core.classes import Package


class Sbom:
    @staticmethod
    def view(report_id: str) -> dict[str, dict]:
        path = f"sbom/view/{report_id}"
        response = socketdev.do_request(path=path)
        if response.status_code == 200:
            sbom = []
            sbom_dict = {}
            data = response.text
            data.strip('"')
            data.strip()
            for line in data.split("\n"):
                if line != '"' and line != "" and line is not None:
                    item = json.loads(line)
                    sbom.append(item)
            for val in sbom:
                sbom_dict[val['id']] = val
        else:
            sbom_dict = {}
        return sbom_dict

    @staticmethod
    def create_packages_dict(sbom: dict[str, dict]) -> dict[str, Package]:
        """
        Converts the SBOM Artifacts from the FulLScan into a Dictionary for parsing
        :param sbom: list - Raw artifacts for the SBOM
        :return:
        """
        packages = {}
        top_level_count = {}
        for package_id in sbom:
            item = sbom[package_id]
            package = Package(**item)
            if package.id in packages:
                print(f"Duplicate package_id: {package_id}")
            else:
                packages[package.id] = package
                for top_id in package.topLevelAncestors:
                    if top_id not in top_level_count:
                        top_level_count[top_id] = 1
                    else:
                        top_level_count[top_id] += 1
        if len(top_level_count) > 0:
            for package_id in top_level_count:
                packages[package_id].transitives = top_level_count[package_id]
        return packages
