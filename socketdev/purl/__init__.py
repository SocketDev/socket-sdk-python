import json


class Purl:
    def __init__(self, api):
        self.api = api

    def post(self, license: str = "true", components: list = []) -> list:
        path = "purl?" + "license=" + license
        components = {"components": components}
        components = json.dumps(components)

        response = self.api.do_request(path=path, payload=components, method="POST")
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
