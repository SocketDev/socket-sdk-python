import json
import logging


log = logging.getLogger("socketdev")


class LicenseMetadata:
    def __init__(self, api):
        self.api = api

    def post(self, licenses: list) -> dict:
        path = f"license-metadata"
        payload = json.dumps(licenses)
        response = self.api.do_request(path=path, method="POST", payload=payload)

        if response.status_code == 200:
            result = response.json()
            return result

        error_message = response.json().get("error", {}).get("message", "Unknown error")
        log.error(f"Failed to create license metadata: {response.status_code}, message: {error_message}")
        return {}

    def get(self, org_slug: str, label_id: str) -> dict:
        path = f"orgs/{org_slug}/repos/labels/{label_id}"
        response = self.api.do_request(path=path)
        if response.status_code == 200:
            result = response.json()
            return result

        error_message = response.json().get("error", {}).get("message", "Unknown error")
        log.error(f"Failed to get repository label: {response.status_code}, message: {error_message}")
        return {}

    def delete(self, org_slug: str, label_id: str) -> dict:
        path = f"orgs/{org_slug}/repos/labels/{label_id}"
        response = self.api.do_request(path=path, method="DELETE")
        if response.status_code == 200:
            return response.json()

        error_message = response.json().get("error", {}).get("message", "Unknown error")
        log.error(f"Error deleting repository label: {response.status_code}, message: {error_message}")
        return {}


    def associate(self, org_slug: str, label_id: int, repo_id: str) -> dict:
        path = f"orgs/{org_slug}/repos/labels/{label_id}/associate"
        payload = json.dumps({"repository_id": repo_id})
        response = self.api.do_request(path=path, method="POST", payload=payload)
        if response.status_code == 200:
            return response.json()

        error_message = response.json().get("error", {}).get("message", "Unknown error")
        log.error(f"Error associating repository label: {response.status_code}, message: {error_message}")
        return {}

    def disassociate(self, org_slug: str, label_id: int, repo_id: str) -> dict:
        path = f"orgs/{org_slug}/repos/labels/{label_id}/disassociate"
        payload = json.dumps({"repository_id": repo_id})
        response = self.api.do_request(path=path, method="POST", payload=payload)
        if response.status_code == 200:
            return response.json()

        error_message = response.json().get("error", {}).get("message", "Unknown error")
        log.error(f"Error associating repository label: {response.status_code}, message: {error_message}")
        return {}
