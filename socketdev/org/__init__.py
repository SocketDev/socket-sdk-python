from typing import TypedDict, Dict
import logging

log = logging.getLogger("socketdev")


class Organization(TypedDict):
    id: str
    name: str
    image: str
    plan: str
    slug: str


class OrganizationsResponse(TypedDict):
    organizations: Dict[str, Organization]
    # Add other fields from the response if needed


class Orgs:
    def __init__(self, api):
        self.api = api

    def get(self, use_types: bool = False) -> OrganizationsResponse:
        path = "organizations"
        response = self.api.do_request(path=path)
        if response.status_code == 200:
            result = response.json()
            if use_types:
                return OrganizationsResponse(result)
            return result
        log.error(f"Error getting organizations: {response.status_code}")
        log.error(response.text)
        return {"organizations": {}}
