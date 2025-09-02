import logging
import json
from urllib.parse import urlencode

log = logging.getLogger("socketdev")


class AlertTypes:
    def __init__(self, api):
        self.api = api

    def get(self, alert_types: list = None, language: str = "en-US", **kwargs) -> dict:
        """
        Get alert types metadata.
        
        Args:
            alert_types: List of alert type strings to get metadata for
            language: Language for alert metadata (default: en-US)
            **kwargs: Additional query parameters
            
        Returns:
            dict: API response containing alert types metadata
        """
        path = "alert-types"
        query_params = {"language": language}
        query_params.update(kwargs)
        
        if query_params:
            path += "?" + urlencode(query_params)
            
        payload = json.dumps(alert_types or [])
        response = self.api.do_request(path=path, method="POST", payload=payload)
        
        if response.status_code == 200:
            return response.json()
        log.error(f"Error getting alert types: {response.status_code}")
        log.error(response.text)
        return {}
