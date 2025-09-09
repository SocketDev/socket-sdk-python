"""
Comprehensive unit tests for ALL Socket SDK endpoints.

This file contains unit tests with proper mocking for every available endpoint.
These tests verify API signature handling, parameter passing, and response parsing.

Run with: python -m pytest tests/unit/test_all_endpoints_unit.py -v
"""

import unittest
import tempfile
import json
import os
from unittest.mock import Mock, patch, mock_open
from socketdev import socketdev
from socketdev.fullscans import FullScanParams


class TestAllEndpointsUnit(unittest.TestCase):
    """Unit tests for all Socket SDK endpoints with comprehensive mocking."""

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

    # Dependencies endpoints
    def test_dependencies_post_unit(self):
        """Test dependencies post with proper file handling."""
        expected_data = {"packages": [{"name": "lodash", "version": "4.17.21"}]}
        self._mock_response(expected_data)
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump({"name": "test-package", "dependencies": {"lodash": "4.17.21"}}, f)
            f.flush()
            
            try:
                # Pass the file path as a string, not a file object
                files = [f.name]
                result = self.sdk.dependencies.post(files, {})
                
                self.assertEqual(result, expected_data)
                self.mock_requests.request.assert_called_once()
                
                # Verify the request was made with correct parameters
                call_args = self.mock_requests.request.call_args
                self.assertEqual(call_args[0][0], "POST")
                self.assertIn("/dependencies", call_args[0][1])
                
            finally:
                os.unlink(f.name)

    def test_dependencies_get_unit(self):
        """Test dependencies get with all parameters."""
        expected_data = {"dependencies": [{"name": "sub-dependency", "version": "1.0.0"}]}
        self._mock_response(expected_data)
        
        result = self.sdk.dependencies.get("test-org", "npm", "lodash", "4.17.21")
        
        self.assertEqual(result, expected_data)
        call_args = self.mock_requests.request.call_args
        self.assertEqual(call_args[0][0], "GET")
        self.assertIn("/orgs/test-org/dependencies/npm/lodash/4.17.21", call_args[0][1])

    # DiffScans endpoints
    def test_diffscans_list_unit(self):
        """Test diffscans list with pagination."""
        expected_data = {
            "results": [{"id": "diff-1", "status": "completed"}],
            "total": 1,
            "page": 1
        }
        self._mock_response(expected_data)
        
        result = self.sdk.diffscans.list("test-org")
        
        self.assertEqual(result, expected_data)
        call_args = self.mock_requests.request.call_args
        self.assertEqual(call_args[0][0], "GET")
        self.assertIn("/orgs/test-org/diff-scans", call_args[0][1])

    def test_diffscans_get_unit(self):
        """Test diffscans get specific scan."""
        expected_data = {
            "id": "diff-123", 
            "status": "completed",
            "created_at": "2025-01-01T00:00:00Z",
            "diff": {"added": [], "removed": [], "modified": []}
        }
        self._mock_response(expected_data)
        
        result = self.sdk.diffscans.get("test-org", "diff-123")
        
        self.assertEqual(result, expected_data)
        call_args = self.mock_requests.request.call_args
        self.assertEqual(call_args[0][0], "GET")
        self.assertIn("/orgs/test-org/diff-scans/diff-123", call_args[0][1])

    def test_diffscans_create_from_ids_unit(self):
        """Test diffscans creation from scan IDs."""
        expected_data = {"id": "new-diff-scan", "status": "queued"}
        self._mock_response(expected_data, 201)
        
        params = {
            "before": "scan-1",
            "after": "scan-2",
            "description": "Test diff scan"
        }
        result = self.sdk.diffscans.create_from_ids("test-org", params)
        
        self.assertEqual(result, expected_data)
        call_args = self.mock_requests.request.call_args
        self.assertEqual(call_args[0][0], "POST")
        self.assertIn("/orgs/test-org/diff-scans", call_args[0][1])

    def test_diffscans_create_from_repo_unit(self):
        """Test diffscans creation from repo files."""
        expected_data = {"id": "repo-diff-scan", "status": "queued"}
        self._mock_response(expected_data, 201)
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump({"name": "test", "version": "1.0.0"}, f)
            f.flush()
            
            try:
                with open(f.name, "rb") as file_obj:
                    files = [("file", ("package.json", file_obj))]
                    params = {"description": "Test repo diff"}
                    result = self.sdk.diffscans.create_from_repo("test-org", "test-repo", files, params)
                
                self.assertEqual(result, expected_data)
                call_args = self.mock_requests.request.call_args
                self.assertEqual(call_args[0][0], "POST")
                self.assertIn("/orgs/test-org/diff-scans/from-repo/test-repo", call_args[0][1])
                
            finally:
                os.unlink(f.name)

    def test_diffscans_gfm_unit(self):
        """Test diffscans GitHub Flavored Markdown export."""
        expected_data = {"markdown": "# Diff Report\n\n## Summary\n- Added: 0\n- Removed: 0"}
        self._mock_response(expected_data)
        
        result = self.sdk.diffscans.gfm("test-org", "diff-123")
        
        self.assertEqual(result, expected_data)
        call_args = self.mock_requests.request.call_args
        self.assertEqual(call_args[0][0], "GET")
        self.assertIn("/orgs/test-org/diff-scans/diff-123/gfm", call_args[0][1])

    def test_diffscans_delete_unit(self):
        """Test diffscans deletion."""
        self._mock_response({"status": "ok"}, 200)
        
        result = self.sdk.diffscans.delete("test-org", "diff-123")
        
        self.assertTrue(result)
        call_args = self.mock_requests.request.call_args
        self.assertEqual(call_args[0][0], "DELETE")
        self.assertIn("/orgs/test-org/diff-scans/diff-123", call_args[0][1])

    # Export endpoints
    def test_export_cdx_bom_unit(self):
        """Test CDX BOM export."""
        expected_data = {
            "bomFormat": "CycloneDX",
            "specVersion": "1.4",
            "components": []
        }
        self._mock_response(expected_data)
        
        result = self.sdk.export.cdx_bom("test-org", "scan-123")
        
        self.assertEqual(result, expected_data)
        call_args = self.mock_requests.request.call_args
        self.assertEqual(call_args[0][0], "GET")
        self.assertIn("/orgs/test-org/export/cdx/scan-123", call_args[0][1])

    def test_export_spdx_bom_unit(self):
        """Test SPDX BOM export."""
        expected_data = {
            "spdxVersion": "SPDX-2.2",
            "SPDXID": "SPDXRef-DOCUMENT",
            "packages": []
        }
        self._mock_response(expected_data)
        
        result = self.sdk.export.spdx_bom("test-org", "scan-123")
        
        self.assertEqual(result, expected_data)
        call_args = self.mock_requests.request.call_args
        self.assertEqual(call_args[0][0], "GET")
        self.assertIn("/orgs/test-org/export/spdx/scan-123", call_args[0][1])

    # FullScans endpoints
    def test_fullscans_get_unit(self):
        """Test fullscans get with various parameter types."""
        expected_data = {"id": "scan-123", "status": "completed", "results": []}
        self._mock_response(expected_data)
        
        # Test with commit parameter
        result = self.sdk.fullscans.get("test-org", {"id": "scan-123"})
        
        self.assertEqual(result, expected_data)
        call_args = self.mock_requests.request.call_args
        self.assertEqual(call_args[0][0], "GET")
        self.assertIn("/orgs/test-org/full-scans/scan-123", call_args[0][1])

    def test_fullscans_post_unit(self):
        """Test fullscans creation with all parameters."""
        expected_data = {"id": "new-scan", "status": "queued"}
        self._mock_response(expected_data, 201)
        
        params = FullScanParams(
            repo="test-repo",
            org_slug="test-org",
            branch="main",
            commit_message="Test scan",
            commit_hash="abc123",
            integration_type="github"
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
                self.assertIn("/full-scans", call_args[0][1])
                
            finally:
                os.unlink(f.name)

    def test_fullscans_delete_unit(self):
        """Test fullscans deletion."""
        expected_data = {"status": "deleted"}
        self._mock_response(expected_data)
        
        result = self.sdk.fullscans.delete("test-org", "scan-123")
        
        self.assertEqual(result, expected_data)
        call_args = self.mock_requests.request.call_args
        self.assertEqual(call_args[0][0], "DELETE")
        self.assertIn("/orgs/test-org/full-scans/scan-123", call_args[0][1])

    # Historical endpoints
    def test_historical_list_unit(self):
        """Test historical list with filtering."""
        expected_data = {
            "results": [{"date": "2025-01-01", "count": 5}],
            "total": 1
        }
        self._mock_response(expected_data)
        
        result = self.sdk.historical.list("test-org")
        
        self.assertEqual(result, expected_data)
        call_args = self.mock_requests.request.call_args
        self.assertEqual(call_args[0][0], "GET")
        self.assertIn("/orgs/test-org/historical", call_args[0][1])

    def test_historical_trend_unit(self):
        """Test historical trend analysis."""
        expected_data = {
            "trend": [
                {"date": "2025-01-01", "value": 10},
                {"date": "2025-01-02", "value": 15}
            ]
        }
        self._mock_response(expected_data)
        
        result = self.sdk.historical.trend("test-org")
        
        self.assertEqual(result, expected_data)
        call_args = self.mock_requests.request.call_args
        self.assertEqual(call_args[0][0], "GET")
        self.assertIn("/orgs/test-org/historical/alerts/trend", call_args[0][1])

    # NPM endpoints
    def test_npm_issues_unit(self):
        """Test npm issues endpoint."""
        expected_data = [{"type": "security", "severity": "high", "title": "Test issue"}]
        self._mock_response(expected_data)
        
        result = self.sdk.npm.issues("lodash", "4.17.21")
        
        self.assertEqual(result, expected_data)
        call_args = self.mock_requests.request.call_args
        self.assertEqual(call_args[0][0], "GET")
        self.assertIn("/npm/lodash/4.17.21/issues", call_args[0][1])

    def test_npm_score_unit(self):
        """Test npm score endpoint."""
        expected_data = [{"category": "security", "value": 85}]
        self._mock_response(expected_data)
        
        result = self.sdk.npm.score("lodash", "4.17.21")
        
        self.assertEqual(result, expected_data)
        call_args = self.mock_requests.request.call_args
        self.assertEqual(call_args[0][0], "GET")
        self.assertIn("/npm/lodash/4.17.21/score", call_args[0][1])

    # OpenAPI endpoints
    def test_openapi_get_unit(self):
        """Test OpenAPI specification retrieval."""
        expected_data = {"openapi": "3.0.0", "info": {"title": "Socket API"}}
        self._mock_response(expected_data)
        
        result = self.sdk.openapi.get()
        
        self.assertEqual(result, expected_data)
        call_args = self.mock_requests.request.call_args
        self.assertEqual(call_args[0][0], "GET")
        self.assertIn("/openapi", call_args[0][1])

    # Org endpoints
    def test_org_get_unit(self):
        """Test organization retrieval."""
        expected_data = {"organizations": {"test-org": {"name": "test-org", "id": "org-123", "plan": "pro"}}}
        self._mock_response(expected_data)
        
        result = self.sdk.org.get("test-org")
        
        self.assertEqual(result, expected_data)
        call_args = self.mock_requests.request.call_args
        self.assertEqual(call_args[0][0], "GET")
        self.assertIn("/organizations", call_args[0][1])

    # PURL endpoints
    def test_purl_post_unit(self):
        """Test PURL validation endpoint."""
        # Expected final result after deduplication - should match what the dedupe function produces
        expected_data = [{
            "inputPurl": "pkg:npm/lodash@4.17.21", 
            "purl": "pkg:npm/lodash@4.17.21", 
            "type": "npm", 
            "name": "lodash", 
            "version": "4.17.21", 
            "valid": True, 
            "alerts": [], 
            "releases": ["npm"]
        }]
        
        # Mock the NDJSON response that would come from the actual API
        # This simulates what the API returns: newline-delimited JSON with SocketArtifact objects
        mock_ndjson_response = '{"inputPurl": "pkg:npm/lodash@4.17.21", "purl": "pkg:npm/lodash@4.17.21", "type": "npm", "name": "lodash", "version": "4.17.21", "valid": true, "alerts": []}'
        
        # Mock the response with NDJSON format
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.headers = {'content-type': 'application/x-ndjson'}
        mock_response.text = mock_ndjson_response
        self.mock_requests.request.return_value = mock_response
        
        components = [{"purl": "pkg:npm/lodash@4.17.21"}]
        result = self.sdk.purl.post("false", components)
        
        self.assertEqual(result, expected_data)
        call_args = self.mock_requests.request.call_args
        self.assertEqual(call_args[0][0], "POST")
        self.assertIn("/purl", call_args[0][1])

    # Quota endpoints
    def test_quota_get_unit(self):
        """Test quota retrieval."""
        expected_data = {"quota": 1000, "used": 100, "remaining": 900}
        self._mock_response(expected_data)
        
        result = self.sdk.quota.get()
        
        self.assertEqual(result, expected_data)
        call_args = self.mock_requests.request.call_args
        self.assertEqual(call_args[0][0], "GET")
        self.assertIn("/quota", call_args[0][1])

    # Report endpoints
    def test_report_list_unit(self):
        """Test report listing."""
        expected_data = {"reports": [{"id": "rep-1", "status": "completed"}]}
        self._mock_response(expected_data)
        
        result = self.sdk.report.list()
        
        self.assertEqual(result, expected_data)
        call_args = self.mock_requests.request.call_args
        self.assertEqual(call_args[0][0], "GET")
        self.assertIn("/report/list", call_args[0][1])

    def test_report_create_unit(self):
        """Test report creation."""
        expected_data = {"id": "report-123", "url": "https://socket.dev/report/report-123"}
        self._mock_response(expected_data, 200)  # API returns 200, not 201
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump({"name": "test", "version": "1.0.0"}, f)
            f.flush()
            
            try:
                with open(f.name, "rb") as file_obj:
                    files = [("file", ("package.json", file_obj))]
                    result = self.sdk.report.create(files)
                
                self.assertEqual(result, expected_data)
                call_args = self.mock_requests.request.call_args
                self.assertEqual(call_args[0][0], "PUT")  # API uses PUT, not POST
                self.assertIn("/report/upload", call_args[0][1])  # Correct path per OpenAPI
                
            finally:
                os.unlink(f.name)

    def test_report_view_unit(self):
        """Test report viewing."""
        expected_data = {"id": "report-123", "status": "completed", "results": []}
        self._mock_response(expected_data)
        
        result = self.sdk.report.view("report-123")
        
        self.assertEqual(result, expected_data)
        call_args = self.mock_requests.request.call_args
        self.assertEqual(call_args[0][0], "GET")
        self.assertIn("/report/view/report-123", call_args[0][1])

    def test_report_delete_unit(self):
        """Test report deletion."""
        self._mock_response({"status": "deleted"})
        
        result = self.sdk.report.delete("report-123")
        
        self.assertTrue(result)
        call_args = self.mock_requests.request.call_args
        self.assertEqual(call_args[0][0], "DELETE")
        self.assertIn("/report/delete/report-123", call_args[0][1])

    def test_report_supported_unit(self):
        """Test supported file types."""
        expected_data = {"supported": ["npm", "pypi", "cargo", "maven"]}
        self._mock_response(expected_data)
        
        result = self.sdk.report.supported()
        
        self.assertEqual(result, expected_data)
        call_args = self.mock_requests.request.call_args
        self.assertEqual(call_args[0][0], "GET")
        self.assertIn("/report/supported", call_args[0][1])

    # Settings endpoints
    def test_settings_get_unit(self):
        """Test settings retrieval."""
        expected_data = {"settings": {"notifications": True, "theme": "dark"}}
        self._mock_response(expected_data)
        
        result = self.sdk.settings.get("test-org")
        
        self.assertEqual(result, expected_data)
        call_args = self.mock_requests.request.call_args
        self.assertEqual(call_args[0][0], "GET")
        self.assertIn("/orgs/test-org/settings", call_args[0][1])

    # Triage endpoints
    def test_triage_list_alert_triage_unit(self):
        """Test alert triage listing."""
        expected_data = {"alerts": [{"id": "alert-1", "status": "open"}]}
        self._mock_response(expected_data)
        
        result = self.sdk.triage.list_alert_triage("test-org")
        
        self.assertEqual(result, expected_data)
        call_args = self.mock_requests.request.call_args
        self.assertEqual(call_args[0][0], "GET")
        self.assertIn("/orgs/test-org/triage/alerts", call_args[0][1])

    def test_triage_update_alert_triage_unit(self):
        """Test alert triage updating."""
        expected_data = {"result": "Updated"}
        self._mock_response(expected_data)
        
        data = {"alertTriage": [{"alertKey": "alert-123", "state": "ignore", "note": "Not applicable"}]}
        result = self.sdk.triage.update_alert_triage("test-org", data)
        
        self.assertEqual(result, expected_data)
        call_args = self.mock_requests.request.call_args
        self.assertEqual(call_args[0][0], "POST")
        self.assertIn("/orgs/test-org/triage/alerts", call_args[0][1])

    # New endpoints
    def test_threatfeed_get_unit(self):
        """Test threatfeed endpoint."""
        expected_data = {"results": [{"id": "threat-1", "type": "malware"}], "nextPage": None}
        self._mock_response(expected_data)
        
        result = self.sdk.threatfeed.get("test-org")
        
        self.assertEqual(result, expected_data)
        call_args = self.mock_requests.request.call_args
        self.assertEqual(call_args[0][0], "GET")
        self.assertIn("/orgs/test-org/threat-feed", call_args[0][1])

    def test_analytics_get_org_unit(self):
        """Test analytics organization endpoint."""
        expected_data = [{"date": "2025-01-01", "count": 5}]
        self._mock_response(expected_data)
        
        result = self.sdk.analytics.get_org("dependencies")
        
        self.assertEqual(result, expected_data)
        call_args = self.mock_requests.request.call_args
        self.assertEqual(call_args[0][0], "GET")
        self.assertIn("/analytics/org/dependencies", call_args[0][1])

    def test_analytics_get_repo_unit(self):
        """Test analytics repository endpoint."""
        expected_data = [{"date": "2025-01-01", "count": 3}]
        self._mock_response(expected_data)
        
        result = self.sdk.analytics.get_repo("test-repo", "alerts")
        
        self.assertEqual(result, expected_data)
        call_args = self.mock_requests.request.call_args
        self.assertEqual(call_args[0][0], "GET")
        self.assertIn("/analytics/repo/test-repo/alerts", call_args[0][1])

    def test_apitokens_create_unit(self):
        """Test API token creation."""
        expected_data = {"id": "token-123", "name": "test-token", "token": "sk_test_..."}
        self._mock_response(expected_data, 201)
        
        result = self.sdk.apitokens.create("test-org", name="test-token")
        
        self.assertEqual(result, expected_data)
        call_args = self.mock_requests.request.call_args
        self.assertEqual(call_args[0][0], "POST")
        self.assertIn("/orgs/test-org/api-tokens", call_args[0][1])

    def test_apitokens_update_unit(self):
        """Test API token updating."""
        expected_data = {"id": "token-123", "name": "updated-token"}
        self._mock_response(expected_data)
        
        result = self.sdk.apitokens.update("test-org", token_id="token-123", name="updated-token")
        
        self.assertEqual(result, expected_data)
        call_args = self.mock_requests.request.call_args
        self.assertEqual(call_args[0][0], "PUT")
        self.assertIn("/orgs/test-org/api-tokens/token-123", call_args[0][1])

    def test_apitokens_list_unit(self):
        """Test API token listing."""
        expected_data = {"tokens": [{"id": "token-1", "name": "prod-token"}]}
        self._mock_response(expected_data)
        
        result = self.sdk.apitokens.list("test-org")
        
        self.assertEqual(result, expected_data)
        call_args = self.mock_requests.request.call_args
        self.assertEqual(call_args[0][0], "GET")
        self.assertIn("/orgs/test-org/api-tokens", call_args[0][1])

    def test_auditlog_get_unit(self):
        """Test audit log retrieval."""
        expected_data = {"logs": [{"id": "log-1", "action": "user.login"}]}
        self._mock_response(expected_data)
        
        result = self.sdk.auditlog.get("test-org")
        
        self.assertEqual(result, expected_data)
        call_args = self.mock_requests.request.call_args
        self.assertEqual(call_args[0][0], "GET")
        self.assertIn("/orgs/test-org/audit-log", call_args[0][1])

    def test_alerttypes_get_unit(self):
        """Test alert types retrieval."""
        expected_data = {"alertTypes": [{"id": "security", "name": "Security Alert"}]}
        self._mock_response(expected_data)
        
        result = self.sdk.alerttypes.get()
        
        self.assertEqual(result, expected_data)
        call_args = self.mock_requests.request.call_args
        self.assertEqual(call_args[0][0], "POST")
        self.assertIn("/alert-types", call_args[0][1])

    def test_labels_get_unit(self):
        """Test labels get endpoint."""
        expected_data = {"id": "1", "name": "environment", "created_at": "2025-01-01"}
        self._mock_response(expected_data)
        
        result = self.sdk.labels.get("test-org", "1")
        
        self.assertEqual(result, expected_data)
        call_args = self.mock_requests.request.call_args
        self.assertEqual(call_args[0][0], "GET")
        self.assertIn("/orgs/test-org/repos/labels/1", call_args[0][1])

    def test_labels_setting_put_unit(self):
        """Test labels setting put endpoint."""
        expected_data = {"updated": True}
        self._mock_response(expected_data, 201)  # Label settings return 201
        
        label_data = {"environment": {"production": {"critical": "true"}}}
        result = self.sdk.labels.setting.put("test-org", 1, label_data)
        
        self.assertEqual(result, expected_data)
        call_args = self.mock_requests.request.call_args
        self.assertEqual(call_args[0][0], "PUT")
        self.assertIn("/orgs/test-org/repos/labels/1/label-setting", call_args[0][1])

    def test_labels_delete_unit(self):
        """Test labels delete endpoint."""
        expected_data = {"deleted": True}
        self._mock_response(expected_data)
        
        result = self.sdk.labels.delete("test-org", "1")
        
        self.assertEqual(result, expected_data)
        call_args = self.mock_requests.request.call_args
        self.assertEqual(call_args[0][0], "DELETE")
        self.assertIn("/orgs/test-org/repos/labels/1", call_args[0][1])

    # License metadata only supports POST method per OpenAPI spec, no GET method available
    # def test_licensemetadata_get_unit(self):
    #     """Test license metadata retrieval."""
    #     expected_data = {"licenses": [{"id": "MIT", "name": "MIT License"}]}
    #     self._mock_response(expected_data)
    #     
    #     result = self.sdk.licensemetadata.get()
    #     
    #     self.assertEqual(result, expected_data)
    #     call_args = self.mock_requests.request.call_args
    #     self.assertEqual(call_args[0][0], "GET")
    #     self.assertIn("/license-metadata", call_args[0][1])


if __name__ == "__main__":
    unittest.main()
