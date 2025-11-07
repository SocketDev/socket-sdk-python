import os
import tempfile
import unittest
from unittest.mock import Mock, patch, mock_open
from socketdev.uploadmanifests import UploadManifests


class TestUploadManifests(unittest.TestCase):
    def setUp(self):
        self.mock_api = Mock()
        self.upload_manifests = UploadManifests(self.mock_api)

    def test_calculate_key_name_with_base_path(self):
        """Test that key names are calculated correctly with base_path."""
        # Test with base_path
        key = self.upload_manifests._calculate_key_name(
            "/project/frontend/package.json",
            base_path="/project"
        )
        self.assertEqual(key, "frontend/package.json")

    def test_calculate_key_name_with_workspace(self):
        """Test that key names are calculated correctly with workspace."""
        # Test with workspace
        key = self.upload_manifests._calculate_key_name(
            "/project/frontend/package.json",
            workspace="/project/"
        )
        self.assertEqual(key, "frontend/package.json")

    def test_calculate_key_name_with_base_paths(self):
        """Test that key names are calculated correctly with base_paths."""
        # Test with base_paths (takes precedence over base_path)
        key = self.upload_manifests._calculate_key_name(
            "/project/frontend/package.json",
            base_path="/project",
            base_paths=["/different", "/project"]
        )
        self.assertEqual(key, "frontend/package.json")

    def test_calculate_key_name_no_stripping(self):
        """Test that key names default to basename when no stripping options provided."""
        # Test without any path stripping - should preserve relative path structure
        key = self.upload_manifests._calculate_key_name(
            "frontend/package.json"
        )
        self.assertEqual(key, "frontend/package.json")

    def test_calculate_key_name_absolute_path_no_stripping(self):
        """Test that absolute paths get cleaned up when no stripping options provided."""
        key = self.upload_manifests._calculate_key_name(
            "/absolute/path/frontend/package.json"
        )
        self.assertEqual(key, "absolute/path/frontend/package.json")

    def test_calculate_key_name_windows_paths(self):
        """Test that Windows paths are handled correctly."""
        key = self.upload_manifests._calculate_key_name(
            "C:\\project\\frontend\\package.json",
            base_path="C:\\project"
        )
        self.assertEqual(key, "frontend/package.json")

    @patch('socketdev.uploadmanifests.Utils.load_files_for_sending_lazy')
    @patch('os.path.exists')
    @patch('os.path.isfile')
    def test_upload_manifest_files_lazy_loading(self, mock_isfile, mock_exists, mock_lazy_load):
        """Test that lazy loading preserves key names correctly."""
        # Setup mocks
        mock_exists.return_value = True
        mock_isfile.return_value = True
        mock_lazy_load.return_value = [
            ('frontend/package.json', ('frontend/package.json', Mock()))
        ]
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'tarHash': 'test_hash'}
        self.mock_api.do_request.return_value = mock_response

        # Test lazy loading
        result = self.upload_manifests.upload_manifest_files(
            "test_org",
            ["/project/frontend/package.json"],
            workspace="/project",
            use_lazy_loading=True
        )

        self.assertEqual(result, 'test_hash')
        mock_lazy_load.assert_called_once_with(
            ["/project/frontend/package.json"],
            workspace="/project",
            base_path=None,
            base_paths=None
        )

    @patch('builtins.open', new_callable=mock_open, read_data=b'{"name": "test"}')
    @patch('os.path.exists')
    @patch('os.path.isfile')
    def test_upload_manifest_files_non_lazy_loading(self, mock_isfile, mock_exists, mock_file):
        """Test that non-lazy loading produces same key names as lazy loading."""
        # Setup mocks
        mock_exists.return_value = True
        mock_isfile.return_value = True
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'tarHash': 'test_hash'}
        self.mock_api.do_request.return_value = mock_response

        # Test non-lazy loading with workspace
        result = self.upload_manifests.upload_manifest_files(
            "test_org",
            ["frontend/package.json"],
            workspace="/project",
            use_lazy_loading=False
        )

        self.assertEqual(result, 'test_hash')
        
        # Verify the API was called with the correct file structure
        call_args = self.mock_api.do_request.call_args
        files_arg = call_args[1]['files']
        self.assertEqual(len(files_arg), 1)
        
        # The key should be 'frontend/package.json' not just 'package.json'
        key, (filename, content) = files_arg[0]
        self.assertEqual(key, "frontend/package.json")
        self.assertEqual(filename, "frontend/package.json")

    @patch('builtins.open', new_callable=mock_open, read_data=b'{"name": "test"}')
    @patch('os.path.exists')
    @patch('os.path.isfile')
    def test_upload_manifest_files_consistency_between_modes(self, mock_isfile, mock_exists, mock_file):
        """Test that lazy and non-lazy loading produce identical key names."""
        # Setup mocks
        mock_exists.return_value = True
        mock_isfile.return_value = True
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'tarHash': 'test_hash'}
        self.mock_api.do_request.return_value = mock_response

        test_files = ["frontend/package.json", "backend/package.json"]
        
        # Test non-lazy loading
        with patch('socketdev.uploadmanifests.Utils.load_files_for_sending_lazy') as mock_lazy_load:
            mock_lazy_load.return_value = [
                ('frontend/package.json', ('frontend/package.json', Mock())),
                ('backend/package.json', ('backend/package.json', Mock()))
            ]
            
            # Get lazy loading result
            self.upload_manifests.upload_manifest_files(
                "test_org",
                test_files,
                use_lazy_loading=True
            )
            lazy_call_args = self.mock_api.do_request.call_args[1]['files']

        # Reset mock
        self.mock_api.reset_mock()
        
        # Get non-lazy loading result
        self.upload_manifests.upload_manifest_files(
            "test_org", 
            test_files,
            use_lazy_loading=False
        )
        non_lazy_call_args = self.mock_api.do_request.call_args[1]['files']

        # Compare key names - they should be identical
        lazy_keys = [item[0] for item in lazy_call_args]
        non_lazy_keys = [item[0] for item in non_lazy_call_args]
        
        self.assertEqual(lazy_keys, non_lazy_keys)
        self.assertEqual(non_lazy_keys, ['frontend/package.json', 'backend/package.json'])


if __name__ == '__main__':
    unittest.main()