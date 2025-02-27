import logging
from urllib.parse import urlencode

log = logging.getLogger("socketdev")


class Triage:
    def __init__(self, api):
        self.api = api

    def list_alert_triage(self, org_slug: str, query_params: dict = None) -> dict:
        """Get list of triaged alerts for an organization.

        Args:
            org_slug: Organization slug
            query_params: Optional dictionary of query parameters
        """
        path = f"orgs/{org_slug}/triage/alerts"
        if query_params:
            path += "?" + urlencode(query_params)

        response = self.api.do_request(path=path)

        if response.status_code == 200:
            return response.json()

        error_message = response.json().get("error", {}).get("message", "Unknown error")
        log.error(f"Error getting alert triage list: {response.status_code}, message: {error_message}")
        return {}

    def update_alert_triage(self, org_slug: str, body: dict) -> dict:
        """Update triaged alerts for an organization.

        Args:
            org_slug: Organization slug
            body: Alert triage configuration to update
        """
        path = f"orgs/{org_slug}/triage/alerts"

        response = self.api.do_request(path=path, method="POST", payload=body)

        if 200 <= response.status_code < 300:
            return response.json()

        error_message = response.json().get("error", {}).get("message", "Unknown error")
        log.error(f"Error updating alert triage: {response.status_code}, message: {error_message}")
        return {}
