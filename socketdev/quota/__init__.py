import logging
from socketdev.exceptions import APIFailure

log = logging.getLogger("socketdev")

# TODO: Add response type classes for Quota endpoints


class Quota:
    def __init__(self, api):
        self.api = api

    def get(self) -> dict:
        path = "quota"
        try:
            response = self.api.do_request(path=path)
            if response.status_code == 200:
                return response.json()
        except APIFailure as e:
            log.error(f"Socket SDK: API failure while getting quota {e}")
            raise
        except Exception as e:
            log.error(f"Socket SDK: Unexpected error while getting quota {e}")
            raise

        return {}
