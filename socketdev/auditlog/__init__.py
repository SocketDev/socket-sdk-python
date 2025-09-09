import logging

log = logging.getLogger("socketdev")


class AuditLog:
    def __init__(self, api):
        self.api = api

    def get(self, org_slug: str, **kwargs) -> dict:
        """
        Get audit log entries for an organization.
        
        Args:
            org_slug: Organization slug
            **kwargs: Query parameters like limit, cursor, etc.
            
        Returns:
            dict: API response containing audit log entries
        """
        path = f"orgs/{org_slug}/audit-log"
        if kwargs:
            from urllib.parse import urlencode
            path += "?" + urlencode(kwargs)
        response = self.api.do_request(path=path)
        if response.status_code == 200:
            return response.json()
        log.error(f"Error getting audit log: {response.status_code}")
        log.error(response.text)
        return {"results": []}
