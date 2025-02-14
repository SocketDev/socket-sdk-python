import logging

from socketdev.core.api import API
from socketdev.dependencies import Dependencies
from socketdev.export import Export
from socketdev.fullscans import FullScans
from socketdev.npm import NPM
from socketdev.openapi import OpenAPI
from socketdev.org import Orgs
from socketdev.purl import Purl
from socketdev.quota import Quota
from socketdev.report import Report
from socketdev.repos import Repos
from socketdev.repositories import Repositories
from socketdev.sbom import Sbom
from socketdev.settings import Settings
from socketdev.utils import Utils, IntegrationType, INTEGRATION_TYPES
from socketdev.version import __version__


__author__ = "socket.dev"
__version__ = __version__
__all__ = ["socketdev", "Utils", "IntegrationType", "INTEGRATION_TYPES"]



global encoded_key
encoded_key: str

api_url = "https://api.socket.dev/v0"
request_timeout = 1200
log = logging.getLogger("socketdev")
log.addHandler(logging.NullHandler())


class socketdev:
    def __init__(self, token: str, timeout: int = 1200):
        self.api = API()
        self.token = token + ":"
        self.api.encode_key(self.token)
        self.api.set_timeout(timeout)

        self.dependencies = Dependencies(self.api)
        self.npm = NPM(self.api)
        self.openapi = OpenAPI(self.api)
        self.org = Orgs(self.api)
        self.quota = Quota(self.api)
        self.report = Report(self.api)
        self.sbom = Sbom(self.api)
        self.purl = Purl(self.api)
        self.fullscans = FullScans(self.api)
        self.export = Export(self.api)
        self.repositories = Repositories(self.api)
        self.repos = Repos(self.api)
        self.settings = Settings(self.api)
        self.utils = Utils()

    @staticmethod
    def set_timeout(timeout: int):
        # Kept for backwards compatibility
        pass
