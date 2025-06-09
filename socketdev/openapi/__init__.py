import logging

log = logging.getLogger("socketdev")

# TODO: Add response type classes for OpenAPI endpoints


class OpenAPI:
    def __init__(self, api):
        self.api = api

    def get(self) -> dict:
        path = "openapi"
        response = self.api.do_request(path=path)
        if response.status_code == 200:
            return response.json()
        log.error(f"Error getting OpenAPI spec: {response.status_code}")
        log.error(response.text)
        return {}
