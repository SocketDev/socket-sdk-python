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

    def list(self, org_slug: str, **kwargs) -> dict:
        """
        List API tokens for an organization.
        
        Args:
            org_slug: Organization slug
            **kwargs: Query parameters
            
        Returns:
            dict: API response containing list of tokens
        """
        path = f"orgs/{org_slug}/api-tokens"
        query_params = {}
        if kwargs:
            query_params.update(kwargs)
        
        if query_params:
            from urllib.parse import urlencode
            path += "?" + urlencode(query_params)
        response = self.api.do_request(path=path, method="GET")
        if response.status_code == 200:
            return response.json()
        log.error(f"Error listing API tokens: {response.status_code}")
        log.error(response.text)
        return {}

    def update(self, org_slug: str, token_id: str = None, **kwargs) -> dict:
        """
        Update an API token.
        
        Args:
            org_slug: Organization slug
            token_id: Token ID to update (optional, can be in kwargs)
            **kwargs: Token update parameters
            
        Returns:
            dict: API response containing the updated token details
        """
        # Extract token_id from kwargs if not provided as parameter
        if token_id is None and 'token_id' in kwargs:
            token_id = kwargs.pop('token_id')
        
        if token_id:
            path = f"orgs/{org_slug}/api-tokens/{token_id}"
            method = "PUT"
        else:
            path = f"orgs/{org_slug}/api-tokens/update"
            method = "POST"
            
        payload = json.dumps(kwargs) if kwargs else "{}"
        response = self.api.do_request(path=path, method=method, payload=payload)
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
