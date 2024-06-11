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
from socketdev.fullscans import Fullscans
from socketdev.repositories import Repositories
from socketdev.settings import Settings
from socketdev.socket_classes import Dependency, Org, Response
from socketdev.exceptions import APIKeyMissing, APIFailure, APIAccessDenied, APIInsufficientQuota, APIResourceNotFound


__author__ = 'socket.dev'
__version__ = '0.0.1'
__all__ = [
    "SocketDev",
]


global encoded_key
api_url = "https://api.socket.dev/v0"
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
        method: str = "GET",
):
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
            files=files
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
    def __init__(self, token: str):
        self.token = token + ":"
        encode_key(self.token)
        self.dependencies = Dependencies()
        self.npm = NPM()
        self.openapi = OpenAPI()
        self.org = Orgs()
        self.quota = Quota()
        self.report = Report()
        self.sbom = Sbom()
        self.purl = Purl()
        self.fullscans = Fullscans()
        self.repositories = Repositories()
        self.settings = Settings()
