import logging

log = logging.getLogger("socketdev")

# TODO: Add response type classes for Quota endpoints


class Quota:
    def __init__(self, api):
        self.api = api

    def get(self) -> dict:
        path = "quota"
        response = self.api.do_request(path=path)
        if response.status_code == 200:
            return response.json()
        log.error(f"Error getting quota: {response.status_code}")
        log.error(response.text)
        return {}
