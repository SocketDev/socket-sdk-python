import json
import logging
from typing import Any, Dict, List, Optional, Union
from ..utils import Utils

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

    def create_from_repo(self, org_slug: str, repo_slug: str, files: list, params: Optional[Dict[str, Any]] = None, use_lazy_loading: bool = False, workspace: str = None, max_open_files: int = 100, base_path: str = None, base_paths: list = None) -> dict:
        """
        Create a diff scan from repo HEAD, uploading files as multipart form data.
        
        Args:
            org_slug: Organization slug
            repo_slug: Repository slug  
            files: List of file paths to upload for scanning
            params: Optional query parameters for the request
            use_lazy_loading: Whether to use lazy file loading to prevent "too many open files" 
                            errors when uploading large numbers of files (default: False)
                            NOTE: In version 3.0, this will default to True for better performance
            workspace: Base directory path to make file paths relative to
            max_open_files: Maximum number of files to keep open simultaneously when using 
                          lazy loading. Useful for systems with low ulimit values (default: 100)
            base_path: Optional base path to strip from key names for cleaner file organization
            base_paths: Optional list of base paths to strip from key names (takes precedence over base_path)
        
        Returns:
            dict: API response containing diff scan results
            
        Note:
            When use_lazy_loading=True, files are opened only when needed during upload,
            preventing file descriptor exhaustion. The max_open_files parameter controls how many
            files can be open simultaneously - set this lower on systems with restrictive ulimits.
            
            For large file uploads (>100 files), it's recommended to set use_lazy_loading=True.
        """
        import urllib.parse
        path = f"orgs/{org_slug}/diff-scans/from-repo/{repo_slug}"
        if params:
            path += "?" + urllib.parse.urlencode(params)
        
        # Use lazy loading if requested
        if use_lazy_loading:
            prepared_files = Utils.load_files_for_sending_lazy(files, workspace, max_open_files, base_path, base_paths)
        else:
            prepared_files = files
        
        response = self.api.do_request(path=path, method="POST", files=prepared_files)
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
