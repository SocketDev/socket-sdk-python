import os
from socketdev.core.api import API
from socketdev.dependencies import Dependencies
from socketdev.diffscans import DiffScans
from socketdev.export import Export
from socketdev.fullscans import FullScans
from socketdev.historical import Historical
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
from socketdev.triage import Triage
from socketdev.utils import Utils, IntegrationType, INTEGRATION_TYPES
from socketdev.version import __version__
from socketdev.labels import Labels
from socketdev.licensemetadata import LicenseMetadata
from socketdev.threatfeed import ThreatFeed
from socketdev.apitokens import ApiTokens
from socketdev.auditlog import AuditLog
from socketdev.analytics import Analytics
from socketdev.alerttypes import AlertTypes
from socketdev.basics import Basics
from socketdev.uploadmanifests import UploadManifests
from socketdev.alertfullscansearch import AlertFullScanSearch
from socketdev.alerts import Alerts
from socketdev.fixes import Fixes
from socketdev.supportedfiles import SupportedFiles
from socketdev.webhooks import Webhooks
from socketdev.telemetry import Telemetry
from socketdev.log import log
from typing import Optional

__author__ = "socket.dev"
__version__ = __version__
__all__ = ["socketdev", "Utils", "IntegrationType", "INTEGRATION_TYPES"]


global encoded_key
encoded_key: str

api_url = "https://api.socket.dev/v0"
request_timeout = 1200


# TODO: Add debug flag to constructor to enable verbose error logging for API response parsing.


class socketdev:
    def __init__(self, token: Optional[str] = None, timeout: int = 1200, allow_unverified: bool = False):
        # Try to get token from environment variables if not provided
        if token is None:
            token = (
                os.getenv("SOCKET_SECURITY_API_TOKEN") or
                os.getenv("SOCKET_SECURITY_API_KEY") or
                os.getenv("SOCKET_API_KEY") or
                os.getenv("SOCKET_API_TOKEN")
            )
        
        if token is None:
            raise ValueError(
                "API token is required. Provide it as a parameter or set one of these environment variables: "
                "SOCKET_SECURITY_API_TOKEN, SOCKET_SECURITY_API_KEY, SOCKET_API_KEY, SOCKET_API_TOKEN"
            )
        
        self.api = API()
        self.token = token + ":"
        self.api.encode_key(self.token)
        self.api.set_timeout(timeout)
        self.api.set_allow_unverified(allow_unverified)

        self.dependencies = Dependencies(self.api)
        self.export = Export(self.api)
        self.fullscans = FullScans(self.api)
        self.historical = Historical(self.api)
        self.npm = NPM(self.api)
        self.openapi = OpenAPI(self.api)
        self.org = Orgs(self.api)
        self.purl = Purl(self.api)
        self.quota = Quota(self.api)
        self.report = Report(self.api)
        self.repos = Repos(self.api)
        self.repositories = Repositories(self.api)
        self.sbom = Sbom(self.api)
        self.settings = Settings(self.api)
        self.triage = Triage(self.api)
        self.utils = Utils()
        self.labels = Labels(self.api)
        self.licensemetadata = LicenseMetadata(self.api)
        self.diffscans = DiffScans(self.api)
        self.threatfeed = ThreatFeed(self.api)
        self.apitokens = ApiTokens(self.api)
        self.auditlog = AuditLog(self.api)
        self.analytics = Analytics(self.api)
        self.alerttypes = AlertTypes(self.api)
        self.basics = Basics(self.api)
        self.uploadmanifests = UploadManifests(self.api)
        self.alertfullscansearch = AlertFullScanSearch(self.api)
        self.alerts = Alerts(self.api)
        self.fixes = Fixes(self.api)
        self.supportedfiles = SupportedFiles(self.api)
        self.webhooks = Webhooks(self.api)
        self.telemetry = Telemetry(self.api)

    @staticmethod
    def set_timeout(timeout: int):
        # Kept for backwards compatibility
        pass
