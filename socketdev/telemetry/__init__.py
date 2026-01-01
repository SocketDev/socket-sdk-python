import logging
import json

log = logging.getLogger("socketdev")


class Telemetry:
    def __init__(self, api):
        self.api = api

    def get_config(self, org_slug: str) -> dict:
        """
        Get telemetry configuration.

        Args:
            org_slug: Organization slug

        Returns:
            dict containing telemetry configuration
        """
        path = f"orgs/{org_slug}/telemetry/config"
        
        response = self.api.do_request(path=path)
        
        if response.status_code == 200:
            return response.json()
        
        log.error(f"Error getting telemetry config: {response.status_code}")
        log.error(response.text)
        return {}

    def update_config(self, org_slug: str, **kwargs) -> dict:
        """
        Update telemetry configuration.

        Args:
            org_slug: Organization slug
            **kwargs: Configuration parameters to update

        Returns:
            dict containing the updated telemetry configuration
        """
        path = f"orgs/{org_slug}/telemetry/config"
        payload = json.dumps(kwargs) if kwargs else "{}"
        
        response = self.api.do_request(path=path, method="PUT", payload=payload)
        
        if response.status_code == 200:
            return response.json()
        
        log.error(f"Error updating telemetry config: {response.status_code}")
        log.error(response.text)
        return {}
