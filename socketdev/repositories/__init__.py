import socketdev
from typing import TypedDict


class Repo(TypedDict):
    name: str
    description: str
    homepage: str
    visibility: str
    archived: bool
    default_branch: str


# remove methods except for list, use old endpoint for list
class Repositories:
    @staticmethod
    def list() -> dict:
        path = "repos"
        response = socketdev.do_request(path=path)
        if response.status_code == 200:
            repos = response.json()
        else:
            repos = {}
        return repos
