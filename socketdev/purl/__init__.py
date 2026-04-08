import json
import urllib.parse
import warnings
from socketdev.log import log
from ..core.dedupe import Dedupe


class Purl:
    def __init__(self, api):
        self.api = api

    def post(
        self,
        license: str = "false",
        components: list = None,
        org_slug: str = None,
        **kwargs,
    ) -> list:
        if org_slug is None:
            warnings.warn(
                "Calling purl.post() without org_slug uses the deprecated POST /v0/purl endpoint. "
                "Pass org_slug to migrate to POST /v0/orgs/{org_slug}/purl.",
                DeprecationWarning,
                stacklevel=2,
            )
        path = f"orgs/{org_slug}/purl?" if org_slug else "purl?"
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
            purl_deduped = Dedupe.dedupe(purl, batched=True)
            return purl_deduped

        log.error(f"Error posting {components} to the Purl API: {response.status_code}")
        log.error(response.text)
        return []
