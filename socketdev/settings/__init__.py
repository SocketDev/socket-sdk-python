import json

import socketdev


class Settings:
    @staticmethod
    def get(org_id: str) -> dict:
        settings = {}
        path = "settings"
        payload = [{"organization": org_id}]
        response = socketdev.do_request(path=path, method="POST", payload=json.dumps(payload))

        if response.status_code != 200:
            return settings

        settings = response.json()
        return settings
