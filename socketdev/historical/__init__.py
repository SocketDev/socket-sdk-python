import logging
from urllib.parse import urlencode

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

        response = self.api.do_request(path=path)
        if response.status_code == 200:
            return response.json()

        log.error(f"Error getting historical alerts: {response.status_code}")
        log.error(response.text)
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

        response = self.api.do_request(path=path)
        if response.status_code == 200:
            return response.json()

        log.error(f"Error getting historical trend: {response.status_code}")
        log.error(response.text)
        return {}
