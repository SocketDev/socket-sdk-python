import socketdev
from typing import TypedDict


class Repo(TypedDict):
    name: str
    description: str
    homepage: str
    visibility: str
    archived: bool
    default_branch: str


class Repositories:
    @staticmethod
    def get(org_slug: str) -> dict:
        path = f"orgs/{org_slug}/repos"
        response = socketdev.do_request(path=path)
        if response.status_code == 200:
            repos = response.json()
        else:
            repos = {}
        return repos

    @staticmethod
    def post(org_slug: str, body: Repo) -> dict:
        path = f"orgs/{org_slug}/repos"
        response = socketdev.do_request(path=path, method="POST", payload=body)
        if response.status_code == 200:
            repos = response.json()
        else:
            repos = {}
        return repos

    @staticmethod
    def update(org_slug: str, body: Repo) -> dict:
        path = f"orgs/{org_slug}/repos"
        response = socketdev.do_request(path=path, method="POST", payload=body)
        if response.status_code == 200:
            repos = response.json()
        else:
            repos = {}
        return repos

    @staticmethod
    def repo(org_slug: str, repo_id: str) -> dict:
        path = f"orgs/{org_slug}/repos/{repo_id}"
        response = socketdev.do_request(path=path)
        if response.status_code == 200:
            repos = response.json()
        else:
            repos = {}
        return repos
