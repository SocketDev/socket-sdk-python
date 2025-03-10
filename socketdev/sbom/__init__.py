import json
from socketdev.core.classes import Package
import logging
from socketdev.exceptions import APIFailure

log = logging.getLogger("socketdev")


class Sbom:
    def __init__(self, api):
        self.api = api

    # NOTE: This method's NDJSON handling is inconsistent with other methods in the SDK.
    # While other methods return arrays for NDJSON responses, this returns a dictionary.
    # This inconsistency is preserved to maintain backward compatibility with clients
    # who have been using this method since its introduction 9 months ago.
    def view(self, report_id: str) -> dict[str, dict]:
        path = f"sbom/view/{report_id}"
        try:
            response = self.api.do_request(path=path)
            if response.status_code == 200:
                sbom = []
                sbom_dict = {}
                data = response.text.strip('"').strip()
                for line in data.split("\n"):
                    if line and line != '"':
                        item = json.loads(line)
                        sbom.append(item)
                for val in sbom:
                    sbom_dict[val["id"]] = val
                return sbom_dict
        except APIFailure as e:
            log.error(f"Socket SDK: API failure while viewing SBOM {e}")
            raise
        except Exception as e:
            log.error(f"Socket SDK: Unexpected error while viewing SBOM {e}")
            raise

        return {}

    def create_packages_dict(self, sbom: dict[str, dict]) -> dict[str, Package]:
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
