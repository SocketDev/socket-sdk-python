import logging
from urllib.parse import urlencode

log = logging.getLogger("socketdev")


class Historical:
    def __init__(self, api):
        self.api = api
        self.snapshots = self.Snapshots(api)

    def list(self, org_slug: str, query_params: dict = None) -> dict:
        """Get historical alerts list for an organization.

        Args:
            org_slug: Organization slug
            query_params: Optional dictionary of query parameters
        """
        path = f"orgs/{org_slug}/historical/alerts"
        if query_params:
            path += "?" + urlencode(query_params)

        response = self.api.do_request(path=path)
        if response.status_code == 200:
            return response.json()

        log.error(f"Error getting historical alerts: {response.status_code}")
        log.error(response.text)
        return {}

    def trend(self, org_slug: str, query_params: dict = None) -> dict:
        """Get historical alert trends data for an org.

        Args:
            org_slug: Organization slug
            query_params: Optional dictionary of query parameters
        """
        path = f"orgs/{org_slug}/historical/alerts/trend"
        if query_params:
            path += "?" + urlencode(query_params)

        response = self.api.do_request(path=path)
        if response.status_code == 200:
            return response.json()

        log.error(f"Error getting historical trend: {response.status_code}")
        log.error(response.text)
        return {}

    class Snapshots:
        """Submodule for managing historical snapshots."""

        def __init__(self, api):
            self.api = api

        def create(self, org_slug: str) -> dict:
            """Create a new snapshot for an organization.

            Args:
                org_slug: Organization slug
                data: Dictionary containing snapshot data
            """
            path = f"orgs/{org_slug}/historical/snapshots"
            response = self.api.do_request(path=path, method="POST")
            if response.status_code == 200:
                return response.json()

            log.error(f"Error creating snapshot: {response.status_code}")
            log.error(response.text)
            return {}

        def list(self, org_slug: str, query_params: dict = None) -> dict:
            """List historical snapshots for an organization."""
            path = f"orgs/{org_slug}/historical/snapshots"
            if query_params:
                path += "?" + urlencode(query_params)

            response = self.api.do_request(path=path)
            if response.status_code == 200:
                return response.json()

            log.error(f"Error listing snapshots: {response.status_code}")
            log.error(response.text)
            return {}
