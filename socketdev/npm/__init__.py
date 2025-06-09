import logging

log = logging.getLogger("socketdev")

# TODO: Add response type classes for NPM endpoints


class NPM:
    def __init__(self, api):
        self.api = api

    def issues(self, package: str, version: str) -> list:
        path = f"npm/{package}/{version}/issues"
        response = self.api.do_request(path=path)
        if response.status_code == 200:
            return response.json()
        log.error(f"Error getting npm issues: {response.status_code}")
        log.error(response.text)
        return []

    def score(self, package: str, version: str) -> list:
        path = f"npm/{package}/{version}/score"
        response = self.api.do_request(path=path)
        if response.status_code == 200:
            return response.json()
        log.error(f"Error getting npm score: {response.status_code}")
        log.error(response.text)
        return []
