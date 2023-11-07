import socketdev


class Settings:
    @staticmethod
    def get() -> dict:
        path = f"settings"
        response = socketdev.do_request(path=path)
        if response.status_code == 200:
            settings = response.json()
        else:
            settings = {}
        return settings
