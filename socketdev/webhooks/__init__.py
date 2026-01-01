import logging
import json
from urllib.parse import urlencode

log = logging.getLogger("socketdev")


class Webhooks:
    def __init__(self, api):
        self.api = api

    def list(self, org_slug: str, **query_params) -> dict:
        """
        List webhooks.

        Args:
            org_slug: Organization slug
            **query_params: Optional query parameters

        Returns:
            dict containing list of webhooks
        """
        path = f"orgs/{org_slug}/webhooks"
        if query_params:
            path += "?" + urlencode(query_params)
        
        response = self.api.do_request(path=path)
        
        if response.status_code == 200:
            return response.json()
        
        log.error(f"Error listing webhooks: {response.status_code}")
        log.error(response.text)
        return {}

    def create(self, org_slug: str, **kwargs) -> dict:
        """
        Create a new webhook.

        Args:
            org_slug: Organization slug
            **kwargs: Webhook configuration parameters

        Returns:
            dict containing the created webhook
        """
        path = f"orgs/{org_slug}/webhooks"
        payload = json.dumps(kwargs) if kwargs else "{}"
        
        response = self.api.do_request(path=path, method="POST", payload=payload)
        
        if response.status_code in (200, 201):
            return response.json()
        
        log.error(f"Error creating webhook: {response.status_code}")
        log.error(response.text)
        return {}

    def get(self, org_slug: str, webhook_id: str) -> dict:
        """
        Get a specific webhook.

        Args:
            org_slug: Organization slug
            webhook_id: Webhook ID

        Returns:
            dict containing webhook details
        """
        path = f"orgs/{org_slug}/webhooks/{webhook_id}"
        
        response = self.api.do_request(path=path)
        
        if response.status_code == 200:
            return response.json()
        
        log.error(f"Error getting webhook: {response.status_code}")
        log.error(response.text)
        return {}

    def update(self, org_slug: str, webhook_id: str, **kwargs) -> dict:
        """
        Update a webhook.

        Args:
            org_slug: Organization slug
            webhook_id: Webhook ID
            **kwargs: Webhook configuration parameters to update

        Returns:
            dict containing the updated webhook
        """
        path = f"orgs/{org_slug}/webhooks/{webhook_id}"
        payload = json.dumps(kwargs) if kwargs else "{}"
        
        response = self.api.do_request(path=path, method="PUT", payload=payload)
        
        if response.status_code == 200:
            return response.json()
        
        log.error(f"Error updating webhook: {response.status_code}")
        log.error(response.text)
        return {}

    def delete(self, org_slug: str, webhook_id: str) -> dict:
        """
        Delete a webhook.

        Args:
            org_slug: Organization slug
            webhook_id: Webhook ID

        Returns:
            dict containing the deletion response
        """
        path = f"orgs/{org_slug}/webhooks/{webhook_id}"
        
        response = self.api.do_request(path=path, method="DELETE")
        
        if response.status_code == 200:
            return response.json()
        
        log.error(f"Error deleting webhook: {response.status_code}")
        log.error(response.text)
        return {}
