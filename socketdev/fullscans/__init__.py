import json
import logging
from enum import Enum
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, asdict, field


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

    def __getitem__(self, key): return getattr(self, key)
    def to_dict(self): return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "SocketPURL":
        return cls(
            type=SocketPURL_Type(data["type"]),
            name=data.get("name"),
            namespace=data.get("namespace"),
            release=data.get("release"),
            subpath=data.get("subpath"),
            version=data.get("version")
        )

@dataclass
class SocketManifestReference:
    file: str
    start: Optional[int] = None
    end: Optional[int] = None

    def __getitem__(self, key): return getattr(self, key)
    def to_dict(self): return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "SocketManifestReference":
        return cls(
            file=data["file"],
            start=data.get("start"),
            end=data.get("end")
        )

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

    def __getitem__(self, key): return getattr(self, key)
    def to_dict(self): return asdict(self)

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
            tmp=data.get("tmp")
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
    repo: Optional[str] = None # In docs, never shows up
    organization_slug: Optional[str] = None # In docs, never shows up
    committers: Optional[List[str]] = None
    commit_message: Optional[str] = None
    commit_hash: Optional[str] = None
    pull_request: Optional[int] = None

    def __getitem__(self, key): return getattr(self, key)
    def to_dict(self): return asdict(self)

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
            pull_request=data.get("pull_request")
        )

@dataclass
class CreateFullScanResponse:
    success: bool
    status: int
    data: Optional[FullScanMetadata] = None
    message: Optional[str] = None

    def __getitem__(self, key): return getattr(self, key)
    def to_dict(self): return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "CreateFullScanResponse":
        return cls(
            success=data["success"],
            status=data["status"],
            message=data.get("message"),
            data=FullScanMetadata.from_dict(data.get("data")) if data.get("data") else None
        )

@dataclass
class GetFullScanMetadataResponse:
    success: bool
    status: int
    data: Optional[FullScanMetadata] = None
    message: Optional[str] = None

    def __getitem__(self, key): return getattr(self, key)
    def to_dict(self): return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "GetFullScanMetadataResponse":
        return cls(
            success=data["success"],
            status=data["status"],
            message=data.get("message"),
            data=FullScanMetadata.from_dict(data.get("data")) if data.get("data") else None
        )

@dataclass
class DependencyRef:
    direct: bool
    toplevelAncestors: List[str]

    def __getitem__(self, key): return getattr(self, key)
    def to_dict(self): return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "DependencyRef":
        return cls(
            direct=data["direct"],
            toplevelAncestors=data["toplevelAncestors"]
        )

@dataclass
class SocketScore:
    supplyChain: float
    quality: float
    maintenance: float
    vulnerability: float
    license: float
    overall: float

    def __getitem__(self, key): return getattr(self, key)
    def to_dict(self): return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "SocketScore":
        return cls(
            supplyChain=data["supplyChain"],
            quality=data["quality"],
            maintenance=data["maintenance"],
            vulnerability=data["vulnerability"],
            license=data["license"],
            overall=data["overall"]
        )

@dataclass
class SecurityCapabilities:
    env: bool
    eval: bool
    fs: bool
    net: bool
    shell: bool
    unsafe: bool

    def __getitem__(self, key): return getattr(self, key)
    def to_dict(self): return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "SecurityCapabilities":
        return cls(
            env=data["env"],
            eval=data["eval"],
            fs=data["fs"],
            net=data["net"],
            shell=data["shell"],
            unsafe=data["unsafe"]
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

    def __getitem__(self, key): return getattr(self, key)
    def to_dict(self): return asdict(self)

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
            actionPolicyIndex=data["actionPolicyIndex"]
        )

@dataclass
class LicenseMatch:
    licenseId: str
    licenseExceptionId: str

    def __getitem__(self, key): return getattr(self, key)
    def to_dict(self): return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "LicenseMatch":
        return cls(
            licenseId=data["licenseId"],
            licenseExceptionId=data["licenseExceptionId"]
        )

@dataclass
class LicenseDetail:
    authors: List[str]
    charEnd: int
    charStart: int
    filepath: str
    match_strength: int
    filehash: str
    provenance: str
    spdxDisj: List[List[LicenseMatch]]

    def __getitem__(self, key): return getattr(self, key)
    def to_dict(self): return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "LicenseDetail":
        return cls(
            authors=data["authors"],
            charEnd=data["charEnd"],
            charStart=data["charStart"],
            filepath=data["filepath"],
            match_strength=data["match_strength"],
            filehash=data["filehash"],
            provenance=data["provenance"],
            spdxDisj=[[LicenseMatch.from_dict(match) for match in group] 
                     for group in data["spdxDisj"]]
        )

@dataclass
class AttributionData:
    purl: str
    foundAuthors: List[str]
    foundInFilepath: Optional[str] = None
    spdxExpr: Optional[str] = None

    def __getitem__(self, key): return getattr(self, key)
    def to_dict(self): return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "AttributionData":
        return cls(
            purl=data["purl"],
            foundAuthors=data["foundAuthors"],
            foundInFilepath=data.get("foundInFilepath"),
            spdxExpr=data.get("spdxExpr")
        )

@dataclass
class LicenseAttribution:
    attribText: str
    attribData: List[AttributionData]

    def __getitem__(self, key): return getattr(self, key)
    def to_dict(self): return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "LicenseAttribution":
        return cls(
            attribText=data["attribText"],
            attribData=[AttributionData.from_dict(item) for item in data["attribData"]]
        )

@dataclass
class DiffArtifactAlert:
    key: str
    type: str
    severity: Optional[SocketIssueSeverity] = None
    category: Optional[SocketCategory] = None
    file: Optional[str] = None
    start: Optional[int] = None
    end: Optional[int] = None
    props: Optional[Dict[str, Any]] = None
    action: Optional[str] = None
    actionPolicyIndex: Optional[int] = None

    def __getitem__(self, key): return getattr(self, key)
    def to_dict(self): return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "DiffArtifactAlert":
        severity = data.get("severity")
        category = data.get("category")
        return cls(
            key=data["key"],
            type=data["type"],
            severity=SocketIssueSeverity(severity) if severity else None,
            category=SocketCategory(category) if category else None,
            file=data.get("file"),
            start=data.get("start"),
            end=data.get("end"),
            props=data.get("props"),
            action=data.get("action"),
            actionPolicyIndex=data.get("actionPolicyIndex")
        )

@dataclass
class DiffArtifact:
    diffType: DiffType
    id: str
    type: str
    name: str
    license: str
    scores: SocketScore
    capabilities: SecurityCapabilities
    files: str
    version: str
    alerts: List[DiffArtifactAlert]
    licenseDetails: List[LicenseDetail]
    base: Optional[DependencyRef] = None
    head: Optional[DependencyRef] = None
    namespace: Optional[str] = None
    subpath: Optional[str] = None
    artifact_id: Optional[str] = None
    artifactId: Optional[str] = None
    qualifiers: Optional[Dict[str, Any]] = None
    size: Optional[int] = None
    author: Optional[str] = None
    state: Optional[str] = None
    error: Optional[str] = None
    licenseAttrib: Optional[List[LicenseAttribution]] = None

    def __getitem__(self, key): return getattr(self, key)
    def to_dict(self): return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "DiffArtifact":
        return cls(
            diffType=DiffType(data["diffType"]),
            id=data["id"],
            type=data["type"],
            name=data["name"],
            license=data.get("license", ""),
            scores=SocketScore.from_dict(data["score"]),
            capabilities=SecurityCapabilities.from_dict(data["capabilities"]),
            files=data["files"],
            version=data["version"],
            alerts=[DiffArtifactAlert.from_dict(alert) for alert in data["alerts"]],
            licenseDetails=[LicenseDetail.from_dict(detail) for detail in data["licenseDetails"]],
            base=DependencyRef.from_dict(data["base"]) if data.get("base") else None,
            head=DependencyRef.from_dict(data["head"]) if data.get("head") else None,
            namespace=data.get("namespace"),
            subpath=data.get("subpath"),
            artifact_id=data.get("artifact_id"),
            artifactId=data.get("artifactId"),
            qualifiers=data.get("qualifiers"),
            size=data.get("size"),
            author=data.get("author"),
            state=data.get("state"),
            error=data.get("error"),
            licenseAttrib=[LicenseAttribution.from_dict(attrib) for attrib in data["licenseAttrib"]] if data.get("licenseAttrib") else None
        )

@dataclass
class DiffArtifacts:
    added: List[DiffArtifact]
    removed: List[DiffArtifact]
    unchanged: List[DiffArtifact]
    replaced: List[DiffArtifact]
    updated: List[DiffArtifact]

    def __getitem__(self, key): return getattr(self, key)
    def to_dict(self): return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "DiffArtifacts":
        return cls(
            added=[DiffArtifact.from_dict(a) for a in data["added"]],
            removed=[DiffArtifact.from_dict(a) for a in data["removed"]],
            unchanged=[DiffArtifact.from_dict(a) for a in data["unchanged"]],
            replaced=[DiffArtifact.from_dict(a) for a in data["replaced"]],
            updated=[DiffArtifact.from_dict(a) for a in data["updated"]]
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

    def __getitem__(self, key): return getattr(self, key)
    def to_dict(self): return asdict(self)

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
            pull_request=data.get("pull_request")
        )

@dataclass
class FullScanDiffReport:
    before: CommitInfo
    after: CommitInfo
    directDependenciesChanged: bool
    diff_report_url: str
    artifacts: DiffArtifacts

    def __getitem__(self, key): return getattr(self, key)
    def to_dict(self): return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "FullScanDiffReport":
        return cls(
            before=CommitInfo.from_dict(data["before"]),
            after=CommitInfo.from_dict(data["after"]),
            directDependenciesChanged=data["directDependenciesChanged"],
            diff_report_url=data["diff_report_url"],
            artifacts=DiffArtifacts.from_dict(data["artifacts"])
        )

@dataclass
class StreamDiffResponse:
    success: bool
    status: int
    data: Optional[FullScanDiffReport] = None
    message: Optional[str] = None

    def __getitem__(self, key): return getattr(self, key)
    def to_dict(self): return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "StreamDiffResponse":
        return cls(
            success=data["success"],
            status=data["status"],
            message=data.get("message"),
            data=FullScanDiffReport.from_dict(data.get("data")) if data.get("data") else None
        )

@dataclass(kw_only=True)
class SocketArtifactLink:
    topLevelAncestors: List[str]
    artifact: Optional[Dict] = None
    dependencies: Optional[List[str]] = None
    direct: Optional[bool] = None
    manifestFiles: Optional[List[SocketManifestReference]] = None

    def __getitem__(self, key): return getattr(self, key)
    def to_dict(self): return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "SocketArtifactLink":
        manifest_files = data.get("manifestFiles")
        return cls(
            topLevelAncestors=data["topLevelAncestors"],
            artifact=data.get("artifact"),
            dependencies=data.get("dependencies"),
            direct=data.get("direct"),
            manifestFiles=[SocketManifestReference.from_dict(m) for m in manifest_files] if manifest_files else None
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

    def __getitem__(self, key): return getattr(self, key)
    def to_dict(self): return asdict(self)

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
            actionPolicyIndex=data.get("actionPolicyIndex")
        )

@dataclass(kw_only=True)
class SocketArtifact(SocketPURL, SocketArtifactLink):
    id: str
    alerts: Optional[List[SocketAlert]] = field(default_factory=list)
    author: Optional[List[str]] = field(default_factory=list)
    batchIndex: Optional[int] = None
    license: Optional[str] = None
    licenseAttrib: Optional[List[LicenseAttribution]] = field(default_factory=list)
    licenseDetails: Optional[List[LicenseDetail]] = field(default_factory=list)
    score: Optional[SocketScore] = None
    size: Optional[float] = None

    def __getitem__(self, key): return getattr(self, key)
    def to_dict(self): return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "SocketArtifact":
        # First get the base class data
        purl_data = {k: data.get(k) for k in SocketPURL.__dataclass_fields__}
        link_data = {k: data.get(k) for k in SocketArtifactLink.__dataclass_fields__}
        
        # Handle nested types
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
            size=data.get("size")
        )

@dataclass
class FullScanStreamResponse:
    success: bool
    status: int
    artifacts: Optional[Dict[str, SocketArtifact]] = None
    message: Optional[str] = None

    def __getitem__(self, key): return getattr(self, key)
    def to_dict(self): return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "FullScanStreamResponse":
        return cls(
            success=data["success"],
            status=data["status"],
            message=data.get("message"),
            artifacts={
                k: SocketArtifact.from_dict(v) 
                for k, v in data["artifacts"].items()
            } if data.get("artifacts") else None
        )

class FullScans:
    def __init__(self, api):
        self.api = api

    def create_params_string(self, params: dict) -> str:
        param_str = ""

        for name, value in params.items():
            if value:
                if name == "committers" and isinstance(value, list):
                    # Handle committers specially - add multiple params
                    for committer in value:
                        param_str += f"&{name}={committer}"
                else:
                    param_str += f"&{name}={value}"

        param_str = "?" + param_str.lstrip("&")

        return param_str

    def get(self, org_slug: str, params: dict) -> GetFullScanMetadataResponse:
        params_arg = self.create_params_string(params)
        Utils.validate_integration_type(params.get("integration_type", ""))

        path = "orgs/" + org_slug + "/full-scans" + str(params_arg)
        headers = None
        payload = None

        response = self.api.do_request(path=path, headers=headers, payload=payload)

        if response.status_code == 200:
            result = response.json()
            return GetFullScanMetadataResponse.from_dict({
                "success": True,
                "status": 200,
                "data": result
            })

        error_message = response.json().get("error", {}).get("message", "Unknown error")
        log.error(f"Error getting full scan metadata: {response.status_code}, message: {error_message}")
        return GetFullScanMetadataResponse.from_dict({
            "success": False,
            "status": response.status_code,
            "message": error_message
        })

    def post(self, files: list, params: FullScanParams) -> CreateFullScanResponse:
        
        org_slug = str(params.org_slug)
        params_dict = params.to_dict()
        params_dict.pop("org_slug")
        params_arg = self.create_params_string(params_dict)  # Convert params to dict

        path = "orgs/" + org_slug + "/full-scans" + str(params_arg)

        response = self.api.do_request(path=path, method="POST", files=files)
        
        if response.status_code == 201:
            result = response.json()
            return CreateFullScanResponse.from_dict({
                "success": True,
                "status": 201,
                "data": result
            })
        
        log.error(f"Error posting {files} to the Fullscans API")
        error_message = response.json().get("error", {}).get("message", "Unknown error")
        log.error(error_message)

        return CreateFullScanResponse.from_dict({
            "success": False,
            "status": response.status_code,
            "message": error_message
        })

    def delete(self, org_slug: str, full_scan_id: str) -> dict:
        path = "orgs/" + org_slug + "/full-scans/" + full_scan_id

        response = self.api.do_request(path=path, method="DELETE")

        if response.status_code == 200:
            result = response.json()
            return result

        error_message = response.json().get("error", {}).get("message", "Unknown error")
        log.error(f"Error deleting full scan: {response.status_code}, message: {error_message}")
        return {}

    def stream_diff(self, org_slug: str, before: str, after: str) -> StreamDiffResponse:
        path = f"orgs/{org_slug}/full-scans/diff?before={before}&after={after}"

        response = self.api.do_request(path=path, method="GET")

        if response.status_code == 200:
            return StreamDiffResponse.from_dict({
                "success": True,
                "status": 200,
                "data": response.json()
            })

        error_message = response.json().get("error", {}).get("message", "Unknown error")
        log.error(f"Error streaming diff: {response.status_code}, message: {error_message}")
        return StreamDiffResponse.from_dict({
            "success": False,
            "status": response.status_code,
            "message": error_message
        })

    def stream(self, org_slug: str, full_scan_id: str) -> FullScanStreamResponse:
        path = "orgs/" + org_slug + "/full-scans/" + full_scan_id
        response = self.api.do_request(path=path, method="GET")
        
        if response.status_code == 200:
            try:
                stream_str = []
                artifacts = {}
                result = response.text
                result.strip('"')
                result.strip()
                for line in result.split("\n"):
                    if line != '"' and line != "" and line is not None:
                        item = json.loads(line)
                        stream_str.append(item)
                for val in stream_str:
                    artifacts[val["id"]] = val  # Just store the raw dict

                return FullScanStreamResponse.from_dict({
                    "success": True,
                    "status": 200,
                    "artifacts": artifacts  # Let from_dict handle the conversion
                })
            except Exception as e:
                error_message = f"Error parsing stream response: {str(e)}"
                log.error(error_message)
                return FullScanStreamResponse.from_dict({
                    "success": False,
                    "status": response.status_code,
                    "message": error_message
                })

        error_message = response.json().get("error", {}).get("message", "Unknown error")
        log.error(f"Error streaming full scan: {response.status_code}, message: {error_message}")
        return FullScanStreamResponse.from_dict({
            "success": False,
            "status": response.status_code,
            "message": error_message
        })

    def metadata(self, org_slug: str, full_scan_id: str) -> GetFullScanMetadataResponse:
        path = "orgs/" + org_slug + "/full-scans/" + full_scan_id + "/metadata"

        response = self.api.do_request(path=path, method="GET")

        if response.status_code == 200:
            return GetFullScanMetadataResponse.from_dict({
                "success": True,
                "status": 200,
                "data": response.json()
            })

        error_message = response.json().get("error", {}).get("message", "Unknown error")
        log.error(f"Error getting metadata: {response.status_code}, message: {error_message}")
        return GetFullScanMetadataResponse.from_dict({
            "success": False,
            "status": response.status_code,
            "message": error_message
        })



