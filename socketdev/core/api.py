import base64
from socketdev.log import log

import requests
from socketdev.core.classes import Response
from socketdev.exceptions import (
    APIKeyMissing,
    APIFailure,
    APIAccessDenied,
    APIInsufficientQuota,
    APIResourceNotFound,
    APITimeout,
    APIConnectionError,
    APIBadGateway,
    APIInsufficientPermissions,
    APIOrganizationNotAllowed,
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
        self,
        path: str,
        headers: dict | None = None,
        payload: [dict, str] = None,
        files: list = None,
        method: str = "GET",
    ) -> Response:
        if self.encoded_key is None or self.encoded_key == "":
            raise APIKeyMissing

        if headers is None:
            headers = {
                "Authorization": f"Basic {self.encoded_key}",
                "User-Agent": f"SocketSDKPython/{__version__}",
                "accept": "application/json",
            }
        url = f"{self.api_url}/{path}"

        def format_headers(headers_dict):
            return "\n".join(f"{k}: {v}" for k, v in headers_dict.items())

        start_time = time.time()
        try:
            
            response = requests.request(
                method.upper(), url, headers=headers, data=payload, files=files, timeout=self.request_timeout
            )
            request_duration = time.time() - start_time

            headers_str = f"\n\nHeaders:\n{format_headers(response.headers)}" if response.headers else ""
            path_str = f"\nPath: {url}"

            if response.status_code == 401:
                raise APIAccessDenied(f"Unauthorized{path_str}{headers_str}")
            if response.status_code == 403:
                try:
                    error_message = response.json().get("error", {}).get("message", "")
                    if "Insufficient permissions for API method" in error_message:
                        log.error(f"{error_message}{path_str}{headers_str}")
                        raise APIInsufficientPermissions()
                    elif "Organization not allowed" in error_message:
                        log.error(f"{error_message}{path_str}{headers_str}")
                        raise APIOrganizationNotAllowed()
                    elif "Insufficient max quota" in error_message:
                        log.error(f"{error_message}{path_str}{headers_str}")
                        raise APIInsufficientQuota()
                    else:
                        raise APIAccessDenied(f"{error_message or 'Access denied'}{path_str}{headers_str}")
                except ValueError:
                    raise APIAccessDenied(f"Access denied{path_str}{headers_str}")
            if response.status_code == 404:
                log.error(f"Path not found {path}{path_str}{headers_str}")
                raise APIResourceNotFound()
            if response.status_code == 429:
                retry_after = response.headers.get("retry-after")
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
                log.error(f"Insufficient quota for API route.{time_msg}{path_str}{headers_str}")
                raise APIInsufficientQuota()
            if response.status_code == 502:
                log.error(f"Upstream server error{path_str}{headers_str}")
                raise APIBadGateway()
            if response.status_code >= 400:
                try:
                    error_json = response.json()
                except Exception:
                    error_json = None
                error_message = error_json.get("error", {}).get("message") if error_json else response.text
                error = (
                    f"Bad Request: HTTP original_status_code:{response.status_code}{path_str}{headers_str}\n"
                    f"Error message: {error_message}"
                )
                log.error(error)
                raise APIFailure(error)

            return response
        except Timeout:
            request_duration = time.time() - start_time
            log.error(f"Request timed out after {request_duration:.2f} seconds")
            raise APITimeout()
        except ConnectionError as error:
            request_duration = time.time() - start_time
            log.error(f"Connection error after {request_duration:.2f} seconds: {error}")
            raise APIConnectionError()
        except (
            APIAccessDenied,
            APIInsufficientQuota,
            APIResourceNotFound,
            APIFailure,
            APITimeout,
            APIConnectionError,
            APIBadGateway,
            APIInsufficientPermissions,
            APIOrganizationNotAllowed,
        ):
            # Let all our custom exceptions propagate up unchanged
            raise
        except Exception as error:
            # Only truly unexpected errors get wrapped in a generic APIFailure
            log.error(f"Unexpected error: {error}")
            raise APIFailure()
