import logging
from socketdev.exceptions import APIFailure

log = logging.getLogger("socketdev")


class NPM:
    def __init__(self, api):
        self.api = api

    def issues(self, package: str, version: str) -> list:
        path = f"npm/{package}/{version}/issues"
        try:
            response = self.api.do_request(path=path)
            if response.status_code == 200:
                return response.json()
        except APIFailure as e:
            log.error(f"Socket SDK: API failure while getting npm issues {e}")
            raise
        except Exception as e:
            log.error(f"Socket SDK: Unexpected error while getting npm issues {e}")
            raise

        return []

    def score(self, package: str, version: str) -> list:
        path = f"npm/{package}/{version}/score"
        try:
            response = self.api.do_request(path=path)
            if response.status_code == 200:
                return response.json()
        except APIFailure as e:
            log.error(f"Socket SDK: API failure while getting npm score {e}")
            raise
        except Exception as e:
            log.error(f"Socket SDK: Unexpected error while getting npm score {e}")
            raise

        return {}
