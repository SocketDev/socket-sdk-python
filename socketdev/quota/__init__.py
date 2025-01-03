
class Quota:
    def __init__(self, api):
        self.api = api

    def get(self) -> dict:
        path = "quota"
        response = self.api.do_request(path=path)
        if response.status_code == 200:
            quota = response.json()
        else:
            quota = {}
        return quota
