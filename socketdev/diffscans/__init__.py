import json
import logging
from typing import Any, Dict, Optional, Union

log = logging.getLogger("socketdev")

class DiffScans:
    def __init__(self, api):
        self.api = api

    def list(self, org_slug: str, params: Optional[Dict[str, Any]] = None) -> dict:
        """List all diff scans for an organization."""
        path = f"orgs/{org_slug}/diff-scans"
        if params:
            import urllib.parse
            path += "?" + urllib.parse.urlencode(params)
        response = self.api.do_request(path=path, method="GET")
        if response.status_code == 200:
            return response.json()
        log.error(f"Error listing diff scans: {response.status_code}, message: {response.text}")
        return {}

    def get(self, org_slug: str, diff_scan_id: str) -> dict:
        """Fetch a diff scan by ID."""
        path = f"orgs/{org_slug}/diff-scans/{diff_scan_id}"
        response = self.api.do_request(path=path, method="GET")
        if response.status_code == 200:
            return response.json()
        log.error(f"Error fetching diff scan: {response.status_code}, message: {response.text}")
        return {}

    def create_from_repo(self, org_slug: str, repo_slug: str, files: list, params: Optional[Dict[str, Any]] = None) -> dict:
        """Create a diff scan from repo HEAD, uploading files as multipart form data."""
        import urllib.parse
        path = f"orgs/{org_slug}/diff-scans/from-repo/{repo_slug}"
        if params:
            path += "?" + urllib.parse.urlencode(params)
        response = self.api.do_request(path=path, method="POST", files=files)
        if response.status_code in (200, 201):
            return response.json()
        log.error(f"Error creating diff scan from repo: {response.status_code}, message: {response.text}")
        return {}

    def create_from_ids(self, org_slug: str, params: Dict[str, Any]) -> dict:
        """Create a diff scan from two full scan IDs using query params."""
        import urllib.parse
        path = f"orgs/{org_slug}/diff-scans/from-ids"
        if params:
            path += "?" + urllib.parse.urlencode(params)
        response = self.api.do_request(path=path, method="POST")
        if response.status_code in (200, 201):
            return response.json()
        log.error(f"Error creating diff scan from IDs: {response.status_code}, message: {response.text}")
        return {}

    def gfm(self, org_slug: str, diff_scan_id: str) -> dict:
        """Fetch GFM (GitHub Flavored Markdown) comments for a diff scan."""
        path = f"orgs/{org_slug}/diff-scans/{diff_scan_id}/gfm"
        response = self.api.do_request(path=path, method="GET")
        if response.status_code == 200:
            return response.json()
        log.error(f"Error fetching diff scan GFM: {response.status_code}, message: {response.text}")
        return {}

    def delete(self, org_slug: str, diff_scan_id: str) -> bool:
        """Delete a diff scan by ID."""
        path = f"orgs/{org_slug}/diff-scans/{diff_scan_id}"
        response = self.api.do_request(path=path, method="DELETE")
        if response.status_code == 200:
            if "status" in response.json() and response.json()["status"] == "ok":
                return True
        log.error(f"Error deleting diff scan: {response.status_code}, message: {response.text}")
        return False
