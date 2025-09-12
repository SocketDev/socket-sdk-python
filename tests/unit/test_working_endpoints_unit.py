"""
Corrected comprehensive unit tests for Socket SDK endpoints.

This file contains working unit tests based on actual API signatures discovered.
Tests are organized by working/verified endpoints vs. endpoints that need investigation.

Run with: python -m pytest tests/unit/test_working_endpoints_unit.py -v
"""

import unittest
import tempfile
import json
import os
from unittest.mock import Mock, patch
from socketdev import socketdev
from socketdev.fullscans import FullScanParams


class TestWorkingEndpointsUnit(unittest.TestCase):
    """Unit tests for verified working Socket SDK endpoints."""

    def setUp(self):
        """Set up test environment with mocked API."""
        self.requests_patcher = patch('socketdev.core.api.requests')
        self.mock_requests = self.requests_patcher.start()
        self.sdk = socketdev(token="test-token")

    def tearDown(self):
        """Clean up patches."""
        self.requests_patcher.stop()

    def _mock_response(self, data=None, status_code=200):
        """Helper to create mock response."""
        if data is None:
            data = {"success": True}
        mock_response = Mock()
        mock_response.status_code = status_code
        mock_response.headers = {'content-type': 'application/json'}
        mock_response.json.return_value = data
        mock_response.text = json.dumps(data)
        self.mock_requests.request.return_value = mock_response
        return mock_response

    # =============================================================================
    # WORKING ENDPOINTS (verified from test output)
    # =============================================================================

    def test_npm_issues_unit(self):
        """Test NPM issues endpoint - WORKING."""
        expected_data = [{"type": "security", "severity": "high"}]
        self._mock_response(expected_data)
        
        result = self.sdk.npm.issues("lodash", "4.17.21")
        
        self.assertEqual(result, expected_data)
        call_args = self.mock_requests.request.call_args
        self.assertEqual(call_args[0][0], "GET")
        self.assertIn("/npm/lodash/4.17.21/issues", call_args[0][1])

    def test_npm_score_unit(self):
        """Test NPM score endpoint - WORKING."""
        expected_data = [{"category": "security", "value": 85}]
        self._mock_response(expected_data)
        
        result = self.sdk.npm.score("lodash", "4.17.21")
        
        self.assertEqual(result, expected_data)
        call_args = self.mock_requests.request.call_args
        self.assertEqual(call_args[0][0], "GET")
        self.assertIn("/npm/lodash/4.17.21/score", call_args[0][1])

    def test_openapi_get_unit(self):
        """Test OpenAPI specification retrieval - WORKING."""
        expected_data = {"openapi": "3.0.0", "info": {"title": "Socket API"}}
        self._mock_response(expected_data)
        
        result = self.sdk.openapi.get()
        
        self.assertEqual(result, expected_data)
        call_args = self.mock_requests.request.call_args
        self.assertEqual(call_args[0][0], "GET")
        self.assertIn("/openapi", call_args[0][1])

    def test_quota_get_unit(self):
        """Test quota retrieval - WORKING."""
        expected_data = {"quota": 1000, "used": 100}
        self._mock_response(expected_data)
        
        result = self.sdk.quota.get()
        
        self.assertEqual(result, expected_data)
        call_args = self.mock_requests.request.call_args
        self.assertEqual(call_args[0][0], "GET")
        self.assertIn("/quota", call_args[0][1])

    def test_settings_get_unit(self):
        """Test settings retrieval - WORKING."""
        expected_data = {"settings": {"notifications": True}}
        self._mock_response(expected_data)
        
        result = self.sdk.settings.get("test-org")
        
        self.assertEqual(result, expected_data)
        call_args = self.mock_requests.request.call_args
        self.assertEqual(call_args[0][0], "GET")
        self.assertIn("/orgs/test-org/settings", call_args[0][1])

    def test_diffscans_list_unit(self):
        """Test diffscans list - WORKING."""
        expected_data = {"results": []}
        self._mock_response(expected_data)
        
        result = self.sdk.diffscans.list("test-org")
        
        self.assertEqual(result, expected_data)
        call_args = self.mock_requests.request.call_args
        self.assertEqual(call_args[0][0], "GET")
        self.assertIn("/orgs/test-org/diff-scans", call_args[0][1])

    def test_diffscans_get_unit(self):
        """Test diffscans get - WORKING."""
        expected_data = {"id": "diff-123", "status": "completed"}
        self._mock_response(expected_data)
        
        result = self.sdk.diffscans.get("test-org", "diff-123")
        
        self.assertEqual(result, expected_data)
        call_args = self.mock_requests.request.call_args
        self.assertEqual(call_args[0][0], "GET")
        self.assertIn("/orgs/test-org/diff-scans/diff-123", call_args[0][1])

    def test_diffscans_gfm_unit(self):
        """Test diffscans GitHub Flavored Markdown - WORKING."""
        expected_data = {"markdown": "# Report"}
        self._mock_response(expected_data)
        
        result = self.sdk.diffscans.gfm("test-org", "diff-123")
        
        self.assertEqual(result, expected_data)
        call_args = self.mock_requests.request.call_args
        self.assertEqual(call_args[0][0], "GET")
        self.assertIn("/orgs/test-org/diff-scans/diff-123/gfm", call_args[0][1])

    def test_diffscans_create_from_ids_unit(self):
        """Test diffscans creation from IDs - WORKING."""
        expected_data = {"id": "new-diff"}
        self._mock_response(expected_data, 201)
        
        params = {"before": "scan1", "after": "scan2"}
        result = self.sdk.diffscans.create_from_ids("test-org", params)
        
        self.assertEqual(result, expected_data)
        call_args = self.mock_requests.request.call_args
        self.assertEqual(call_args[0][0], "POST")

    def test_historical_list_unit(self):
        """Test historical list - WORKING."""
        expected_data = {"results": []}
        self._mock_response(expected_data)
        
        result = self.sdk.historical.list("test-org")
        
        self.assertEqual(result, expected_data)
        call_args = self.mock_requests.request.call_args
        self.assertEqual(call_args[0][0], "GET")
        self.assertIn("/orgs/test-org/historical", call_args[0][1])

    def test_fullscans_delete_unit(self):
        """Test fullscans deletion - WORKING."""
        expected_data = {"status": "deleted"}
        self._mock_response(expected_data)
        
        result = self.sdk.fullscans.delete("test-org", "scan-123")
        
        self.assertEqual(result, expected_data)
        call_args = self.mock_requests.request.call_args
        self.assertEqual(call_args[0][0], "DELETE")

    def test_fullscans_post_unit(self):
        """Test fullscans creation - WORKING."""
        expected_data = {"id": "new-scan"}
        self._mock_response(expected_data, 201)
        
        params = FullScanParams(
            repo="test-repo",
            org_slug="test-org",
            branch="main"
        )
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump({"name": "test", "version": "1.0.0"}, f)
            f.flush()
            
            try:
                with open(f.name, "rb") as file_obj:
                    files = [("file", ("package.json", file_obj))]
                    result = self.sdk.fullscans.post(files, params)
                
                self.assertEqual(result, expected_data)
                call_args = self.mock_requests.request.call_args
                self.assertEqual(call_args[0][0], "POST")
                
            finally:
                os.unlink(f.name)

    def test_triage_list_alert_triage_unit(self):
        """Test triage list alerts - WORKING."""
        expected_data = {"alerts": []}
        self._mock_response(expected_data)
        
        result = self.sdk.triage.list_alert_triage("test-org")
        
        self.assertEqual(result, expected_data)
        call_args = self.mock_requests.request.call_args
        self.assertEqual(call_args[0][0], "GET")

    def test_analytics_get_org_unit(self):
        """Test analytics org endpoint - WORKING."""
        expected_data = [{"date": "2025-01-01", "count": 5}]
        self._mock_response(expected_data)
        
        result = self.sdk.analytics.get_org("dependencies")
        
        self.assertEqual(result, expected_data)
        call_args = self.mock_requests.request.call_args
        self.assertEqual(call_args[0][0], "GET")

    def test_analytics_get_repo_unit(self):
        """Test analytics repo endpoint - WORKING."""
        expected_data = [{"date": "2025-01-01", "count": 3}]
        self._mock_response(expected_data)
        
        result = self.sdk.analytics.get_repo("test-repo", "alerts")
        
        self.assertEqual(result, expected_data)
        call_args = self.mock_requests.request.call_args
        self.assertEqual(call_args[0][0], "GET")

    def test_apitokens_create_unit(self):
        """Test API token creation - WORKING."""
        expected_data = {"id": "token-123", "name": "test-token"}
        self._mock_response(expected_data, 201)
        
        result = self.sdk.apitokens.create("test-org", name="test-token")
        
        self.assertEqual(result, expected_data)
        call_args = self.mock_requests.request.call_args
        self.assertEqual(call_args[0][0], "POST")

    # =============================================================================
    # CORRECTED ENDPOINTS (fixed based on actual API paths)
    # =============================================================================

    def test_export_cdx_bom_corrected_unit(self):
        """Test CDX BOM export - CORRECTED PATH."""
        expected_data = {"bomFormat": "CycloneDX"}
        self._mock_response(expected_data)
        
        result = self.sdk.export.cdx_bom("test-org", "scan-123")
        
        self.assertEqual(result, expected_data)
        call_args = self.mock_requests.request.call_args
        self.assertEqual(call_args[0][0], "GET")
        # Corrected path based on actual implementation
        self.assertIn("/orgs/test-org/export/cdx/scan-123", call_args[0][1])

    def test_export_spdx_bom_corrected_unit(self):
        """Test SPDX BOM export - CORRECTED PATH."""
        expected_data = {"spdxVersion": "SPDX-2.2"}
        self._mock_response(expected_data)
        
        result = self.sdk.export.spdx_bom("test-org", "scan-123")
        
        self.assertEqual(result, expected_data)
        call_args = self.mock_requests.request.call_args
        self.assertEqual(call_args[0][0], "GET")
        # Corrected path based on actual implementation
        self.assertIn("/orgs/test-org/export/spdx/scan-123", call_args[0][1])

    def test_dependencies_get_corrected_unit(self):
        """Test dependencies get - CORRECTED SIGNATURE."""
        expected_data = {"dependencies": []}
        self._mock_response(expected_data)
        
        # Correct signature: limit and offset only
        result = self.sdk.dependencies.get(limit=50, offset=0)
        
        self.assertEqual(result, expected_data)
        call_args = self.mock_requests.request.call_args
        self.assertEqual(call_args[0][0], "POST")  # It's actually POST, not GET
        self.assertIn("/dependencies/search", call_args[0][1])

    def test_threatfeed_get_corrected_unit(self):
        """Test threatfeed get - CORRECTED PATH."""
        expected_data = {"results": []}
        self._mock_response(expected_data)
        
        result = self.sdk.threatfeed.get("test-org")
        
        self.assertEqual(result, expected_data)
        call_args = self.mock_requests.request.call_args
        self.assertEqual(call_args[0][0], "GET")
        # Corrected path based on actual implementation
        self.assertIn("/orgs/test-org/threat-feed", call_args[0][1])

    def test_historical_trend_corrected_unit(self):
        """Test historical trend - CORRECTED PATH."""
        expected_data = {"trend": []}
        self._mock_response(expected_data)
        
        result = self.sdk.historical.trend("test-org")
        
        self.assertEqual(result, expected_data)
        call_args = self.mock_requests.request.call_args
        self.assertEqual(call_args[0][0], "GET")
        # Corrected path based on actual implementation
        self.assertIn("/orgs/test-org/historical/alerts/trend", call_args[0][1])

    # =============================================================================
    # COMPLEX ENDPOINT TESTS (file handling, special parameters)
    # =============================================================================

    def test_dependencies_post_corrected_unit(self):
        """Test dependencies post - CORRECTED FILE HANDLING."""
        expected_data = {"packages": []}
        self._mock_response(expected_data)
        
        # Create a real file and pass just the filename, not tuple
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump({"name": "test", "version": "1.0.0"}, f)
            f.flush()
            
            try:
                # Pass just filename, not file object
                result = self.sdk.dependencies.post([f.name], {})
                
                self.assertEqual(result, expected_data)
                call_args = self.mock_requests.request.call_args
                self.assertEqual(call_args[0][0], "POST")
                self.assertIn("/dependencies/upload", call_args[0][1])
                
            finally:
                os.unlink(f.name)

    def test_fullscans_get_corrected_unit(self):
        """Test fullscans get - CORRECTED PARAMETER HANDLING."""
        expected_data = {"id": "scan-123", "status": "completed"}
        self._mock_response(expected_data)

        # When getting a specific scan by ID, it uses path parameters
        result = self.sdk.fullscans.get("test-org", {"id": "scan-123"})

        self.assertEqual(result, expected_data)
        call_args = self.mock_requests.request.call_args
        self.assertEqual(call_args[0][0], "GET")
        # Single ID param creates path segment, not query params
        self.assertIn("/orgs/test-org/full-scans/scan-123", call_args[0][1])

    def test_diffscans_create_from_repo_corrected_unit(self):
        """Test diffscans creation from repo - CORRECTED PATH."""
        expected_data = {"id": "repo-diff"}
        self._mock_response(expected_data, 201)
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump({"name": "test", "version": "1.0.0"}, f)
            f.flush()
            
            try:
                with open(f.name, "rb") as file_obj:
                    files = [("file", ("package.json", file_obj))]
                    params = {"description": "Test diff"}
                    result = self.sdk.diffscans.create_from_repo("test-org", "test-repo", files, params)
                
                self.assertEqual(result, expected_data)
                call_args = self.mock_requests.request.call_args
                self.assertEqual(call_args[0][0], "POST")
                # Corrected path based on actual implementation
                self.assertIn("/orgs/test-org/diff-scans/from-repo/test-repo", call_args[0][1])
                
            finally:
                os.unlink(f.name)


class TestEndpointSignatureDiscovery(unittest.TestCase):
    """Tests to discover correct API signatures for problematic endpoints."""

    def setUp(self):
        """Set up test environment with mocked API."""
        self.requests_patcher = patch('socketdev.core.api.requests')
        self.mock_requests = self.requests_patcher.start()
        self.sdk = socketdev(token="test-token")

    def tearDown(self):
        """Clean up patches."""
        self.requests_patcher.stop()

    def _mock_response(self, data=None, status_code=200):
        """Helper to create mock response."""
        if data is None:
            data = {"success": True}
        mock_response = Mock()
        mock_response.status_code = status_code
        mock_response.headers = {'content-type': 'application/json'}
        mock_response.json.return_value = data
        mock_response.text = json.dumps(data)
        self.mock_requests.request.return_value = mock_response
        return mock_response

    def test_org_get_discover_signature(self):
        """Discover the correct org.get signature."""
        expected_data = {"name": "test-org"}
        self._mock_response(expected_data)
        
        # Try the call and see what path it actually uses
        try:
            result = self.sdk.org.get("test-org")
            call_args = self.mock_requests.request.call_args
            print(f"org.get path: {call_args[0][1]}")
            print(f"org.get method: {call_args[0][0]}")
        except Exception as e:
            print(f"org.get error: {e}")

    def test_labels_discover_signature(self):
        """Discover the correct labels signatures."""
        expected_data = {"label": "test"}
        self._mock_response(expected_data)
        
        # Try to discover the actual method names available
        try:
            methods = [attr for attr in dir(self.sdk.labels) if not attr.startswith('_')]
            print(f"labels methods: {methods}")
            
            # Try get with different signatures
            if hasattr(self.sdk.labels, 'get'):
                try:
                    result = self.sdk.labels.get("test-org", 1)
                    call_args = self.mock_requests.request.call_args
                    print(f"labels.get(org, id) path: {call_args[0][1]}")
                except Exception as e:
                    print(f"labels.get(org, id) error: {e}")
                    
        except Exception as e:
            print(f"labels discovery error: {e}")

    def test_discover_missing_methods(self):
        """Test which methods don't exist on various endpoints."""
        endpoints_to_check = [
            ('export', ['get']),
            ('apitokens', ['list']),
            ('licensemetadata', ['get']),
            ('labels', ['put'])
        ]
        
        for endpoint_name, methods in endpoints_to_check:
            endpoint = getattr(self.sdk, endpoint_name)
            for method in methods:
                has_method = hasattr(endpoint, method)
                available_methods = [attr for attr in dir(endpoint) if not attr.startswith('_') and callable(getattr(endpoint, attr))]
                print(f"{endpoint_name}.{method} exists: {has_method}")
                print(f"{endpoint_name} available methods: {available_methods}")


if __name__ == "__main__":
    unittest.main()
