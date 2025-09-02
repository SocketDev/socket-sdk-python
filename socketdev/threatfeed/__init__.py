import logging
from urllib.parse import urlencode

log = logging.getLogger("socketdev")


class ThreatFeed:
    def __init__(self, api):
        self.api = api

    def get(self, org_slug: str = None, **kwargs) -> dict:
        """
        Get threat feed items.
        
        Args:
            org_slug: Organization slug (required for the new endpoint)
            **kwargs: Query parameters like per_page, page_cursor, sort, etc.
            
        Returns:
            dict: API response containing threat feed items
        """
        if org_slug:
            # Use the new org-scoped endpoint
            path = f"orgs/{org_slug}/threat-feed"
        else:
            # Use the deprecated global endpoint
            path = "threat-feed"
            
        if kwargs:
            path += "?" + urlencode(kwargs)
            
        response = self.api.do_request(path=path)
        if response.status_code == 200:
            return response.json()
        log.error(f"Error getting threat feed: {response.status_code}")
        log.error(response.text)
        return {"results": [], "nextPage": None}
