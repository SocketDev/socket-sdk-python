import socketdev


class Quota:
    @staticmethod
    def get() -> dict:
        path = "quota"
        response = socketdev.do_request(path=path)
        if response.status_code == 200:
            quota = response.json()
        else:
            quota = {}
        return quota
