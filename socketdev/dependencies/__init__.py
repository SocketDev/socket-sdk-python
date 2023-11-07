import socketdev
from socketdev.tools import load_files
from urllib.parse import urlencode
import json


class Dependencies:
    @staticmethod
    def post(files: list, params: dict) -> dict:
        loaded_files = []
        loaded_files = load_files(files, loaded_files)
        path = "dependencies/upload?" + urlencode(params)
        response = socketdev.do_request(
            path=path,
            files=loaded_files,
            method="POST"
        )
        if response.status_code == 200:
            result = response.json()
        else:
            result = {}
            print(f"Error posting {files} to the Dependency API")
            print(response.text)
        return result

    @staticmethod
    def get(
            limit: int = 50,
            offset: int = 0,
    ) -> dict:
        path = "dependencies/search"
        payload = {
            "limit":  limit,
            "offset": offset
        }
        payload_str = json.dumps(payload)
        response = socketdev.do_request(
            path=path,
            method="POST",
            payload=payload_str
        )
        if response.status_code == 200:
            result = response.json()
        else:
            result = {}
            print("Unable to retrieve Dependencies")
            print(response.text)
        return result
