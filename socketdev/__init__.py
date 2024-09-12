import logging
import requests
import base64

from socketdev.dependencies import Dependencies
from socketdev.npm import NPM
from socketdev.openapi import OpenAPI
from socketdev.org import Orgs
from socketdev.quota import Quota
from socketdev.report import Report
from socketdev.sbom import Sbom
from socketdev.purl import Purl
from socketdev.fullscans import FullScans
from socketdev.repositories import Repositories
from socketdev.settings import Settings
from core.classes import Response
from socketdev.exceptions import APIKeyMissing, APIFailure, APIAccessDenied, APIInsufficientQuota, APIResourceNotFound


__author__ = 'socket.dev'
__version__ = '1.0.0'
__all__ = [
    "SocketDev",
]


global encoded_key
api_url = "https://api.socket.dev/v0"
request_timeout = 30
log = logging.getLogger("socketdev")
log.addHandler(logging.NullHandler())


def encode_key(token: str):
    global encoded_key
    encoded_key = base64.b64encode(token.encode()).decode('ascii')


def do_request(
        path: str,
        headers: dict = None,
        payload: [dict, str] = None,
        files: list = None,
        method: str = "GET"
) -> Response:
    """
    Shared function for performing the requests against the API.
    :param path: String path of the URL
    :param headers: Optional dictionary of the headers to include in the request. Defaults to None
    :param payload: Optional dictionary or string of the payload to POST. Defaults to None
    :param files: Optional list of files to send. Defaults to None
    :param method: Optional string of the method for the Request. Defaults to GET
    """

    if encoded_key is None or encoded_key == "":
        raise APIKeyMissing

    if headers is None:
        headers = {
            'Authorization': f"Basic {encoded_key}",
            'User-Agent': 'SocketPythonScript/0.0.1',
            "accept": "application/json"
        }
    url = f"{api_url}/{path}"
    try:
        response = requests.request(
            method.upper(),
            url,
            headers=headers,
            data=payload,
            files=files,
            timeout=request_timeout
        )
        if response.status_code >= 400:
            raise APIFailure("Bad Request")
        elif response.status_code == 401:
            raise APIAccessDenied("Unauthorized")
        elif response.status_code == 403:
            raise APIInsufficientQuota("Insufficient max_quota for API method")
        elif response.status_code == 404:
            raise APIResourceNotFound(f"Path not found {path}")
        elif response.status_code == 429:
            raise APIInsufficientQuota("Insufficient quota for API route")
    except Exception as error:
        response = Response(
            text=f"{error}",
            error=True,
            status_code=500
        )
        raise APIFailure(response)
    return response


class SocketDev:
    token: str
    timeout: int
    dependencies: Dependencies
    npm: NPM
    openapi: OpenAPI
    org: Orgs
    quota: Quota
    report: Report
    sbom: Sbom
    purl: purl
    fullscans: FullScans
    repositories: Report
    settings: Settings

    def __init__(self, token: str, timeout: int = 30):
        self.token = token + ":"
        encode_key(self.token)
        self.timeout = timeout
        SocketDev.set_timeout(self.timeout)
        self.dependencies = Dependencies()
        self.npm = NPM()
        self.openapi = OpenAPI()
        self.org = Orgs()
        self.quota = Quota()
        self.report = Report()
        self.sbom = Sbom()
        self.purl = Purl()
        self.fullscans = FullScans()
        self.repositories = Repositories()
        self.settings = Settings()

    @staticmethod
    def set_timeout(timeout: int):
        global request_timeout
        request_timeout = timeout
