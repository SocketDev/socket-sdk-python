from typing import TypedDict


class Repo(TypedDict):
    name: str
    description: str
    homepage: str
    visibility: str
    archived: bool
    default_branch: str


class Repositories:
    def __init__(self, api):
        self.api = api

    def list(self) -> dict:
        path = "repos"
        response = self.api.do_request(path=path)
        if response.status_code == 200:
            repos = response.json()
        else:
            repos = {}
        return repos
