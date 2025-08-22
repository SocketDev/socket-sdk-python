import json
import logging
from enum import Enum
from typing import Any, Dict, List, Optional, Union
from dataclasses import dataclass, asdict, field
import urllib.parse
from ..core.dedupe import Dedupe
from ..utils import IntegrationType, Utils

log = logging.getLogger("socketdev")


class SocketPURL_Type(str, Enum):
    UNKNOWN = "unknown"
    NPM = "npm"
    PYPI = "pypi"
    GOLANG = "golang"


class SocketIssueSeverity(str, Enum):
    LOW = "low"
    MIDDLE = "middle"
    HIGH = "high"
    CRITICAL = "critical"


class SocketCategory(str, Enum):
    SUPPLY_CHAIN_RISK = "supplyChainRisk"
    QUALITY = "quality"
    MAINTENANCE = "maintenance"
    VULNERABILITY = "vulnerability"
    LICENSE = "license"
    MISCELLANEOUS = "miscellaneous"


class DiffType(str, Enum):
    ADDED = "added"
    REMOVED = "removed"
    UNCHANGED = "unchanged"
    REPLACED = "replaced"
    UPDATED = "updated"


@dataclass(kw_only=True)
class SocketPURL:
    type: SocketPURL_Type
    name: Optional[str] = None
    namespace: Optional[str] = None
    release: Optional[str] = None
    subpath: Optional[str] = None
    version: Optional[str] = None

    def __getitem__(self, key):
        return getattr(self, key)

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "SocketPURL":
        return cls(
            type=SocketPURL_Type(data["type"]),
            name=data.get("name"),
            namespace=data.get("namespace"),
            release=data.get("release"),
            subpath=data.get("subpath"),
            version=data.get("version"),
        )


@dataclass
class SocketManifestReference:
    file: str
    start: Optional[int] = None
    end: Optional[int] = None

    def __getitem__(self, key):
        return getattr(self, key)

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "SocketManifestReference":
        return cls(file=data["file"], start=data.get("start"), end=data.get("end"))


@dataclass
class FullScanParams:
    repo: str
    org_slug: Optional[str] = None
    branch: Optional[str] = None
    commit_message: Optional[str] = None
    commit_hash: Optional[str] = None
    pull_request: Optional[int] = None
    committers: Optional[List[str]] = None
    integration_type: Optional[IntegrationType] = None
    integration_org_slug: Optional[str] = None
    make_default_branch: Optional[bool] = None
    set_as_pending_head: Optional[bool] = None
    tmp: Optional[bool] = None

    def __getitem__(self, key):
        return getattr(self, key)

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "FullScanParams":
        integration_type = data.get("integration_type")
        return cls(
            repo=data["repo"],
            org_slug=data.get("org_slug"),
            branch=data.get("branch"),
            commit_message=data.get("commit_message"),
            commit_hash=data.get("commit_hash"),
            pull_request=data.get("pull_request"),
            committers=data.get("committers"),
            integration_type=IntegrationType(integration_type) if integration_type else None,
            integration_org_slug=data.get("integration_org_slug"),
            make_default_branch=data.get("make_default_branch"),
            set_as_pending_head=data.get("set_as_pending_head"),
            tmp=data.get("tmp"),
        )


@dataclass
class FullScanMetadata:
    id: str
    created_at: str
    updated_at: str
    organization_id: str
    repository_id: str
    branch: str
    html_report_url: str
    repo: Optional[str] = None
    organization_slug: Optional[str] = None
    committers: Optional[List[str]] = None
    commit_message: Optional[str] = None
    commit_hash: Optional[str] = None
    pull_request: Optional[int] = None

    def __getitem__(self, key):
        return getattr(self, key)

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "FullScanMetadata":
        return cls(
            id=data["id"],
            created_at=data["created_at"],
            updated_at=data["updated_at"],
            organization_id=data["organization_id"],
            repository_id=data["repository_id"],
            branch=data["branch"],
            html_report_url=data["html_report_url"],
            repo=data.get("repo"),
            organization_slug=data.get("organization_slug"),
            committers=data.get("committers"),
            commit_message=data.get("commit_message"),
            commit_hash=data.get("commit_hash"),
            pull_request=data.get("pull_request"),
        )


@dataclass
class CreateFullScanResponse:
    success: bool
    status: int
    data: Optional[FullScanMetadata] = None
    message: Optional[str] = None

    def __getitem__(self, key):
        return getattr(self, key)

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "CreateFullScanResponse":
        return cls(
            success=data["success"],
            status=data["status"],
            message=data.get("message"),
            data=FullScanMetadata.from_dict(data.get("data")) if data.get("data") else None,
        )


@dataclass
class GetFullScanMetadataResponse:
    success: bool
    status: int
    data: Optional[FullScanMetadata] = None
    message: Optional[str] = None

    def __getitem__(self, key):
        return getattr(self, key)

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "GetFullScanMetadataResponse":
        return cls(
            success=data["success"],
            status=data["status"],
            message=data.get("message"),
            data=FullScanMetadata.from_dict(data.get("data")) if data.get("data") else None,
        )


@dataclass(kw_only=True)
class SocketArtifactLink:
    topLevelAncestors: List[str]
    direct: bool = False
    artifact: Optional[Dict] = None
    dependencies: Optional[List[str]] = None
    manifestFiles: Optional[List[SocketManifestReference]] = None

    def __getitem__(self, key):
        return getattr(self, key)

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "SocketArtifactLink":
        manifest_files = data.get("manifestFiles")
        direct_val = data.get("direct", False)
        return cls(
            topLevelAncestors=data["topLevelAncestors"],
            direct=direct_val if isinstance(direct_val, bool) else direct_val.lower() == "true",
            artifact=data.get("artifact"),
            dependencies=data.get("dependencies"),
            manifestFiles=[SocketManifestReference.from_dict(m) for m in manifest_files] if manifest_files else None,
        )


@dataclass
class SocketScore:
    supplyChain: float
    quality: float
    maintenance: float
    vulnerability: float
    license: float
    overall: float

    def __getitem__(self, key):
        return getattr(self, key)

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "SocketScore":
        return cls(
            supplyChain=data["supplyChain"],
            quality=data["quality"],
            maintenance=data["maintenance"],
            vulnerability=data["vulnerability"],
            license=data["license"],
            overall=data["overall"],
        )


@dataclass
class SecurityCapabilities:
    env: bool
    eval: bool
    fs: bool
    net: bool
    shell: bool
    unsafe: bool

    def __getitem__(self, key):
        return getattr(self, key)

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "SecurityCapabilities":
        return cls(
            env=data["env"],
            eval=data["eval"],
            fs=data["fs"],
            net=data["net"],
            shell=data["shell"],
            unsafe=data["unsafe"],
        )


@dataclass
class Alert:
    key: str
    type: int
    file: str
    start: int
    end: int
    props: Dict[str, Any]
    action: str
    actionPolicyIndex: int

    def __getitem__(self, key):
        return getattr(self, key)

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "Alert":
        return cls(
            key=data["key"],
            type=data["type"],
            file=data["file"],
            start=data["start"],
            end=data["end"],
            props=data["props"],
            action=data["action"],
            actionPolicyIndex=data["actionPolicyIndex"],
        )


@dataclass
class LicenseMatch:
    licenseId: str
    licenseExceptionId: str

    def __getitem__(self, key):
        return getattr(self, key)

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "LicenseMatch":
        return cls(licenseId=data["licenseId"], licenseExceptionId=data["licenseExceptionId"])


@dataclass
class LicenseDetail:
    authors: List[str]
    errorData: str
    filepath: str
    match_strength: int
    provenance: str
    spdxDisj: List[List[LicenseMatch]]

    def __getitem__(self, key):
        return getattr(self, key)

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "LicenseDetail":
        return cls(
            spdxDisj=data["spdxDisj"],
            authors=data["authors"],
            errorData=data["errorData"],
            provenance=data["provenance"],
            filepath=data["filepath"],
            match_strength=data["match_strength"],

        )


@dataclass
class AttributionData:
    purl: str
    foundAuthors: List[str]
    foundInFilepath: Optional[str] = None
    spdxExpr: Optional[str] = None

    def __getitem__(self, key):
        return getattr(self, key)

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "AttributionData":
        return cls(
            purl=data["purl"],
            foundAuthors=data["foundAuthors"],
            foundInFilepath=data.get("foundInFilepath"),
            spdxExpr=data.get("spdxExpr"),
        )


@dataclass
class LicenseAttribution:
    attribText: str
    attribData: List[AttributionData]

    def __getitem__(self, key):
        return getattr(self, key)

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "LicenseAttribution":
        return cls(
            attribText=data["attribText"], attribData=[AttributionData.from_dict(item) for item in data["attribData"]]
        )


@dataclass
class SocketAlert:
    key: str
    type: str
    severity: SocketIssueSeverity
    category: SocketCategory
    file: Optional[str] = None
    start: Optional[int] = None
    end: Optional[int] = None
    props: Optional[Dict[str, Any]] = None
    action: Optional[str] = None
    actionPolicyIndex: Optional[int] = None

    def __getitem__(self, key):
        return getattr(self, key)

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "SocketAlert":
        return cls(
            key=data["key"],
            type=data["type"],
            severity=SocketIssueSeverity(data["severity"]),
            category=SocketCategory(data["category"]),
            file=data.get("file"),
            start=data.get("start"),
            end=data.get("end"),
            props=data.get("props"),
            action=data.get("action"),
            actionPolicyIndex=data.get("actionPolicyIndex"),
        )


@dataclass
class DiffArtifact:
    diffType: DiffType
    id: str
    type: str
    name: str
    version: str
    licenseDetails: List[LicenseDetail]
    score: Optional[SocketScore] = None
    author: List[str] = field(default_factory=list)
    alerts: List[SocketAlert] = field(default_factory=list)
    license: Optional[str] = None
    files: Optional[str] = None
    capabilities: Optional[SecurityCapabilities] = None
    base: Optional[List[SocketArtifactLink]] = None
    head: Optional[List[SocketArtifactLink]] = None
    namespace: Optional[str] = None
    subpath: Optional[str] = None
    artifact_id: Optional[str] = None
    artifactId: Optional[str] = None
    qualifiers: Optional[Dict[str, Any]] = None
    size: Optional[int] = None
    state: Optional[str] = None
    error: Optional[str] = None
    licenseAttrib: Optional[List[LicenseAttribution]] = None

    def __getitem__(self, key):
        return getattr(self, key)

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "DiffArtifact":
        base_data = data.get("base")
        head_data = data.get("head")

        score_data = data.get("score") or data.get("scores")
        score = SocketScore.from_dict(score_data) if score_data else None
        license_details_source = data.get("licenseDetails")
        if license_details_source:
            license_details = [LicenseDetail.from_dict(detail) for detail in license_details_source]
        else:
            license_details = []
        license_attrib_source = data.get("licenseAttrib")
        if license_attrib_source:
            license_attrib = [LicenseAttribution.from_dict(attrib) for attrib in license_attrib_source]
        else:
            license_attrib = []

        return cls(
            diffType=DiffType(data["diffType"]),
            id=data["id"],
            type=data["type"],
            name=data["name"],
            score=score,
            version=data["version"],
            alerts=[SocketAlert.from_dict(alert) for alert in data.get("alerts", [])],
            licenseDetails=license_details,
            files=data.get("files"),
            license=data.get("license"),
            capabilities=SecurityCapabilities.from_dict(data["capabilities"]) if data.get("capabilities") else None,
            base=[SocketArtifactLink.from_dict(b) for b in base_data] if base_data else None,
            head=[SocketArtifactLink.from_dict(h) for h in head_data] if head_data else None,
            namespace=data.get("namespace"),
            subpath=data.get("subpath"),
            artifact_id=data.get("artifact_id"),
            artifactId=data.get("artifactId"),
            qualifiers=data.get("qualifiers"),
            size=data.get("size"),
            author=data.get("author", []),
            state=data.get("state"),
            error=data.get("error"),
            licenseAttrib=license_attrib
            if data.get("licenseAttrib")
            else None,
        )


@dataclass
class DiffArtifacts:
    added: List[DiffArtifact]
    removed: List[DiffArtifact]
    unchanged: List[DiffArtifact]
    replaced: List[DiffArtifact]
    updated: List[DiffArtifact]

    def __getitem__(self, key):
        return getattr(self, key)

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "DiffArtifacts":
        return cls(
            added=[DiffArtifact.from_dict(a) for a in data["added"]],
            removed=[DiffArtifact.from_dict(a) for a in data["removed"]],
            unchanged=[DiffArtifact.from_dict(a) for a in data["unchanged"]],
            replaced=[DiffArtifact.from_dict(a) for a in data["replaced"]],
            updated=[DiffArtifact.from_dict(a) for a in data["updated"]],
        )


@dataclass
class CommitInfo:
    repository_id: str
    branch: str
    id: str
    organization_id: str
    committers: List[str]
    commit_message: Optional[str] = None
    commit_hash: Optional[str] = None
    pull_request: Optional[int] = None

    def __getitem__(self, key):
        return getattr(self, key)

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "CommitInfo":
        return cls(
            repository_id=data["repository_id"],
            branch=data["branch"],
            id=data["id"],
            organization_id=data["organization_id"],
            committers=data["committers"],
            commit_message=data.get("commit_message"),
            commit_hash=data.get("commit_hash"),
            pull_request=data.get("pull_request"),
        )


@dataclass
class FullScanDiffReport:
    before: CommitInfo
    after: CommitInfo
    diff_report_url: str
    artifacts: DiffArtifacts
    directDependenciesChanged: bool = False

    def __getitem__(self, key):
        return getattr(self, key)

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "FullScanDiffReport":
        return cls(
            before=CommitInfo.from_dict(data["before"]),
            after=CommitInfo.from_dict(data["after"]),
            directDependenciesChanged=data.get("directDependenciesChanged", False),
            diff_report_url=data["diff_report_url"],
            artifacts=DiffArtifacts.from_dict(data["artifacts"]),
        )


@dataclass
class StreamDiffResponse:
    success: bool
    status: int
    data: Optional[FullScanDiffReport] = None
    message: Optional[str] = None

    def __getitem__(self, key):
        return getattr(self, key)

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "StreamDiffResponse":
        return cls(
            success=data["success"],
            status=data["status"],
            message=data.get("message"),
            data=FullScanDiffReport.from_dict(data.get("data")) if data.get("data") else None,
        )


@dataclass(kw_only=True)
class SocketArtifact(SocketPURL, SocketArtifactLink):
    id: str
    alerts: List[SocketAlert]
    score: SocketScore
    author: Optional[List[str]] = field(default_factory=list)
    batchIndex: Optional[int] = None
    license: Optional[str] = None
    licenseAttrib: Optional[List[LicenseAttribution]] = field(default_factory=list)
    licenseDetails: Optional[List[LicenseDetail]] = field(default_factory=list)
    size: Optional[int] = None

    def __getitem__(self, key):
        return getattr(self, key)

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "SocketArtifact":
        purl_data = {k: data.get(k) for k in SocketPURL.__dataclass_fields__}
        link_data = {k: data.get(k) for k in SocketArtifactLink.__dataclass_fields__}

        alerts = data.get("alerts")
        license_attrib = data.get("licenseAttrib")
        license_details = data.get("licenseDetails")
        score = data.get("score")

        return cls(
            **purl_data,
            **link_data,
            id=data["id"],
            alerts=[SocketAlert.from_dict(a) for a in alerts] if alerts is not None else [],
            author=data.get("author"),
            batchIndex=data.get("batchIndex"),
            license=data.get("license"),
            licenseAttrib=[LicenseAttribution.from_dict(la) for la in license_attrib] if license_attrib else None,
            licenseDetails=[LicenseDetail.from_dict(ld) for ld in license_details] if license_details else None,
            score=SocketScore.from_dict(score) if score else None,
            size=data.get("size"),
        )


@dataclass
class FullScanStreamResponse:
    success: bool
    status: int
    artifacts: Optional[Dict[str, SocketArtifact]] = None
    message: Optional[str] = None

    def __getitem__(self, key):
        return getattr(self, key)

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "FullScanStreamResponse":
        return cls(
            success=data["success"],
            status=data["status"],
            message=data.get("message"),
            artifacts={k: SocketArtifact.from_dict(v) for k, v in data["artifacts"].items()}
            if data.get("artifacts")
            else None,
        )


class FullScans:
    def __init__(self, api):
        self.api = api


    def get(self, org_slug: str, params: dict, use_types: bool = False) -> Union[dict, GetFullScanMetadataResponse]:
        params_arg = urllib.parse.urlencode(params)
        path = "orgs/" + org_slug + "/full-scans?" + str(params_arg)
        response = self.api.do_request(path=path)

        if response.status_code == 200:
            result = response.json()
            if use_types:
                return GetFullScanMetadataResponse.from_dict({"success": True, "status": 200, "data": result})

            return result

        error_message = response.json().get("error", {}).get("message", "Unknown error")
        log.error(f"Error getting full scan metadata: {response.status_code}, message: {error_message}")
        if use_types:
            return GetFullScanMetadataResponse.from_dict(
                {"success": False, "status": response.status_code, "message": error_message}
            )
        return {}

    def post(self, files: list, params: FullScanParams, use_types: bool = False, use_lazy_loading: bool = False, workspace: str = None, max_open_files: int = 100) -> Union[dict, CreateFullScanResponse]:
        """
        Create a new full scan by uploading manifest files.
        
        Args:
            files: List of file paths to upload for scanning
            params: FullScanParams object containing scan configuration
            use_types: Whether to return typed response objects (default: False)
            use_lazy_loading: Whether to use lazy file loading to prevent "too many open files" 
                            errors when uploading large numbers of files (default: False)
                            NOTE: In version 3.0, this will default to True for better performance
            workspace: Base directory path to make file paths relative to
            max_open_files: Maximum number of files to keep open simultaneously when using 
                          lazy loading. Useful for systems with low ulimit values (default: 100)
        
        Returns:
            dict or CreateFullScanResponse: API response containing scan results
            
        Note:
            When use_lazy_loading=True, files are opened only when needed during upload,
            preventing file descriptor exhaustion. The max_open_files parameter controls how many
            files can be open simultaneously - set this lower on systems with restrictive ulimits.
            
            For large file uploads (>100 files), it's recommended to set use_lazy_loading=True.
        """
        Utils.validate_integration_type(params.integration_type if params.integration_type else "api")
        org_slug = str(params.org_slug)
        params_dict = params.to_dict()
        params_dict.pop("org_slug")
        params_arg = urllib.parse.urlencode(params_dict)
        path = "orgs/" + org_slug + "/full-scans?" + str(params_arg)

        # Use lazy loading if requested
        if use_lazy_loading:
            prepared_files = Utils.load_files_for_sending_lazy(files, workspace, max_open_files)
        else:
            prepared_files = files

        response = self.api.do_request(path=path, method="POST", files=prepared_files)

        if response.status_code == 201:
            result = response.json()
            if use_types:
                return CreateFullScanResponse.from_dict({"success": True, "status": 201, "data": result})
            return result

        error_message = response.json().get("error", {}).get("message", "Unknown error")
        log.error(f"Error posting {files} to the Fullscans API: {response.status_code}, message: {error_message}")
        if use_types:
            return CreateFullScanResponse.from_dict(
                {"success": False, "status": response.status_code, "message": error_message}
            )
        return {}

    def delete(self, org_slug: str, full_scan_id: str) -> dict:
        path = "orgs/" + org_slug + "/full-scans/" + full_scan_id

        response = self.api.do_request(path=path, method="DELETE")

        if response.status_code == 200:
            result = response.json()
            return result

        error_message = response.json().get("error", {}).get("message", "Unknown error")
        log.error(f"Error deleting full scan: {response.status_code}, message: {error_message}")
        return {}

    def stream_diff(
            self,
            org_slug: str,
            before: str,
            after: str,
            use_types: bool = True,
            include_license_details: str = "true",
            **kwargs,
    ) -> Union[dict, StreamDiffResponse]:
        path = f"orgs/{org_slug}/full-scans/diff?before={before}&after={after}&include_license_details={include_license_details}"
        if kwargs:
            for key, value in kwargs.items():
                path += f"&{key}={value}"

        response = self.api.do_request(path=path, method="GET")

        if response.status_code == 200:
            result = response.json()
            if use_types:
                return StreamDiffResponse.from_dict({"success": True, "status": 200, "data": result})
            return result

        error_message = response.json().get("error", {}).get("message", "Unknown error")
        log.error(f"Error streaming diff: {response.status_code}, message: {error_message}")
        if use_types:
            return StreamDiffResponse.from_dict(
                {"success": False, "status": response.status_code, "message": error_message}
            )
        return {}

    def stream(self, org_slug: str, full_scan_id: str, use_types: bool = False) -> Union[dict, FullScanStreamResponse]:
        path = "orgs/" + org_slug + "/full-scans/" + full_scan_id
        response = self.api.do_request(path=path, method="GET")

        if response.status_code == 200:
            try:
                stream_str = []
                artifacts = {}
                result = response.text
                result = result.strip('"').strip()
                for line in result.split("\n"):
                    if line != '"' and line != "" and line is not None:
                        item = json.loads(line)
                        stream_str.append(item)
                stream_deduped = Dedupe.dedupe(stream_str, batched=False)
                for batch in stream_deduped:
                    artifacts[batch["id"]] = batch
                if use_types:
                    return FullScanStreamResponse.from_dict({"success": True, "status": 200, "artifacts": artifacts})
                return artifacts

            except Exception as e:
                error_message = f"Error parsing stream response: {str(e)}"
                log.error(error_message)
                if use_types:
                    return FullScanStreamResponse.from_dict(
                        {"success": False, "status": response.status_code, "message": error_message}
                    )
                return {}

        error_message = response.json().get("error", {}).get("message", "Unknown error")
        log.error(f"Error streaming full scan: {response.status_code}, message: {error_message}")
        if use_types:
            return FullScanStreamResponse.from_dict(
                {"success": False, "status": response.status_code, "message": error_message}
            )
        return {}

    def metadata(
        self, org_slug: str, full_scan_id: str, use_types: bool = False
    ) -> Union[dict, GetFullScanMetadataResponse]:
        path = "orgs/" + org_slug + "/full-scans/" + full_scan_id + "/metadata"

        response = self.api.do_request(path=path, method="GET")

        if response.status_code == 200:
            result = response.json()
            if use_types:
                return GetFullScanMetadataResponse.from_dict({"success": True, "status": 200, "data": result})
            return result

        error_message = response.json().get("error", {}).get("message", "Unknown error")
        log.error(f"Error getting metadata: {response.status_code}, message: {error_message}")
        if use_types:
            return GetFullScanMetadataResponse.from_dict(
                {"success": False, "status": response.status_code, "message": error_message}
            )
        return {}

    def gfm(self, org_slug: str, before: str, after: str) -> dict:
        path = "orgs/" + org_slug + f"/full-scans/diff/gfm?before={before}&after={after}"
        response = self.api.do_request(path=path, method="GET")
        if response.status_code == 200:
            result = response.json()
            return result

        error_message = response.json().get("error", {}).get("message", "Unknown error")
        log.error(f"Error getting diff scan results: {response.status_code}, message: {error_message}")
        return {}