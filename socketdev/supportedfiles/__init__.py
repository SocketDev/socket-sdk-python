import logging

log = logging.getLogger("socketdev")


class SupportedFiles:
    def __init__(self, api):
        self.api = api

    def get(self, org_slug: str) -> dict:
        """
        Get list of supported manifest file types.

        Args:
            org_slug: Organization slug

        Returns:
            dict containing list of supported file types
        """
        path = f"orgs/{org_slug}/supported-files"
        
        response = self.api.do_request(path=path)
        
        if response.status_code == 200:
            return response.json()
        
        log.error(f"Error getting supported files: {response.status_code}")
        log.error(response.text)
        return {}
