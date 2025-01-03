


class OpenAPI:
    def __init__(self, api):
        self.api = api

    def get(self) -> dict:
        path = "openapi"
        response = self.api.do_request(path=path)
        if response.status_code == 200:
            openapi = response.json()
        else:
            openapi = {}
        return openapi
