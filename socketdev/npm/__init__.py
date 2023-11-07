import socketdev


class NPM:
    @staticmethod
    def issues(package: str, version: str) -> list:
        path = f"npm/{package}/{version}/issues"
        response = socketdev.do_request(path=path)
        issues = []
        if response.status_code == 200:
            issues = response.json()
        return issues

    @staticmethod
    def score(package: str, version: str) -> list:
        path = f"npm/{package}/{version}/score"
        response = socketdev.do_request(path=path)
        issues = []
        if response.status_code == 200:
            issues = response.json()
        return issues
