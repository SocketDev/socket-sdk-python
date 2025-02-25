import base64
import requests
from socketdev.core.classes import Response
from socketdev.exceptions import (
    APIKeyMissing, APIFailure, APIAccessDenied, APIInsufficientQuota, 
    APIResourceNotFound, APITimeout, APIConnectionError, APIBadGateway,
    APIInsufficientPermissions, APIOrganizationNotAllowed
)
from socketdev.version import __version__
from requests.exceptions import Timeout, ConnectionError
import time


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
            start_time = time.time()
            response = requests.request(
                method.upper(), url, headers=headers, data=payload, files=files, timeout=self.request_timeout
            )
            request_duration = time.time() - start_time
            
            if response.status_code == 401:
                raise APIAccessDenied("Unauthorized")
            if response.status_code == 403:
                try:
                    error_message = response.json().get('error', {}).get('message', '')
                    if "Insufficient permissions for API method" in error_message:
                        raise APIInsufficientPermissions(error_message)
                    elif "Organization not allowed" in error_message:
                        raise APIOrganizationNotAllowed(error_message)
                    elif "Insufficient max quota" in error_message:
                        raise APIInsufficientQuota(error_message)
                    else:
                        raise APIAccessDenied(error_message or "Access denied")
                except ValueError:
                    # If JSON parsing fails
                    raise APIAccessDenied("Access denied")
            if response.status_code == 404:
                raise APIResourceNotFound(f"Path not found {path}")
            if response.status_code == 429:
                retry_after = response.headers.get('retry-after')
                if retry_after:
                    try:
                        seconds = int(retry_after)
                        minutes = seconds // 60
                        remaining_seconds = seconds % 60
                        time_msg = f" Quota will reset in {minutes} minutes and {remaining_seconds} seconds"
                    except ValueError:
                        time_msg = f" Retry after: {retry_after}"
                else:
                    time_msg = ""
                raise APIInsufficientQuota(f"Insufficient quota for API route.{time_msg}")
            if response.status_code == 502:
                raise APIBadGateway("Upstream server error")
            if response.status_code >= 400:
                raise APIFailure(f"Bad Request: HTTP {response.status_code}")
            
            return response
            
        except Timeout:
            request_duration = time.time() - start_time
            raise APITimeout(f"Request timed out after {request_duration:.2f} seconds")
        except ConnectionError as error:
            request_duration = time.time() - start_time
            raise APIConnectionError(f"Connection error after {request_duration:.2f} seconds: {error}")
        except (APIAccessDenied, APIInsufficientQuota, APIResourceNotFound, APIFailure,
                APITimeout, APIConnectionError, APIBadGateway, APIInsufficientPermissions,
                APIOrganizationNotAllowed):
            # Let all our custom exceptions propagate up unchanged
            raise
        except Exception as error:
            # Only truly unexpected errors get wrapped in a generic APIFailure
            raise APIFailure(f"Unexpected error: {error}", status_code=500)
