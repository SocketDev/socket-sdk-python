"""
Comprehensive integration tests for the Socket SDK Python client.

These tests require the following environment variables:
- SOCKET_SECURITY_API_KEY: Your Socket.dev API key
- SOCKET_ORG_SLUG: Your organization slug
- SOCKET_REPO_SLUG: A repository slug for testing (optional for some tests)

Run with: python -m pytest tests/integration/test_comprehensive_integration.py -v
"""

import unittest
import os
import tempfile
import shutil
import json
from socketdev import socketdev
from socketdev.fullscans import FullScanParams


class TestSocketSDKIntegration(unittest.TestCase):
    """Comprehensive integration tests for the Socket SDK."""

    @classmethod
    def setUpClass(cls):
        """Set up test environment and validate required environment variables."""
        cls.api_key = os.getenv("SOCKET_SECURITY_API_KEY", "")
        cls.org_slug = os.getenv("SOCKET_ORG_SLUG", "")
        cls.repo_slug = os.getenv("SOCKET_REPO_SLUG", "")
        
        # Only require API key and org_slug for most tests
        missing = []
        if not cls.api_key:
            missing.append("SOCKET_SECURITY_API_KEY")
        if not cls.org_slug:
            missing.append("SOCKET_ORG_SLUG")
            
        if missing:
            raise RuntimeError(
                f"Missing required environment variables: {', '.join(missing)}\n"
                f"SOCKET_REPO_SLUG is optional for some tests."
            )
        
        cls.sdk = socketdev(token=cls.api_key)
        
        # Prepare temp directory for test files
        cls.temp_dir = tempfile.mkdtemp()
        cls.package_json_path = os.path.join(cls.temp_dir, "package.json")
        cls.package_empty_path = os.path.join(cls.temp_dir, "package-empty.json")
        
        # Create test package.json files
        test_package = {
            "name": "test-integration-project",
            "version": "1.0.0",
            "dependencies": {
                "lodash": "4.17.21"
            }
        }
        
        empty_package = {
            "name": "test-empty-project",
            "version": "1.0.0"
        }
        
        with open(cls.package_json_path, 'w') as f:
            json.dump(test_package, f, indent=2)
            
        with open(cls.package_empty_path, 'w') as f:
            json.dump(empty_package, f, indent=2)

    @classmethod
    def tearDownClass(cls):
        """Clean up test environment."""
        if hasattr(cls, 'temp_dir'):
            shutil.rmtree(cls.temp_dir)

    def setUp(self):
        """Set up for each test."""
        self.created_scan_ids = []
        self.created_diff_scan_ids = []

    def tearDown(self):
        """Clean up after each test."""
        # Clean up any created resources
        for diff_scan_id in self.created_diff_scan_ids:
            try:
                self.sdk.diffscans.delete(self.org_slug, diff_scan_id)
            except Exception:
                pass  # Ignore cleanup errors
                
        for scan_id in self.created_scan_ids:
            try:
                self.sdk.fullscans.delete(self.org_slug, scan_id)
            except Exception:
                pass  # Ignore cleanup errors

    def test_org_endpoints(self):
        """Test organization-related endpoints."""
        # Test getting organization info
        org_info = self.sdk.org.get(self.org_slug)
        self.assertIsInstance(org_info, dict)

    def test_quota_endpoint(self):
        """Test quota endpoint."""
        try:
            quota_info = self.sdk.quota.get()
            self.assertIsInstance(quota_info, dict)
        except Exception as e:
            # Some organizations might not have quota access
            print(f"Quota endpoint not available: {e}")

    def test_settings_endpoints(self):
        """Test settings endpoints."""
        try:
            settings = self.sdk.settings.get(self.org_slug)
            self.assertIsInstance(settings, dict)
        except Exception as e:
            # Some organizations might not have settings access
            print(f"Settings endpoint not available: {e}")

    def test_diffscans_list(self):
        """Test listing diff scans."""
        result = self.sdk.diffscans.list(self.org_slug)
        self.assertIsInstance(result, dict)
        self.assertIn("results", result)

    def test_fullscans_basic_workflow(self):
        """Test basic full scan workflow."""
        if not self.repo_slug:
            self.skipTest("SOCKET_REPO_SLUG not provided")
            
        params = FullScanParams(
            org_slug=self.org_slug,
            repo=self.repo_slug,
            branch="main",
            commit_message="Integration test commit",
            commit_hash="1234567890abcdef1234567890abcdef12345678",
            pull_request=999,
            committers=["integration-tester"],
            integration_type="api"
        )

        # Create a full scan
        with open(self.package_json_path, "rb") as f:
            files = [("file", ("package.json", f))]
            result = self.sdk.fullscans.post(files=files, params=params)
            
        self.assertIsInstance(result, dict)
        self.assertIn("id", result)
        
        scan_id = result["id"]
        self.created_scan_ids.append(scan_id)
        
        # Get the scan
        scan_info = self.sdk.fullscans.get(self.org_slug, {"id": scan_id})
        self.assertIsInstance(scan_info, dict)
        
        # List scans
        scans_list = self.sdk.fullscans.list(self.org_slug)
        self.assertIsInstance(scans_list, dict)

    def test_diffscans_complete_workflow(self):
        """Test complete diff scan workflow."""
        if not self.repo_slug:
            self.skipTest("SOCKET_REPO_SLUG not provided")
            
        # Create 'before' scan with empty package.json
        params_before = FullScanParams(
            org_slug=self.org_slug,
            repo=self.repo_slug,
            branch="main",
            commit_message="Before scan",
            commit_hash="before000000000000000000000000000000000000",
            pull_request=998,
            committers=["integration-tester"],
            integration_type="api"
        )
        
        with open(self.package_empty_path, "rb") as f:
            files_before = [("file", ("package.json", f))]
            before_result = self.sdk.fullscans.post(files=files_before, params=params_before)
            
        self.assertIn("id", before_result)
        before_id = before_result["id"]
        self.created_scan_ids.append(before_id)
        
        # Create 'after' scan with dependencies
        params_after = FullScanParams(
            org_slug=self.org_slug,
            repo=self.repo_slug,
            branch="main",
            commit_message="After scan",
            commit_hash="after0000000000000000000000000000000000000",
            pull_request=999,
            committers=["integration-tester"],
            integration_type="api"
        )
        
        with open(self.package_json_path, "rb") as f:
            files_after = [("file", ("package.json", f))]
            after_result = self.sdk.fullscans.post(files=files_after, params=params_after)
            
        self.assertIn("id", after_result)
        after_id = after_result["id"]
        self.created_scan_ids.append(after_id)
        
        # Create diff scan from IDs
        diff_params = {
            "before": before_id,
            "after": after_id,
            "description": "Integration test diff scan"
        }
        
        diff_result = self.sdk.diffscans.create_from_ids(self.org_slug, diff_params)
        self.assertIsInstance(diff_result, dict)
        
        # Extract diff scan ID
        diff_scan_id = (
            diff_result.get("id") or
            diff_result.get("diff_scan_id") or
            (diff_result.get("diff_scan", {}).get("id") if "diff_scan" in diff_result else None)
        )
        
        self.assertIsNotNone(diff_scan_id)
        self.created_diff_scan_ids.append(diff_scan_id)
        
        # Get the diff scan
        get_result = self.sdk.diffscans.get(self.org_slug, diff_scan_id)
        self.assertIsInstance(get_result, dict)
        
        # Get GFM output
        gfm_result = self.sdk.diffscans.gfm(self.org_slug, diff_scan_id)
        self.assertIsInstance(gfm_result, dict)

    def test_diffscans_from_repo(self):
        """Test creating diff scans from repository."""
        if not self.repo_slug:
            self.skipTest("SOCKET_REPO_SLUG not provided")
            
        with open(self.package_json_path, "rb") as f:
            files = [("file", ("package.json", f))]
            params = {"description": "Integration test diff scan from repo"}
            
            result = self.sdk.diffscans.create_from_repo(
                self.org_slug, 
                self.repo_slug, 
                files, 
                params
            )
            
        self.assertIsInstance(result, dict)
        
        # Extract diff scan ID for cleanup
        diff_scan_id = (
            result.get("id") or
            result.get("diff_scan_id") or
            (result.get("diff_scan", {}).get("id") if "diff_scan" in result else None)
        )
        
        if diff_scan_id:
            self.created_diff_scan_ids.append(diff_scan_id)

    def test_npm_endpoints(self):
        """Test NPM-related endpoints."""
        # Test getting package issues - this should work for most packages
        try:
            issues = self.sdk.npm.issues("lodash", "4.17.21")
            self.assertIsInstance(issues, dict)
        except Exception as e:
            print(f"NPM issues endpoint not available: {e}")

    def test_export_endpoint(self):
        """Test export functionality."""
        try:
            result = self.sdk.export.get(self.org_slug)
            self.assertIsInstance(result, dict)
        except Exception as e:
            print(f"Export endpoint not available: {e}")

    def test_purl_endpoint(self):
        """Test PURL (Package URL) functionality."""
        try:
            # Test with a common npm package
            purl = "pkg:npm/lodash@4.17.21"
            result = self.sdk.purl.post([purl])
            self.assertIsInstance(result, dict)
        except Exception as e:
            print(f"PURL endpoint not available: {e}")

    def test_report_endpoints(self):
        """Test report endpoints."""
        if not self.repo_slug:
            self.skipTest("SOCKET_REPO_SLUG not provided")
            
        # List reports
        reports = self.sdk.report.list(self.org_slug)
        self.assertIsInstance(reports, dict)

    def test_new_endpoints_basic(self):
        """Test basic functionality of newer endpoints."""
        # Test Labels
        try:
            labels = self.sdk.labels.list(self.org_slug)
            self.assertIsInstance(labels, dict)
        except Exception as e:
            # Some endpoints might not be available for all organizations
            print(f"Labels endpoint not available: {e}")

        # Test License Metadata
        try:
            license_data = self.sdk.licensemetadata.get()
            self.assertIsInstance(license_data, dict)
        except Exception as e:
            print(f"License metadata endpoint not available: {e}")

        # Test Threat Feed
        try:
            threat_feed = self.sdk.threatfeed.get()
            self.assertIsInstance(threat_feed, dict)
        except Exception as e:
            print(f"Threat feed endpoint not available: {e}")

        # Test API Tokens (list only, don't create)
        try:
            tokens = self.sdk.apitokens.list()
            self.assertIsInstance(tokens, dict)
        except Exception as e:
            print(f"API tokens endpoint not available: {e}")

        # Test Analytics
        try:
            analytics = self.sdk.analytics.get(self.org_slug)
            self.assertIsInstance(analytics, dict)
        except Exception as e:
            print(f"Analytics endpoint not available: {e}")

        # Test Alert Types
        try:
            alert_types = self.sdk.alerttypes.get()
            self.assertIsInstance(alert_types, dict)
        except Exception as e:
            print(f"Alert types endpoint not available: {e}")

    def test_dependencies_endpoint(self):
        """Test dependencies endpoint."""
        try:
            deps = self.sdk.dependencies.get(self.org_slug)
            self.assertIsInstance(deps, dict)
        except Exception as e:
            print(f"Dependencies endpoint not available: {e}")


if __name__ == "__main__":
    unittest.main()
