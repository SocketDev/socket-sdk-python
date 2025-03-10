import json
from urllib.parse import urlencode
import logging
from socketdev.tools import load_files
from socketdev.exceptions import APIFailure

log = logging.getLogger("socketdev")

# TODO: Add types for responses. Not currently used in the CLI.


class Dependencies:
    def __init__(self, api):
        self.api = api

    def post(self, files: list, params: dict) -> dict:
        loaded_files = load_files(files, [])
        path = "dependencies/upload?" + urlencode(params)
        try:
            response = self.api.do_request(path=path, files=loaded_files, method="POST")
            if response.status_code == 200:
                return response.json()
        except APIFailure as e:
            log.error(f"Socket SDK: API failure while posting dependencies {e}")
            raise
        except Exception as e:
            log.error(f"Socket SDK: Unexpected error while posting dependencies {e}")
            raise

        return {}

    def get(
        self,
        limit: int = 50,
        offset: int = 0,
    ) -> dict:
        path = "dependencies/search"
        payload = {"limit": limit, "offset": offset}
        payload_str = json.dumps(payload)
        try:
            response = self.api.do_request(path=path, method="POST", payload=payload_str)
            if response.status_code == 200:
                return response.json()
        except APIFailure as e:
            log.error(f"Socket SDK: API failure while retrieving dependencies {e}")
            raise
        except Exception as e:
            log.error(f"Socket SDK: Unexpected error while retrieving dependencies {e}")
            raise

        return {}
