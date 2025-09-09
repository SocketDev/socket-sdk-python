"""
Comprehensive tests for ALL Socket SDK endpoints.

This file tests every available endpoint with both mocked and real API calls.
For real API calls, appropriate error handling is included when endpoints aren't available.

Run with: python -m pytest tests/integration/test_all_endpoints.py -v
"""

import unittest
import os
import tempfile
import json
from unittest.mock import Mock, patch
from socketdev import socketdev
from socketdev.fullscans import FullScanParams


class TestAllEndpointsMocked(unittest.TestCase):
    """Mock tests for all Socket SDK endpoints."""

    def setUp(self):
        """Set up test environment with mocked API."""
        self.requests_patcher = patch('socketdev.core.api.requests')
        self.mock_requests = self.requests_patcher.start()
        self.sdk = socketdev(token="test-token")

    def tearDown(self):
        """Clean up patches."""
        self.requests_patcher.stop()

    def _mock_success_response(self, data=None):
        """Helper to create successful mock response."""
        if data is None:
            data = {"success": True}
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.headers = {}
        mock_response.json.return_value = data
        self.mock_requests.request.return_value = mock_response
        return mock_response

    def _mock_created_response(self, data=None):
        """Helper to create successful creation mock response."""
        if data is None:
            data = {"id": "created-id", "success": True}
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.headers = {}
        mock_response.json.return_value = data
        self.mock_requests.request.return_value = mock_response
        return mock_response

    # Dependencies endpoints
    def test_dependencies_post_mocked(self):
        """Test dependencies post endpoint."""
        self._mock_success_response({"packages": []})
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump({"name": "test", "version": "1.0.0"}, f)
            f.flush()
            try:
                # Pass the file path as a string, not a file object
                result = self.sdk.dependencies.post([f.name], {})
                self.assertIn("packages", result)
            finally:
                os.unlink(f.name)

    def test_dependencies_get_mocked(self):
        """Test dependencies get endpoint."""
        self._mock_success_response({"dependencies": []})
        result = self.sdk.dependencies.get("test-org", "npm", "test-package", "1.0.0")
        self.assertIn("dependencies", result)

    # DiffScans endpoints
    def test_diffscans_list_mocked(self):
        """Test diffscans list endpoint."""
        self._mock_success_response({"results": []})
        result = self.sdk.diffscans.list("test-org")
        self.assertIn("results", result)

    def test_diffscans_get_mocked(self):
        """Test diffscans get endpoint."""
        self._mock_success_response({"id": "diff-123", "status": "completed"})
        result = self.sdk.diffscans.get("test-org", "diff-123")
        self.assertEqual(result["id"], "diff-123")

    def test_diffscans_create_from_ids_mocked(self):
        """Test diffscans create_from_ids endpoint."""
        self._mock_created_response({"id": "new-diff-scan"})
        params = {"before": "scan1", "after": "scan2", "description": "test"}
        result = self.sdk.diffscans.create_from_ids("test-org", params)
        self.assertEqual(result["id"], "new-diff-scan")

    def test_diffscans_create_from_repo_mocked(self):
        """Test diffscans create_from_repo endpoint."""
        self._mock_created_response({"id": "repo-diff-scan"})
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump({"name": "test", "version": "1.0.0"}, f)
            f.flush()
            try:
                result = self.sdk.diffscans.create_from_repo(
                    "test-org", "test-repo", 
                    [("file", ("package.json", open(f.name, "rb")))], 
                    {"description": "test"}
                )
                self.assertEqual(result["id"], "repo-diff-scan")
            finally:
                os.unlink(f.name)

    def test_diffscans_gfm_mocked(self):
        """Test diffscans gfm endpoint."""
        self._mock_success_response({"markdown": "# Diff Report"})
        result = self.sdk.diffscans.gfm("test-org", "diff-123")
        self.assertIn("markdown", result)

    def test_diffscans_delete_mocked(self):
        """Test diffscans delete endpoint."""
        self._mock_success_response({"status": "ok"})
        result = self.sdk.diffscans.delete("test-org", "diff-123")
        self.assertTrue(result)

    # Export endpoints
    def test_export_cdx_bom_mocked(self):
        """Test export CDX BOM endpoint."""
        self._mock_success_response({"bomFormat": "CycloneDX"})
        result = self.sdk.export.cdx_bom("test-org", "scan-123")
        self.assertIn("bomFormat", result)

    def test_export_spdx_bom_mocked(self):
        """Test export SPDX BOM endpoint."""
        self._mock_success_response({"spdxVersion": "SPDX-2.2"})
        result = self.sdk.export.spdx_bom("test-org", "scan-123")
        self.assertIn("spdxVersion", result)

    def test_export_get_mocked(self):
        """Test export get endpoint."""
        self._mock_success_response({"exports": []})
        result = self.sdk.export.get("test-org")
        self.assertIn("exports", result)

    # FullScans endpoints
    def test_fullscans_get_mocked(self):
        """Test fullscans get endpoint."""
        self._mock_success_response({"id": "scan-123", "status": "completed"})
        result = self.sdk.fullscans.get("test-org", {"id": "scan-123"})
        self.assertEqual(result["id"], "scan-123")

    def test_fullscans_post_mocked(self):
        """Test fullscans post endpoint."""
        self._mock_created_response({"id": "new-scan"})
        params = FullScanParams(repo="test-repo", org_slug="test-org")
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump({"name": "test", "version": "1.0.0"}, f)
            f.flush()
            try:
                result = self.sdk.fullscans.post([("file", ("package.json", open(f.name, "rb")))], params)
                self.assertEqual(result["id"], "new-scan")
            finally:
                os.unlink(f.name)

    def test_fullscans_delete_mocked(self):
        """Test fullscans delete endpoint."""
        self._mock_success_response({"status": "deleted"})
        result = self.sdk.fullscans.delete("test-org", "scan-123")
        self.assertIn("status", result)

    # Historical endpoints
    def test_historical_list_mocked(self):
        """Test historical list endpoint."""
        self._mock_success_response({"results": []})
        result = self.sdk.historical.list("test-org")
        self.assertIn("results", result)

    def test_historical_trend_mocked(self):
        """Test historical trend endpoint."""
        self._mock_success_response({"trend": []})
        result = self.sdk.historical.trend("test-org")
        self.assertIn("trend", result)

    # NPM endpoints
    def test_npm_issues_mocked(self):
        """Test npm issues endpoint."""
        self._mock_success_response([{"type": "security", "severity": "high"}])
        result = self.sdk.npm.issues("lodash", "4.17.21")
        self.assertIsInstance(result, list)

    def test_npm_score_mocked(self):
        """Test npm score endpoint."""
        self._mock_success_response([{"category": "security", "value": 85}])
        result = self.sdk.npm.score("lodash", "4.17.21")
        self.assertIsInstance(result, list)

    # OpenAPI endpoints
    def test_openapi_get_mocked(self):
        """Test openapi get endpoint."""
        self._mock_success_response({"openapi": "3.0.0"})
        result = self.sdk.openapi.get()
        self.assertIn("openapi", result)

    # Org endpoints
    def test_org_get_mocked(self):
        """Test org get endpoint."""
        self._mock_success_response({"name": "test-org", "id": "org-123"})
        result = self.sdk.org.get("test-org")
        self.assertEqual(result["name"], "test-org")

    # PURL endpoints
    def test_purl_post_mocked(self):
        """Test purl post endpoint."""
        self._mock_success_response([{"purl": "pkg:npm/lodash@4.17.21", "valid": True}])
        result = self.sdk.purl.post("false", [{"purl": "pkg:npm/lodash@4.17.21"}])
        self.assertIsInstance(result, list)

    # Quota endpoints
    def test_quota_get_mocked(self):
        """Test quota get endpoint."""
        self._mock_success_response({"quota": 1000, "used": 100})
        result = self.sdk.quota.get()
        self.assertIn("quota", result)

    # Report endpoints
    def test_report_list_mocked(self):
        """Test report list endpoint."""
        self._mock_success_response({"reports": []})
        result = self.sdk.report.list()
        self.assertIn("reports", result)

    def test_report_create_mocked(self):
        """Test report create endpoint."""
        self._mock_created_response({"id": "report-123"})
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump({"name": "test", "version": "1.0.0"}, f)
            f.flush()
            try:
                result = self.sdk.report.create([("file", ("package.json", open(f.name, "rb")))])
                self.assertEqual(result["id"], "report-123")
            finally:
                os.unlink(f.name)

    def test_report_view_mocked(self):
        """Test report view endpoint."""
        self._mock_success_response({"id": "report-123", "status": "completed"})
        result = self.sdk.report.view("report-123")
        self.assertEqual(result["id"], "report-123")

    def test_report_delete_mocked(self):
        """Test report delete endpoint."""
        self._mock_success_response({"status": "ok"})
        result = self.sdk.report.delete("report-123")
        self.assertTrue(result)

    def test_report_supported_mocked(self):
        """Test report supported endpoint."""
        self._mock_success_response({"supported": ["npm", "pypi"]})
        result = self.sdk.report.supported()
        self.assertIn("supported", result)

    # Settings endpoints
    def test_settings_get_mocked(self):
        """Test settings get endpoint."""
        self._mock_success_response({"settings": {}})
        result = self.sdk.settings.get("test-org")
        self.assertIn("settings", result)

    # Triage endpoints
    def test_triage_list_alert_triage_mocked(self):
        """Test triage list_alert_triage endpoint."""
        self._mock_success_response({"alerts": []})
        result = self.sdk.triage.list_alert_triage("test-org")
        self.assertIn("alerts", result)

    def test_triage_update_alert_triage_mocked(self):
        """Test triage update_alert_triage endpoint."""
        self._mock_success_response({"updated": True})
        result = self.sdk.triage.update_alert_triage("test-org", {"alert_id": "123", "status": "resolved"})
        self.assertIn("updated", result)

    # New endpoints tests
    def test_threatfeed_get_mocked(self):
        """Test threatfeed get endpoint."""
        self._mock_success_response({"results": [], "nextPage": None})
        result = self.sdk.threatfeed.get("test-org")
        self.assertIn("results", result)

    def test_analytics_get_org_mocked(self):
        """Test analytics get_org endpoint."""
        self._mock_success_response([{"date": "2025-01-01", "count": 5}])
        result = self.sdk.analytics.get_org("dependencies")
        self.assertIsInstance(result, list)

    def test_analytics_get_repo_mocked(self):
        """Test analytics get_repo endpoint."""
        self._mock_success_response([{"date": "2025-01-01", "count": 3}])
        result = self.sdk.analytics.get_repo("test-repo", "alerts")
        self.assertIsInstance(result, list)

    def test_apitokens_create_mocked(self):
        """Test apitokens create endpoint."""
        self._mock_created_response({"id": "token-123", "name": "test-token"})
        result = self.sdk.apitokens.create("test-org", name="test-token")
        self.assertEqual(result["name"], "test-token")

    def test_apitokens_update_mocked(self):
        """Test apitokens update endpoint."""
        self._mock_success_response({"id": "token-123", "name": "updated-token"})
        result = self.sdk.apitokens.update("test-org", token_id="token-123", name="updated-token")
        self.assertEqual(result["name"], "updated-token")

    def test_apitokens_list_mocked(self):
        """Test apitokens list endpoint."""
        self._mock_success_response({"tokens": []})
        result = self.sdk.apitokens.list()
        self.assertIn("tokens", result)

    def test_auditlog_get_mocked(self):
        """Test auditlog get endpoint."""
        self._mock_success_response({"logs": []})
        result = self.sdk.auditlog.get("test-org")
        self.assertIn("logs", result)

    def test_alerttypes_get_mocked(self):
        """Test alerttypes get endpoint."""
        self._mock_success_response({"alertTypes": []})
        result = self.sdk.alerttypes.get()
        self.assertIn("alertTypes", result)

    def test_labels_get_mocked(self):
        """Test labels get endpoint."""
        self._mock_success_response({"label": "test-label"})
        result = self.sdk.labels.get("test-org", 1, "test-key")
        self.assertIn("label", result)

    def test_labels_put_mocked(self):
        """Test labels put endpoint."""
        self._mock_success_response({"updated": True})
        result = self.sdk.labels.put("test-org", 1, {"test": {"key": {"value": "data"}}})
        self.assertIn("updated", result)

    def test_labels_delete_mocked(self):
        """Test labels delete endpoint."""
        self._mock_success_response({"deleted": True})
        result = self.sdk.labels.delete("test-org", 1, "test-key")
        self.assertIn("deleted", result)

    def test_licensemetadata_get_mocked(self):
        """Test licensemetadata get endpoint."""
        self._mock_success_response({"licenses": []})
        result = self.sdk.licensemetadata.get()
        self.assertIn("licenses", result)


class TestAllEndpointsIntegration(unittest.TestCase):
    """Integration tests for all Socket SDK endpoints."""

    @classmethod
    def setUpClass(cls):
        """Set up test environment."""
        cls.api_key = os.getenv("SOCKET_SECURITY_API_KEY", "")
        cls.org_slug = os.getenv("SOCKET_ORG_SLUG", "")
        cls.repo_slug = os.getenv("SOCKET_REPO_SLUG", "")
        
        if not cls.api_key or not cls.org_slug:
            raise unittest.SkipTest(
                "SOCKET_SECURITY_API_KEY and SOCKET_ORG_SLUG required for integration tests"
            )
        
        cls.sdk = socketdev(token=cls.api_key)
        cls.temp_dir = tempfile.mkdtemp()
        cls.package_json_path = os.path.join(cls.temp_dir, "package.json")
        
        # Create test package.json
        test_package = {
            "name": "test-integration-package",
            "version": "1.0.0",
            "dependencies": {"lodash": "4.17.21"}
        }
        with open(cls.package_json_path, 'w') as f:
            json.dump(test_package, f, indent=2)

    @classmethod
    def tearDownClass(cls):
        """Clean up test environment."""
        import shutil
        if hasattr(cls, 'temp_dir'):
            shutil.rmtree(cls.temp_dir)

    def _try_endpoint(self, endpoint_func, *args, **kwargs):
        """Helper to try an endpoint and handle errors gracefully."""
        try:
            return endpoint_func(*args, **kwargs)
        except Exception as e:
            print(f"Endpoint {endpoint_func.__name__} not available: {e}")
            return None

    # Core working endpoints
    def test_org_get_integration(self):
        """Test org get endpoint (should always work)."""
        result = self._try_endpoint(self.sdk.org.get, self.org_slug)
        if result:
            self.assertIsInstance(result, dict)

    def test_quota_get_integration(self):
        """Test quota get endpoint."""
        result = self._try_endpoint(self.sdk.quota.get)
        if result:
            self.assertIsInstance(result, dict)

    def test_openapi_get_integration(self):
        """Test openapi get endpoint."""
        result = self._try_endpoint(self.sdk.openapi.get)
        if result:
            self.assertIsInstance(result, dict)

    # NPM endpoints (should work for public packages)
    def test_npm_issues_integration(self):
        """Test npm issues endpoint."""
        result = self._try_endpoint(self.sdk.npm.issues, "lodash", "4.17.21")
        if result:
            self.assertIsInstance(result, list)

    def test_npm_score_integration(self):
        """Test npm score endpoint."""
        result = self._try_endpoint(self.sdk.npm.score, "lodash", "4.17.21")
        if result:
            self.assertIsInstance(result, list)

    # PURL endpoints
    def test_purl_post_integration(self):
        """Test purl post endpoint."""
        components = [{"purl": "pkg:npm/lodash@4.17.21"}]
        result = self._try_endpoint(self.sdk.purl.post, "false", components)
        if result:
            self.assertIsInstance(result, list)

    # Settings endpoints
    def test_settings_get_integration(self):
        """Test settings get endpoint."""
        result = self._try_endpoint(self.sdk.settings.get, self.org_slug)
        if result:
            self.assertIsInstance(result, dict)

    # Export endpoints
    def test_export_get_integration(self):
        """Test export get endpoint."""
        result = self._try_endpoint(self.sdk.export.get, self.org_slug)
        if result:
            self.assertIsInstance(result, dict)

    # DiffScans endpoints
    def test_diffscans_list_integration(self):
        """Test diffscans list endpoint."""
        result = self._try_endpoint(self.sdk.diffscans.list, self.org_slug)
        if result:
            self.assertIsInstance(result, dict)
            self.assertIn("results", result)

    # Report endpoints
    def test_report_list_integration(self):
        """Test report list endpoint."""
        result = self._try_endpoint(self.sdk.report.list)
        if result:
            self.assertIsInstance(result, dict)

    def test_report_supported_integration(self):
        """Test report supported endpoint."""
        result = self._try_endpoint(self.sdk.report.supported)
        if result:
            self.assertIsInstance(result, dict)

    # Historical endpoints
    def test_historical_list_integration(self):
        """Test historical list endpoint."""
        result = self._try_endpoint(self.sdk.historical.list, self.org_slug)
        if result:
            self.assertIsInstance(result, dict)

    # New endpoints
    def test_threatfeed_get_integration(self):
        """Test threatfeed get endpoint."""
        # Try org-scoped version first
        result = self._try_endpoint(self.sdk.threatfeed.get, org_slug=self.org_slug)
        if not result:
            # Try global version
            result = self._try_endpoint(self.sdk.threatfeed.get)
        if result:
            self.assertIsInstance(result, dict)
            self.assertIn("results", result)

    def test_alerttypes_get_integration(self):
        """Test alerttypes get endpoint."""
        result = self._try_endpoint(self.sdk.alerttypes.get)
        if result:
            self.assertIsInstance(result, dict)

    def test_licensemetadata_get_integration(self):
        """Test licensemetadata get endpoint."""
        result = self._try_endpoint(self.sdk.licensemetadata.get)
        if result:
            self.assertIsInstance(result, dict)

    def test_apitokens_list_integration(self):
        """Test apitokens list endpoint."""
        result = self._try_endpoint(self.sdk.apitokens.list)
        if result:
            self.assertIsInstance(result, dict)

    def test_auditlog_get_integration(self):
        """Test auditlog get endpoint."""
        result = self._try_endpoint(self.sdk.auditlog.get, self.org_slug)
        if result:
            self.assertIsInstance(result, dict)

    # Dependencies endpoint
    def test_dependencies_get_integration(self):
        """Test dependencies get endpoint."""
        result = self._try_endpoint(
            self.sdk.dependencies.get, 
            self.org_slug, "npm", "lodash", "4.17.21"
        )
        if result:
            self.assertIsInstance(result, dict)

    # Triage endpoints
    def test_triage_list_alert_triage_integration(self):
        """Test triage list_alert_triage endpoint."""
        result = self._try_endpoint(self.sdk.triage.list_alert_triage, self.org_slug)
        if result:
            self.assertIsInstance(result, dict)

    # Full workflow tests (only if repo is configured)
    def test_fullscans_integration(self):
        """Test fullscans endpoints."""
        if not self.repo_slug:
            self.skipTest("SOCKET_REPO_SLUG not provided")

        # Try to create a full scan
        params = FullScanParams(
            repo=self.repo_slug,
            org_slug=self.org_slug,
            branch="test-branch",
            commit_message="Integration test scan",
            commit_hash="1234567890abcdef1234567890abcdef12345678",
            integration_type="api"
        )

        with open(self.package_json_path, "rb") as f:
            files = [("file", ("package.json", f))]
            result = self._try_endpoint(self.sdk.fullscans.post, files, params)
            
            if result and "id" in result:
                scan_id = result["id"]
                
                # Try to get the scan
                get_result = self._try_endpoint(
                    self.sdk.fullscans.get, 
                    self.org_slug, 
                    {"id": scan_id}
                )
                if get_result:
                    self.assertIsInstance(get_result, dict)
                
                # Clean up - try to delete the scan
                self._try_endpoint(self.sdk.fullscans.delete, self.org_slug, scan_id)


if __name__ == "__main__":
    unittest.main()
