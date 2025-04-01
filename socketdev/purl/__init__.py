import json
import urllib.parse
from socketdev.log import log


class Purl:
    def __init__(self, api):
        self.api = api

    def post(self, license: str = "false", components: list = None, **kwargs) -> list:
        path = "purl?"
        if components is None:
            components = []
        purls = {"components": components}
        purls = json.dumps(purls)
        query_args = {
            "license": license,
        }
        if kwargs:
            query_args.update(kwargs)
        params = urllib.parse.urlencode(query_args)
        path += params
        response = self.api.do_request(path=path, payload=purls, method="POST")
        if response.status_code == 200:
            purl = []
            result = response.text
            result = result.strip('"').strip()
            for line in result.split("\n"):
                if line and line != '"':
                    try:
                        item = json.loads(line)
                        purl.append(item)
                    except json.JSONDecodeError:
                        continue
            return purl

        log.error(f"Error posting {components} to the Purl API: {response.status_code}")
        print(response.text)
        return []
