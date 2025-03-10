import json
import logging
from typing import Optional, Union
from dataclasses import dataclass, asdict
from socketdev.exceptions import APIFailure

log = logging.getLogger("socketdev")


@dataclass
class RepositoryInfo:
    id: str
    created_at: str  # Could be datetime if we want to parse it
    updated_at: str  # Could be datetime if we want to parse it
    head_full_scan_id: str
    name: str
    description: str
    homepage: str
    visibility: str
    archived: bool
    default_branch: str
    slug: Optional[str] = None

    def __getitem__(self, key):
        return getattr(self, key)

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "RepositoryInfo":
        return cls(
            id=data["id"],
            created_at=data["created_at"],
            updated_at=data["updated_at"],
            head_full_scan_id=data["head_full_scan_id"],
            name=data["name"],
            description=data["description"],
            homepage=data["homepage"],
            visibility=data["visibility"],
            archived=data["archived"],
            default_branch=data["default_branch"],
            slug=data.get("slug"),
        )


@dataclass
class GetRepoResponse:
    success: bool
    status: int
    data: Optional[RepositoryInfo] = None
    message: Optional[str] = None

    def __getitem__(self, key):
        return getattr(self, key)

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "GetRepoResponse":
        return cls(
            success=data["success"],
            status=data["status"],
            message=data.get("message"),
            data=RepositoryInfo.from_dict(data.get("data")) if data.get("data") else None,
        )


class Repos:
    def __init__(self, api):
        self.api = api

    def get(self, org_slug: str, **kwargs) -> dict[str, list[dict] | int]:
        query_params = kwargs
        path = "orgs/" + org_slug + "/repos"

        if query_params:  # Only add query string if we have parameters
            path += "?"
            for param in query_params:
                value = query_params[param]
                path += f"{param}={value}&"
            path = path.rstrip("&")

        try:
            response = self.api.do_request(path=path)
            if response.status_code == 200:
                raw_result = response.json()
                per_page = int(query_params.get("per_page", 30))

                # TEMPORARY: Handle pagination edge case where API returns nextPage=1 even when no more results exist
                if raw_result["nextPage"] != 0 and len(raw_result["results"]) < per_page:
                    raw_result["nextPage"] = 0

                return raw_result
        except APIFailure as e:
            log.error(f"Socket SDK: API failure while getting repositories {e}")
            raise
        except Exception as e:
            log.error(f"Socket SDK: Unexpected error while getting repositories {e}")
            raise

        return {}

    def repo(self, org_slug: str, repo_name: str, use_types: bool = False) -> Union[dict, GetRepoResponse]:
        path = f"orgs/{org_slug}/repos/{repo_name}"
        try:
            response = self.api.do_request(path=path)
            if response.status_code == 200:
                result = response.json()
                if use_types:
                    return GetRepoResponse.from_dict({"success": True, "status": 200, "data": result})
                return result
        except APIFailure as e:
            log.error(f"Socket SDK: API failure while getting repository {e}")
            raise
        except Exception as e:
            log.error(f"Socket SDK: Unexpected error while getting repository {e}")
            raise

        if use_types:
            error_message = response.json().get("error", {}).get("message", "Unknown error")
            return GetRepoResponse.from_dict(
                {"success": False, "status": response.status_code, "message": error_message}
            )
        return {}

    def delete(self, org_slug: str, name: str) -> dict:
        path = f"orgs/{org_slug}/repos/{name}"
        try:
            response = self.api.do_request(path=path, method="DELETE")
            if response.status_code == 200:
                return response.json()
        except APIFailure as e:
            log.error(f"Socket SDK: API failure while deleting repository {e}")
            raise
        except Exception as e:
            log.error(f"Socket SDK: Unexpected error while deleting repository {e}")
            raise

        return {}

    def post(self, org_slug: str, **kwargs) -> dict:
        params = {}
        if kwargs:
            for key, val in kwargs.items():
                params[key] = val
        if len(params) == 0:
            return {}

        path = "orgs/" + org_slug + "/repos"
        payload = json.dumps(params)
        try:
            response = self.api.do_request(path=path, method="POST", payload=payload)
            if response.status_code == 201:
                return response.json()
        except APIFailure as e:
            log.error(f"Socket SDK: API failure while creating repository {e}")
            raise
        except Exception as e:
            log.error(f"Socket SDK: Unexpected error while creating repository {e}")
            raise

        return {}

    def update(self, org_slug: str, repo_name: str, **kwargs) -> dict:
        params = {}
        if kwargs:
            for key, val in kwargs.items():
                params[key] = val
        if len(params) == 0:
            return {}

        path = f"orgs/{org_slug}/repos/{repo_name}"
        payload = json.dumps(params)
        try:
            response = self.api.do_request(path=path, method="POST", payload=payload)
            if response.status_code == 200:
                return response.json()
        except APIFailure as e:
            log.error(f"Socket SDK: API failure while updating repository {e}")
            raise
        except Exception as e:
            log.error(f"Socket SDK: Unexpected error while updating repository {e}")
            raise

        return {}
