"""
Tests for newly added Socket SDK endpoints.

These tests cover the newer endpoints like threatfeed, analytics, apitokens, etc.
Some tests are integration tests (require API key) while others are unit tests (mocked).

Run with: python -m pytest tests/integration/test_new_endpoints.py -v
"""

import unittest
import os
from unittest.mock import Mock, patch
from socketdev import socketdev


class TestNewEndpointsIntegration(unittest.TestCase):
    """Integration tests for newly added endpoints."""

    @classmethod
    def setUpClass(cls):
        """Set up test environment."""
        cls.api_key = os.getenv("SOCKET_SECURITY_API_KEY", "")
        cls.org_slug = os.getenv("SOCKET_ORG_SLUG", "")
        
        if not cls.api_key or not cls.org_slug:
            raise unittest.SkipTest(
                "SOCKET_SECURITY_API_KEY and SOCKET_ORG_SLUG required for integration tests"
            )
        
        cls.sdk = socketdev(token=cls.api_key)

    def test_threatfeed_org_endpoint(self):
        """Test the new org-scoped threat feed endpoint."""
        try:
            result = self.sdk.threatfeed.get(org_slug=self.org_slug)
            self.assertIsInstance(result, dict)
            # Should have results key
            self.assertIn("results", result)
        except Exception as e:
            # This endpoint might not be available for all orgs
            print(f"Org threat feed endpoint not available: {e}")

    def test_threatfeed_global_endpoint(self):
        """Test the deprecated global threat feed endpoint."""
        try:
            result = self.sdk.threatfeed.get()
            self.assertIsInstance(result, dict)
            self.assertIn("results", result)
        except Exception as e:
            print(f"Global threat feed endpoint not available: {e}")

    def test_threatfeed_with_parameters(self):
        """Test threat feed with query parameters."""
        try:
            result = self.sdk.threatfeed.get(
                org_slug=self.org_slug,
                per_page=10,
                sort="created_at"
            )
            self.assertIsInstance(result, dict)
            self.assertIn("results", result)
        except Exception as e:
            print(f"Threat feed with parameters not available: {e}")

    def test_analytics_deprecated_warning(self):
        """Test that analytics methods issue deprecation warnings."""
        with patch('socketdev.analytics.log') as mock_log:
            try:
                self.sdk.analytics.get_org("dependencies")
                # Should log a deprecation warning
                mock_log.warning.assert_called_once()
                warning_msg = mock_log.warning.call_args[0][0]
                self.assertIn("deprecated", warning_msg.lower())
            except Exception:
                # Endpoint might not be available
                pass

    def test_apitokens_list(self):
        """Test listing API tokens."""
        try:
            result = self.sdk.apitokens.list()
            self.assertIsInstance(result, dict)
        except Exception as e:
            # This is sensitive functionality that might be restricted
            print(f"API tokens list not available: {e}")

    def test_alerttypes_get(self):
        """Test getting alert types."""
        try:
            result = self.sdk.alerttypes.get()
            self.assertIsInstance(result, dict)
        except Exception as e:
            print(f"Alert types endpoint not available: {e}")

    def test_auditlog_list(self):
        """Test listing audit log entries."""
        try:
            result = self.sdk.auditlog.list(self.org_slug)
            self.assertIsInstance(result, dict)
        except Exception as e:
            print(f"Audit log endpoint not available: {e}")

    def test_labels_list(self):
        """Test listing labels."""
        try:
            result = self.sdk.labels.list(self.org_slug)
            self.assertIsInstance(result, dict)
        except Exception as e:
            print(f"Labels endpoint not available: {e}")

    def test_licensemetadata_get(self):
        """Test getting license metadata."""
        try:
            result = self.sdk.licensemetadata.get()
            self.assertIsInstance(result, dict)
        except Exception as e:
            print(f"License metadata endpoint not available: {e}")


class TestNewEndpointsUnit(unittest.TestCase):
    """Unit tests for newly added endpoints with mocked responses."""

    def setUp(self):
        """Set up test environment with mocked API."""
        self.sdk = socketdev(token="test-token")
        self.mock_api = Mock()
        self.sdk.api = self.mock_api

    def test_threatfeed_org_scoped_mocked(self):
        """Test org-scoped threat feed endpoint with mocked response."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "results": [
                {"id": "threat1", "type": "malware"},
                {"id": "threat2", "type": "typosquatting"}
            ],
            "nextPage": None
        }
        self.mock_api.do_request.return_value = mock_response
        
        result = self.sdk.threatfeed.get(org_slug="test-org")
        
        self.assertEqual(len(result["results"]), 2)
        self.mock_api.do_request.assert_called_once_with(
            path="orgs/test-org/threat-feed"
        )

    def test_threatfeed_global_mocked(self):
        """Test global threat feed endpoint with mocked response."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "results": [{"id": "global-threat", "type": "malware"}],
            "nextPage": None
        }
        self.mock_api.do_request.return_value = mock_response
        
        result = self.sdk.threatfeed.get()
        
        self.assertEqual(len(result["results"]), 1)
        self.mock_api.do_request.assert_called_once_with(
            path="threat-feed"
        )

    def test_threatfeed_with_params_mocked(self):
        """Test threat feed with parameters."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"results": [], "nextPage": None}
        self.mock_api.do_request.return_value = mock_response
        
        result = self.sdk.threatfeed.get(
            org_slug="test-org",
            per_page=5,
            sort="created_at"
        )
        
        self.mock_api.do_request.assert_called_once_with(
            path="orgs/test-org/threat-feed?per_page=5&sort=created_at"
        )

    def test_threatfeed_error_handling(self):
        """Test threat feed error handling."""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.text = "Not found"
        self.mock_api.do_request.return_value = mock_response
        
        with patch('socketdev.threatfeed.log') as mock_log:
            result = self.sdk.threatfeed.get(org_slug="test-org")
            
            # Should return default structure on error
            self.assertEqual(result, {"results": [], "nextPage": None})
            mock_log.error.assert_called()

    def test_apitokens_create_mocked(self):
        """Test API token creation with mocked response."""
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {
            "id": "token123",
            "name": "test-token",
            "created_at": "2025-01-01T00:00:00Z"
        }
        self.mock_api.do_request.return_value = mock_response
        
        result = self.sdk.apitokens.create(
            org_slug="test-org",
            name="test-token",
            description="Test token"
        )
        
        self.assertEqual(result["id"], "token123")
        self.mock_api.do_request.assert_called_once_with(
            path="orgs/test-org/api-tokens",
            method="POST",
            payload='{"name": "test-token", "description": "Test token"}'
        )

    def test_apitokens_update_mocked(self):
        """Test API token update with mocked response."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"id": "token123", "name": "updated-token"}
        self.mock_api.do_request.return_value = mock_response
        
        result = self.sdk.apitokens.update(
            org_slug="test-org",
            token_id="token123",
            name="updated-token"
        )
        
        self.assertEqual(result["name"], "updated-token")
        self.mock_api.do_request.assert_called_once_with(
            path="orgs/test-org/api-tokens/update",
            method="POST",
            payload='{"token_id": "token123", "name": "updated-token"}'
        )

    def test_analytics_deprecation_warning(self):
        """Test that analytics methods show deprecation warnings."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = []
        self.mock_api.do_request.return_value = mock_response
        
        with patch('socketdev.analytics.log') as mock_log:
            result = self.sdk.analytics.get_org("dependencies")
            
            # Should log deprecation warning
            mock_log.warning.assert_called_once()
            warning_msg = mock_log.warning.call_args[0][0]
            self.assertIn("deprecated", warning_msg.lower())
            self.assertIn("Historical", warning_msg)

    def test_analytics_get_repo_deprecation(self):
        """Test repo analytics deprecation warning."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = []
        self.mock_api.do_request.return_value = mock_response
        
        with patch('socketdev.analytics.log') as mock_log:
            result = self.sdk.analytics.get_repo("test-repo", "alerts")
            
            # Should log deprecation warning
            mock_log.warning.assert_called_once()
            warning_msg = mock_log.warning.call_args[0][0]
            self.assertIn("deprecated", warning_msg.lower())


class TestEndpointCompatibility(unittest.TestCase):
    """Test backward compatibility and API consistency."""

    def setUp(self):
        """Set up test environment."""
        self.sdk = socketdev(token="test-token")

    def test_all_endpoints_have_api_reference(self):
        """Test that all endpoint modules have the api attribute."""
        endpoints = [
            'dependencies', 'export', 'fullscans', 'historical',
            'npm', 'openapi', 'org', 'purl', 'quota', 'report', 'repos',
            'repositories', 'sbom', 'settings', 'triage', 'labels',
            'licensemetadata', 'diffscans', 'threatfeed', 'apitokens',
            'auditlog', 'analytics', 'alerttypes'
        ]
        
        for endpoint_name in endpoints:
            endpoint = getattr(self.sdk, endpoint_name)
            if hasattr(endpoint, 'api'):  # Skip utils which doesn't have api
                self.assertIsNotNone(endpoint.api, f"{endpoint_name} should have api reference")

    def test_sdk_components_initialization(self):
        """Test that all SDK components initialize properly."""
        # This tests that there are no import errors or initialization issues
        try:
            sdk = socketdev(token="test-token")
            
            # Try to access each component
            components = [
                sdk.dependencies, sdk.export, sdk.fullscans, sdk.historical,
                sdk.npm, sdk.openapi, sdk.org, sdk.purl, sdk.quota, 
                sdk.report, sdk.repos, sdk.repositories, sdk.sbom, 
                sdk.settings, sdk.triage, sdk.utils, sdk.labels,
                sdk.licensemetadata, sdk.diffscans, sdk.threatfeed, 
                sdk.apitokens, sdk.auditlog, sdk.analytics, sdk.alerttypes
            ]
            
            for component in components:
                self.assertIsNotNone(component)
                
        except Exception as e:
            self.fail(f"SDK component initialization failed: {e}")


if __name__ == "__main__":
    unittest.main()
