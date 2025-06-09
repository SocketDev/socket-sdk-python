from typing import TypedDict, Union
import logging

log = logging.getLogger("socketdev")


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

    def list(self, use_types: bool = False) -> Union[dict, list[Repo]]:
        path = "repos"
        response = self.api.do_request(path=path)
        if response.status_code == 200:
            result = response.json()
            if use_types:
                return [Repo(repo) for repo in result]
            return result

        log.error(f"Error listing repositories: {response.status_code}")
        log.error(response.text)
        return []
