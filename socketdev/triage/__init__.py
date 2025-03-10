import logging
from urllib.parse import urlencode
from socketdev.exceptions import APIFailure

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

        try:
            response = self.api.do_request(path=path)
            if response.status_code == 200:
                return response.json()
        except APIFailure as e:
            log.error(f"Socket SDK: API failure while getting alert triage list {e}")
            raise
        except Exception as e:
            log.error(f"Socket SDK: Unexpected error while getting alert triage list {e}")
            raise

        return {}

    def update_alert_triage(self, org_slug: str, body: dict) -> dict:
        """Update triaged alerts for an organization.

        Args:
            org_slug: Organization slug
            body: Alert triage configuration to update
        """
        path = f"orgs/{org_slug}/triage/alerts"

        try:
            response = self.api.do_request(path=path, method="POST", payload=body)
            if 200 <= response.status_code < 300:
                return response.json()
        except APIFailure as e:
            log.error(f"Socket SDK: API failure while updating alert triage {e}")
            raise
        except Exception as e:
            log.error(f"Socket SDK: Unexpected error while updating alert triage {e}")
            raise

        return {}
