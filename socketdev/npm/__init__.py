


class NPM:
    def __init__(self, api):
        self.api = api

    def issues(self, package: str, version: str) -> list:
        path = f"npm/{package}/{version}/issues"
        response = self.api.do_request(path=path)
        issues = []
        if response.status_code == 200:
            issues = response.json()
        return issues

    def score(self, package: str, version: str) -> list:
        path = f"npm/{package}/{version}/score"
        response = self.api.do_request(path=path)
        issues = []
        if response.status_code == 200:
            issues = response.json()
        return issues
