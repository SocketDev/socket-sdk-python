import json
from urllib.parse import urlencode
import logging
from socketdev.tools import load_files
from ..utils import Utils

log = logging.getLogger("socketdev")

# TODO: Add types for responses. Not currently used in the CLI.


class Dependencies:
    def __init__(self, api):
        self.api = api

    def post(self, files: list, params: dict, use_lazy_loading: bool = False, workspace: str = None) -> dict:
        if use_lazy_loading:
            loaded_files = Utils.load_files_for_sending_lazy(files, workspace)
        else:
            loaded_files = []
            loaded_files = load_files(files, loaded_files)
        
        path = "dependencies/upload?" + urlencode(params)
        response = self.api.do_request(path=path, files=loaded_files, method="POST")
        if response.status_code == 200:
            result = response.json()
        else:
            result = {}
            log.error(f"Error posting {files} to the Dependency API")
            log.error(response.text)
        return result

    def get(
        self,
        limit: int = 50,
        offset: int = 0,
    ) -> dict:
        path = "dependencies/search"
        payload = {"limit": limit, "offset": offset}
        payload_str = json.dumps(payload)
        response = self.api.do_request(path=path, method="POST", payload=payload_str)
        if response.status_code == 200:
            result = response.json()
        else:
            result = {}
            log.error("Unable to retrieve Dependencies")
            log.error(response.text)
        return result
