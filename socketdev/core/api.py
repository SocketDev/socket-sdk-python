import base64
import requests
from socketdev.core.classes import Response
from socketdev.exceptions import APIKeyMissing, APIFailure, APIAccessDenied, APIInsufficientQuota, APIResourceNotFound
from socketdev.version import __version__


class API:
    def __init__(self):
        self.encoded_key = None
        self.api_url = "https://api.socket.dev/v0"
        self.request_timeout = 30

    def encode_key(self, token: str):
        self.encoded_key = base64.b64encode(token.encode()).decode("ascii")

    def set_timeout(self, timeout: int):
        self.request_timeout = timeout

    def do_request(
        self, path: str, headers: dict | None = None, payload: [dict, str] = None, files: list = None, method: str = "GET"
    ) -> Response:
        if self.encoded_key is None or self.encoded_key == "":
            raise APIKeyMissing

        if headers is None:
            headers = {
                "Authorization": f"Basic {self.encoded_key}",
                "User-Agent": f"SocketPythonScript/{__version__}",
                "accept": "application/json",
            }
        url = f"{self.api_url}/{path}"
        try:
            response = requests.request(
                method.upper(), url, headers=headers, data=payload, files=files, timeout=self.request_timeout
            )
            
            if response.status_code == 401:
                raise APIAccessDenied("Unauthorized")
            if response.status_code == 403:
                raise APIInsufficientQuota("Insufficient max_quota for API method")
            if response.status_code == 404:
                raise APIResourceNotFound(f"Path not found {path}")
            if response.status_code == 429:
                raise APIInsufficientQuota("Insufficient quota for API route")
            if response.status_code >= 400:
                raise APIFailure("Bad Request")
            
            return response
            
        except Exception as error:
            response = Response(text=f"{error}", error=True, status_code=500)
            raise APIFailure(response)
