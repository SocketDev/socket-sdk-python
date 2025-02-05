import json


class Purl:
    def __init__(self, api):
        self.api = api

    def post(self, license: str = "true", components: list = []) -> dict:
        path = "purl?" + "license=" + license
        components = {"components": components}
        components = json.dumps(components)

        response = self.api.do_request(path=path, payload=components, method="POST")
        if response.status_code == 200:
            purl = []
            purl_dict = {}
            result = response.text
            result.strip('"')
            result.strip()
            for line in result.split("\n"):
                if line != '"' and line != "" and line is not None:
                    item = json.loads(line)
                    purl.append(item)
            for val in purl:
                purl_dict[val["id"]] = val
        else:
            purl_dict = {}
            print(f"Error posting {components} to the Purl API")
            print(response.text)

        return purl_dict
