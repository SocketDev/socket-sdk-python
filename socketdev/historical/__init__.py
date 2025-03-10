import logging
from urllib.parse import urlencode
from socketdev.exceptions import APIFailure

log = logging.getLogger("socketdev")


class Historical:
    def __init__(self, api):
        self.api = api

    def list(self, org_slug: str, query_params: dict = None) -> dict:
        """Get historical alerts list for an organization.

        Args:
            org_slug: Organization slug
            query_params: Optional dictionary of query parameters
        """
        path = f"orgs/{org_slug}/alerts/historical"
        if query_params:
            path += "?" + urlencode(query_params)

        try:
            response = self.api.do_request(path=path)
            if response.status_code == 200:
                return response.json()
        except APIFailure as e:
            log.error(f"Socket SDK: API failure while getting historical alerts {e}")
            raise
        except Exception as e:
            log.error(f"Socket SDK: Unexpected error while getting historical alerts {e}")
            raise

        return {}

    def trend(self, org_slug: str, query_params: dict = None) -> dict:
        """Get historical alerts trend data for an organization.

        Args:
            org_slug: Organization slug
            query_params: Optional dictionary of query parameters
        """
        path = f"orgs/{org_slug}/alerts/historical/trend"
        if query_params:
            path += "?" + urlencode(query_params)

        try:
            response = self.api.do_request(path=path)
            if response.status_code == 200:
                return response.json()
        except APIFailure as e:
            log.error(f"Socket SDK: API failure while getting historical trend {e}")
            raise
        except Exception as e:
            log.error(f"Socket SDK: Unexpected error while getting historical trend {e}")
            raise

        return {}
