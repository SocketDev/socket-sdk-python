import json
import logging
import urllib.parse

log = logging.getLogger("socketdev")


class LicenseMetadata:
    def __init__(self, api):
        self.api = api

    def post(self, licenses: list, params: dict = None) -> dict:
        path = f"license-metadata"
        if params:
            query_args = urllib.parse.urlencode(params)
            path += f"?{query_args}"
        payload = json.dumps(licenses)
        response = self.api.do_request(path=path, method="POST", payload=payload)

        if response.status_code == 200:
            result = response.json()
            return result

        error_message = response.json().get("error", {}).get("message", "Unknown error")
        log.error(f"Failed to create license metadata: {response.status_code}, message: {error_message}")
        return {}

