import json
import logging
from typing import Any
from urllib.parse import urlencode


log = logging.getLogger("socketdev")

class Setting:
    def __init__(self, api):
        self.api = api

    def create_url(self, org_slug: str, label_id: int):
        return "orgs/" + org_slug + f"/repos/labels/{label_id}/label-setting"

    def get(self, org_slug: str, label_id: int, setting_key: str):
        url = self.create_url(org_slug, label_id)
        path = f"{url}?setting_key={setting_key}"
        response = self.api.do_request(path=path)
        if response.status_code == 201:
            return response.json()

        error_message = response.json().get("error", {}).get("message", "Unknown error")
        log.error(f"Error getting label setting {setting_key} for {label_id}: {response.status_code}, message: {error_message}")
        return {}

    def put(self, org_slug: str, label_id: int, settings: dict[str, dict[str, dict[str, str]]]):
        path = self.create_url(org_slug, label_id)
        response = self.api.do_request(method="PUT", path=path, payload=json.dumps(settings))

        if response.status_code == 201:
            return response.json()

        error_message = response.json().get("error", {}).get("message", "Unknown error")
        log.error(f"Error updating label settings for {label_id}: {response.status_code}, message: {error_message}")
        return {}

    def delete(self, org_slug: str, label_id: int, settings_key: str):
        path = self.create_url(org_slug, label_id)
        path += "?setting_key=" + settings_key
        response = self.api.do_request(path=path, method="DELETE")

        if response.status_code == 201:
            return response.json()

        error_message = response.json().get("error", {}).get("message", "Unknown error")
        log.error(f"Error updating label settings for {label_id}: {response.status_code}, message: {error_message}")
        return {}


class Labels:
    def __init__(self, api):
        self.api = api
        self.setting = Setting(api)

    def list(self, org_slug: str):
        path = f"orgs/" + org_slug + f"/repos/labels"
        response = self.api.do_request(path=path)
        if response.status_code == 200:
            return response.json()

        error_message = response.json().get("error", {}).get("message", "Unknown error")
        log.error(f"Error getting labels: {response.status_code}, message: {error_message}")
        return {}

    def post(self, org_slug: str, label_name: str) -> dict:
        path = f"orgs/{org_slug}/repos/labels"
        payload = json.dumps({"name": label_name})
        response = self.api.do_request(path=path, method="POST", payload=payload)

        if response.status_code == 201:
            result = response.json()
            return result

        error_message = response.json().get("error", {}).get("message", "Unknown error")
        log.error(f"Failed to create repository label: {response.status_code}, message: {error_message}")
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
