import logging
from enum import Enum
from typing import Dict, Optional
from dataclasses import dataclass, asdict
log = logging.getLogger("socketdev")

class SecurityAction(str, Enum):
    DEFER = 'defer'
    ERROR = 'error'
    WARN = 'warn'
    MONITOR = 'monitor'
    IGNORE = 'ignore'

@dataclass
class SecurityPolicyRule:
    action: SecurityAction

    def __getitem__(self, key): return getattr(self, key)
    def to_dict(self): return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "SecurityPolicyRule":
        return cls(
            action=SecurityAction(data["action"])
        )

@dataclass
class OrgSecurityPolicyResponse:
    success: bool
    status: int
    securityPolicyRules: Optional[Dict[str, SecurityPolicyRule]] = None
    message: Optional[str] = None

    def __getitem__(self, key): return getattr(self, key)
    def to_dict(self): return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "OrgSecurityPolicyResponse":
        return cls(
            securityPolicyRules={
                k: SecurityPolicyRule.from_dict(v) 
                for k, v in data["securityPolicyRules"].items()
            } if data.get("securityPolicyRules") else None,
            success=data["success"],
            status=data["status"],
            message=data.get("message")
        )

class Settings:
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

    def get(self, org_slug: str, custom_rules_only: bool = False) -> OrgSecurityPolicyResponse:
        path = f"orgs/{org_slug}/settings/security-policy"
        params = {"custom_rules_only": custom_rules_only}
        params_args = self.create_params_string(params) if custom_rules_only else ""
        path += params_args
        response = self.api.do_request(path=path, method="GET")

        if response.status_code == 200:
            rules = response.json()
            return OrgSecurityPolicyResponse.from_dict({
                "securityPolicyRules": rules.get("securityPolicyRules", {}),
                "success": True,
                "status": 200
            })
        else:
            error_message = response.json().get("error", {}).get("message", "Unknown error")
            log.error(f"Failed to get security policy: {response.status_code}, message: {error_message}")
            return OrgSecurityPolicyResponse.from_dict({
                "securityPolicyRules": {},
                "success": False,
                "status": response.status_code,
                "message": error_message
            })
