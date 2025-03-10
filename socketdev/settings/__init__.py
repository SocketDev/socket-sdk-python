import logging
from enum import Enum
from typing import Dict, Optional, Union
from dataclasses import dataclass, asdict
from socketdev.exceptions import APIFailure

log = logging.getLogger("socketdev")


class SecurityAction(str, Enum):
    DEFER = "defer"
    ERROR = "error"
    WARN = "warn"
    MONITOR = "monitor"
    IGNORE = "ignore"


@dataclass
class SecurityPolicyRule:
    action: SecurityAction

    def __getitem__(self, key):
        return getattr(self, key)

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "SecurityPolicyRule":
        return cls(action=SecurityAction(data["action"]))


@dataclass
class OrgSecurityPolicyResponse:
    success: bool
    status: int
    securityPolicyRules: Optional[Dict[str, SecurityPolicyRule]] = None
    message: Optional[str] = None

    def __getitem__(self, key):
        return getattr(self, key)

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "OrgSecurityPolicyResponse":
        return cls(
            securityPolicyRules={k: SecurityPolicyRule.from_dict(v) for k, v in data["securityPolicyRules"].items()}
            if data.get("securityPolicyRules")
            else None,
            success=data["success"],
            status=data["status"],
            message=data.get("message"),
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

    def get(
        self, org_slug: str, custom_rules_only: bool = False, use_types: bool = False
    ) -> Union[dict, OrgSecurityPolicyResponse]:
        path = f"orgs/{org_slug}/settings/security-policy"
        params = {"custom_rules_only": custom_rules_only}
        params_args = self.create_params_string(params) if custom_rules_only else ""
        path += params_args

        try:
            response = self.api.do_request(path=path, method="GET")
            if response.status_code == 200:
                rules = response.json()
                if use_types:
                    return OrgSecurityPolicyResponse.from_dict(
                        {"securityPolicyRules": rules.get("securityPolicyRules", {}), "success": True, "status": 200}
                    )
                return rules
        except APIFailure as e:
            log.error(f"Socket SDK: API failure while getting security policy {e}")
            raise
        except Exception as e:
            log.error(f"Socket SDK: Unexpected error while getting security policy {e}")
            raise

        if use_types:
            return OrgSecurityPolicyResponse.from_dict(
                {
                    "securityPolicyRules": {},
                    "success": False,
                    "status": response.status_code,
                    "message": "Unknown error",
                }
            )
        return {}

    def integration_events(self, org_slug: str, integration_id: str) -> dict:
        """Get integration events for a specific integration.

        Args:
            org_slug: Organization slug
            integration_id: Integration ID
        """
        path = f"orgs/{org_slug}/settings/integrations/{integration_id}"
        try:
            response = self.api.do_request(path=path)
            if response.status_code == 200:
                return response.json()
        except APIFailure as e:
            log.error(f"Socket SDK: API failure while getting integration events {e}")
            raise
        except Exception as e:
            log.error(f"Socket SDK: Unexpected error while getting integration events {e}")
            raise

        return {}

    def get_license_policy(self, org_slug: str) -> dict:
        """Get license policy settings for an organization.

        Args:
            org_slug: Organization slug
        """
        path = f"orgs/{org_slug}/settings/license-policy"
        try:
            response = self.api.do_request(path=path)
            if response.status_code == 200:
                return response.json()
        except APIFailure as e:
            log.error(f"Socket SDK: API failure while getting license policy {e}")
            raise
        except Exception as e:
            log.error(f"Socket SDK: Unexpected error while getting license policy {e}")
            raise

        return {}

    def update_security_policy(self, org_slug: str, body: dict, custom_rules_only: bool = False) -> dict:
        """Update security policy settings for an organization.

        Args:
            org_slug: Organization slug
            body: Security policy configuration to update
            custom_rules_only: Optional flag to update only custom rules
        """
        path = f"orgs/{org_slug}/settings/security-policy"
        if custom_rules_only:
            path += "?custom_rules_only=true"

        try:
            response = self.api.do_request(path=path, method="POST", payload=body)
            if response.status_code == 200:
                return response.json()
        except APIFailure as e:
            log.error(f"Socket SDK: API failure while updating security policy {e}")
            raise
        except Exception as e:
            log.error(f"Socket SDK: Unexpected error while updating security policy {e}")
            raise

        return {}

    def update_license_policy(self, org_slug: str, body: dict, merge_update: bool = False) -> dict:
        """Update license policy settings for an organization.

        Args:
            org_slug: Organization slug
            body: License policy configuration to update
            merge_update: Optional flag to merge updates instead of replacing (defaults to False)
        """
        path = f"orgs/{org_slug}/settings/license-policy?merge_update={str(merge_update).lower()}"

        try:
            response = self.api.do_request(path=path, method="POST", payload=body)
            if response.status_code == 200:
                return response.json()
        except APIFailure as e:
            log.error(f"Socket SDK: API failure while updating license policy {e}")
            raise
        except Exception as e:
            log.error(f"Socket SDK: Unexpected error while updating license policy {e}")
            raise

        return {}
