import os
import logging
from typing import List, Optional, Union
from ..utils import Utils

log = logging.getLogger("socketdev")


class UploadManifests:
    def __init__(self, api):
        self.api = api

    def _calculate_key_name(self, file_path: str, workspace: Optional[str] = None, base_path: Optional[str] = None, base_paths: Optional[List[str]] = None) -> str:
        """
        Calculate the key name for a file using the same logic as load_files_for_sending_lazy.
        This ensures consistency between lazy and non-lazy loading modes.
        """
        # Normalize file path
        if "\\" in file_path:
            file_path = file_path.replace("\\", "/")
        
        # Normalize paths
        if workspace and "\\" in workspace:
            workspace = workspace.replace("\\", "/")
        if base_path and "\\" in base_path:
            base_path = base_path.replace("\\", "/")
        if base_paths:
            base_paths = [bp.replace("\\", "/") if "\\" in bp else bp for bp in base_paths]

        # Calculate the key name for the form data
        key = file_path
        path_stripped = False

        # If base_paths is provided, try to strip one of the paths from the file path
        if base_paths:
            for bp in base_paths:
                normalized_base_path = bp.rstrip("/") + "/" if not bp.endswith("/") else bp
                if key.startswith(normalized_base_path):
                    key = key[len(normalized_base_path):]
                    path_stripped = True
                    break
                elif key.startswith(bp.rstrip("/")):
                    stripped_base = bp.rstrip("/")
                    if key.startswith(stripped_base + "/") or key == stripped_base:
                        key = key[len(stripped_base):]
                        key = key.lstrip("/")
                        path_stripped = True
                        break
        elif base_path:
            normalized_base_path = base_path.rstrip("/") + "/" if not base_path.endswith("/") else base_path
            if key.startswith(normalized_base_path):
                key = key[len(normalized_base_path):]
                path_stripped = True
            elif key.startswith(base_path.rstrip("/")):
                stripped_base = base_path.rstrip("/")
                if key.startswith(stripped_base + "/") or key == stripped_base:
                    key = key[len(stripped_base):]
                    key = key.lstrip("/")
                    path_stripped = True

        # If workspace is provided and no base paths matched, fall back to workspace logic
        if not path_stripped and workspace and file_path.startswith(workspace):
            key = file_path[len(workspace):]
            # Remove all leading slashes (for absolute paths)
            while key.startswith("/"):
                key = key[1:]
            path_stripped = True

        # Clean up relative path prefixes, but preserve filename dots
        while key.startswith("./"):
            key = key[2:]
        while key.startswith("../"):
            key = key[3:]
        # Remove any remaining leading slashes (for absolute paths)
        while key.startswith("/"):
            key = key[1:]

        # Remove Windows drive letter if present (C:/...)
        if len(key) > 2 and key[1] == ':' and (key[2] == '/' or key[2] == '\\'):
            key = key[2:]
            while key.startswith("/"):
                key = key[1:]

        return key

    def upload_manifest_files(self, org_slug: str, file_paths: List[str], workspace: Optional[str] = None, base_path: Optional[str] = None, base_paths: Optional[List[str]] = None, use_lazy_loading: bool = True) -> str:
        """
        Upload manifest files to Socket API and return tarHash.
        
        Args:
            org_slug: Organization slug
            file_paths: List of manifest file paths to upload
            workspace: Base directory path to make paths relative to
            base_path: Optional base path to strip from key names for cleaner file organization
            base_paths: Optional list of base paths to strip from key names (takes precedence over base_path)
            use_lazy_loading: Whether to use lazy file loading (default: True)
            
        Returns:
            str: The tarHash from the upload response
            
        Raises:
            Exception: If upload fails
        """
        # Filter to only existing files
        valid_files = [f for f in file_paths if os.path.exists(f) and os.path.isfile(f)]
        
        if not valid_files:
            raise Exception("No valid manifest files found to upload")
        
        # Prepare files for upload using the utility function
        if use_lazy_loading:
            loaded_files = Utils.load_files_for_sending_lazy(
                valid_files, 
                workspace=workspace, 
                base_path=base_path, 
                base_paths=base_paths
            )
        else:
            # Fallback to basic file loading if needed
            loaded_files = []
            for file_path in valid_files:
                # Use the same key generation logic as lazy loading for consistency
                key = self._calculate_key_name(file_path, workspace, base_path, base_paths)
                with open(file_path, 'rb') as f:
                    loaded_files.append((key, (key, f.read())))
        
        # Make the upload request
        path = f"orgs/{org_slug}/upload-manifest-files"
        response = self.api.do_request(path=path, files=loaded_files, method="POST")
        
        if response.status_code != 200:
            raise Exception(f"Upload failed with status {response.status_code}: {response.text}")
        
        result = response.json()
        tar_hash = result.get('tarHash')
        
        if not tar_hash:
            raise Exception("Server did not return a tarHash")
            
        log.info(f"Successfully uploaded {len(valid_files)} manifest files, tarHash: {tar_hash}")
        return tar_hash