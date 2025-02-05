from typing import TypedDict, Dict

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

    def get(self) -> OrganizationsResponse:
        path = "organizations"
        response = self.api.do_request(path=path)
        if response.status_code == 200:
            return response.json()  # Return the full response
        else:
            return {"organizations": {}}  # Return an empty structure