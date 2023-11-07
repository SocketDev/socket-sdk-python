import socketdev


class Orgs:
    @staticmethod
    def get() -> dict:
        path = "organizations"
        headers = None
        payload = None

        response = socketdev.do_request(
            path=path,
            headers=headers,
            payload=payload
        )
        if response.status_code == 200:
            result = response.json()
        else:
            result = {}
        return result
