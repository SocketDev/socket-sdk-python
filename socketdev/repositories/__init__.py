import socketdev


class Repositories:
    @staticmethod
    def get() -> dict:
        path = f"repo/list"
        response = socketdev.do_request(path=path)
        if response.status_code == 200:
            repos = response.json()
        else:
            repos = {}
        return repos
