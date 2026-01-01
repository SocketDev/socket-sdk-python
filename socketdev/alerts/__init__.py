import logging
from urllib.parse import urlencode

log = logging.getLogger("socketdev")


class Alerts:
    def __init__(self, api):
        self.api = api

    def get(self, org_slug: str, **query_params) -> dict:
        """
        Get alerts for an organization.

        Args:
            org_slug: Organization slug
            **query_params: Optional query parameters for filtering

        Returns:
            dict containing alerts data
        """
        path = f"orgs/{org_slug}/alerts"
        if query_params:
            path += "?" + urlencode(query_params)
        
        response = self.api.do_request(path=path)
        
        if response.status_code == 200:
            return response.json()
        
        log.error(f"Error getting alerts: {response.status_code}")
        log.error(response.text)
        return {}
