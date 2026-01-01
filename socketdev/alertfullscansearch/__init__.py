import logging
from urllib.parse import urlencode

log = logging.getLogger("socketdev")


class AlertFullScanSearch:
    def __init__(self, api):
        self.api = api

    def search(self, org_slug: str, **query_params) -> dict:
        """
        Search alerts across full scans.

        Args:
            org_slug: Organization slug
            **query_params: Optional query parameters for filtering

        Returns:
            dict containing search results
        """
        path = f"orgs/{org_slug}/alert-full-scan-search"
        if query_params:
            path += "?" + urlencode(query_params)
        
        response = self.api.do_request(path=path)
        
        if response.status_code == 200:
            return response.json()
        
        log.error(f"Error searching alerts: {response.status_code}")
        log.error(response.text)
        return {}
