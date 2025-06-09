import json
import logging
from typing import Optional, Union
from dataclasses import dataclass, asdict

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
            created_at=data.get("created_at", ""),
            updated_at=data.get("updated_at", ""),
            head_full_scan_id=data.get("head_full_scan_id", ""),
            name=data["name"],
            description=data.get("description", ""),
            homepage=data.get("homepage", ""),
            visibility=data.get("visibility", "private"),
            archived=data.get("archived", False),
            default_branch=data.get("default_branch", "main"),
            slug=data["slug"]
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

        response = self.api.do_request(path=path)

        if response.status_code == 200:
            raw_result = response.json()
            per_page = int(query_params.get("per_page", 30))

            # TEMPORARY: Handle pagination edge case where API returns nextPage=1 even when no more results exist
            if raw_result["nextPage"] != 0 and len(raw_result["results"]) < per_page:
                raw_result["nextPage"] = 0

            return raw_result

        error_message = response.json().get("error", {}).get("message", "Unknown error")
        log.error(f"Error getting repositories: {response.status_code}, message: {error_message}")
        return {}

    def repo(self, org_slug: str, repo_name: str, use_types: bool = False) -> Union[dict, GetRepoResponse]:
        path = f"orgs/{org_slug}/repos/{repo_name}"
        response = self.api.do_request(path=path)

        if response.status_code == 200:
            result = response.json()
            if use_types:
                return GetRepoResponse.from_dict({"success": True, "status": 200, "data": result})
            return result

        error_message = response.json().get("error", {}).get("message", "Unknown error")
        log.error(f"Failed to get repository: {response.status_code}, message: {error_message}")
        if use_types:
            return GetRepoResponse.from_dict(
                {"success": False, "status": response.status_code, "message": error_message}
            )
        return {}

    def delete(self, org_slug: str, name: str) -> dict:
        path = f"orgs/{org_slug}/repos/{name}"
        response = self.api.do_request(path=path, method="DELETE")

        if response.status_code == 200:
            return response.json()

        error_message = response.json().get("error", {}).get("message", "Unknown error")
        log.error(f"Error deleting repository: {response.status_code}, message: {error_message}")
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
        response = self.api.do_request(path=path, method="POST", payload=payload)

        if response.status_code == 201:
            return response.json()

        error_message = response.json().get("error", {}).get("message", "Unknown error")
        log.error(f"Error creating repository: {response.status_code}, message: {error_message}")
        return {}

    def update(self, org_slug: str, repo_name: str, **kwargs) -> dict:
        params = {}
        if kwargs:
            for key, val in kwargs.keys():
                params[key] = val
        if len(params) == 0:
            return {}

        path = f"orgs/{org_slug}/repos/{repo_name}"
        payload = json.dumps(params)
        response = self.api.do_request(path=path, method="POST", payload=payload)

        if response.status_code == 200:
            return response.json()

        error_message = response.json().get("error", {}).get("message", "Unknown error")
        log.error(f"Error updating repository: {response.status_code}, message: {error_message}")
        return {}
