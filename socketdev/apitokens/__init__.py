import logging
import json

log = logging.getLogger("socketdev")


class ApiTokens:
    def __init__(self, api):
        self.api = api

    def create(self, org_slug: str, **kwargs) -> dict:
        """
        Create a new API token.
        
        Args:
            org_slug: Organization slug
            **kwargs: Token configuration parameters
            
        Returns:
            dict: API response containing the created token details
        """
        path = f"orgs/{org_slug}/api-tokens"
        payload = json.dumps(kwargs) if kwargs else "{}"
        response = self.api.do_request(path=path, method="POST", payload=payload)
        if response.status_code == 201:
            return response.json()
        log.error(f"Error creating API token: {response.status_code}")
        log.error(response.text)
        return {}

    def update(self, org_slug: str, **kwargs) -> dict:
        """
        Update an API token.
        
        Args:
            org_slug: Organization slug
            **kwargs: Token update parameters
            
        Returns:
            dict: API response containing the updated token details
        """
        path = f"orgs/{org_slug}/api-tokens/update"
        payload = json.dumps(kwargs) if kwargs else "{}"
        response = self.api.do_request(path=path, method="POST", payload=payload)
        if response.status_code == 200:
            return response.json()
        log.error(f"Error updating API token: {response.status_code}")
        log.error(response.text)
        return {}

    def rotate(self, org_slug: str, **kwargs) -> dict:
        """
        Rotate an API token.
        
        Args:
            org_slug: Organization slug
            **kwargs: Token rotation parameters
            
        Returns:
            dict: API response containing the rotated token details
        """
        path = f"orgs/{org_slug}/api-tokens/rotate"
        payload = json.dumps(kwargs) if kwargs else "{}"
        response = self.api.do_request(path=path, method="POST", payload=payload)
        if response.status_code == 200:
            return response.json()
        log.error(f"Error rotating API token: {response.status_code}")
        log.error(response.text)
        return {}

    def revoke(self, org_slug: str, **kwargs) -> dict:
        """
        Revoke an API token.
        
        Args:
            org_slug: Organization slug
            **kwargs: Token revocation parameters
            
        Returns:
            dict: API response confirming token revocation
        """
        path = f"orgs/{org_slug}/api-tokens/revoke"
        payload = json.dumps(kwargs) if kwargs else "{}"
        response = self.api.do_request(path=path, method="POST", payload=payload)
        if response.status_code == 200:
            return response.json()
        log.error(f"Error revoking API token: {response.status_code}")
        log.error(response.text)
        return {}
