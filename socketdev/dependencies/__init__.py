import json
from urllib.parse import urlencode

from socketdev.tools import load_files


class Dependencies:
    def __init__(self, api):
        self.api = api

    def post(self, files: list, params: dict) -> dict:
        loaded_files = []
        loaded_files = load_files(files, loaded_files)
        path = "dependencies/upload?" + urlencode(params)
        response = self.api.do_request(path=path, files=loaded_files, method="POST")
        if response.status_code == 200:
            result = response.json()
        else:
            result = {}
            print(f"Error posting {files} to the Dependency API")
            print(response.text)
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
            print("Unable to retrieve Dependencies")
            print(response.text)
        return result
