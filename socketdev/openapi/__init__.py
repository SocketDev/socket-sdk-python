import socketdev


class OpenAPI:
    @staticmethod
    def get() -> dict:
        path = "openapi"
        response = socketdev.do_request(path=path)
        if response.status_code == 200:
            openapi = response.json()
        else:
            openapi = {}
        return openapi
