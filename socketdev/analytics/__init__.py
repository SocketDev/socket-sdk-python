import logging
from urllib.parse import urlencode

log = logging.getLogger("socketdev")


class Analytics:
    def __init__(self, api):
        self.api = api

    def get_org(self, filter: str, **kwargs) -> list:
        """
        Get organization analytics (deprecated).
        
        **DEPRECATED**: Use the Historical module methods instead:
        - sdk.historical.alerts_trend() for alerts analytics
        - sdk.historical.dependencies_trend() for dependencies analytics
        
        Args:
            filter: Analytics filter type
            **kwargs: Additional query parameters
            
        Returns:
            list: API response containing analytics data
        """
        log.warning("Analytics.get_org() is deprecated. Use Historical module methods instead.")
        path = f"analytics/org/{filter}"
        if kwargs:
            path += "?" + urlencode(kwargs)
            
        response = self.api.do_request(path=path)
        if response.status_code == 200:
            return response.json()
        log.error(f"Error getting org analytics: {response.status_code}")
        log.error(response.text)
        return []

    def get_repo(self, name: str, filter: str, **kwargs) -> list:
        """
        Get repository analytics (deprecated).
        
        **DEPRECATED**: Use the Historical module methods instead:
        - sdk.historical.alerts_trend() for alerts analytics  
        - sdk.historical.dependencies_trend() for dependencies analytics
        
        Args:
            name: Repository name
            filter: Analytics filter type
            **kwargs: Additional query parameters
            
        Returns:
            list: API response containing analytics data
        """
        log.warning("Analytics.get_repo() is deprecated. Use Historical module methods instead.")
        path = f"analytics/repo/{name}/{filter}"
        if kwargs:
            path += "?" + urlencode(kwargs)
            
        response = self.api.do_request(path=path)
        if response.status_code == 200:
            return response.json()
        log.error(f"Error getting repo analytics: {response.status_code}")
        log.error(response.text)
        return []
