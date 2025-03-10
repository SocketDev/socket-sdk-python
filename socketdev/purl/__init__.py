import json
from socketdev.exceptions import APIFailure
import logging

log = logging.getLogger("socketdev")


class Purl:
    def __init__(self, api):
        self.api = api

    def post(self, license: str = "true", components: list = []) -> list:
        path = "purl?" + "license=" + license
        components = {"components": components}
        components = json.dumps(components)

        try:
            response = self.api.do_request(path=path, payload=components, method="POST")
            if response.status_code == 200:
                purl = []
                result = response.text.strip('"').strip()
                for line in result.split("\n"):
                    if line and line != '"':
                        try:
                            item = json.loads(line)
                            purl.append(item)
                        except json.JSONDecodeError:
                            continue
                return purl
        except APIFailure as e:
            log.error(f"Socket SDK: API failure while posting to the Purl API {e}")
            raise
        except Exception as e:
            log.error(f"Socket SDK: Unexpected error while posting to the Purl API {e}")
            raise

        return []
