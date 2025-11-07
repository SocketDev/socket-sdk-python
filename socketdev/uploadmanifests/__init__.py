import os
import logging
from typing import List, Optional, Union
from ..utils import Utils

log = logging.getLogger("socketdev")


class UploadManifests:
    def __init__(self, api):
        self.api = api

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
                key = os.path.basename(file_path)
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