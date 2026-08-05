"""
Unit tests for the SDK exception hierarchy and transient-error classification.

`APIFailure.is_transient_error()` tells consumers whether retrying the same request may
succeed (gateway/connection-level failures: HTTP 408/502/503/504, dropped or reset
connections, client-side timeouts) or whether the failure is deterministic (400/401/403/
404/429 and similar). Classification is based on the `status_code` recorded at raise time
inside `API.do_request`, so these tests cover both the exception classes themselves and
the status codes `do_request` attaches when raising them.

Run with: python -m pytest tests/unit/ -v
"""

import unittest
from unittest.mock import MagicMock, patch

import requests

from socketdev.core.api import API
from socketdev.exceptions import (
    APIAccessDenied,
    APIBadGateway,
    APIConnectionError,
    APIFailure,
    APIInsufficientPermissions,
    APIInsufficientQuota,
    APIOrganizationNotAllowed,
    APIResourceNotFound,
    APITimeout,
)


class TestIsTransientError(unittest.TestCase):
    """Classification of exceptions constructed directly."""

    def test_transient_statuses_on_catch_all_failure(self):
        for status in (408, 502, 503, 504):
            self.assertTrue(APIFailure("boom", status_code=status).is_transient_error())

    def test_deterministic_statuses_on_catch_all_failure(self):
        for status in (400, 401, 403, 404, 422, 429, 500):
            self.assertFalse(APIFailure("boom", status_code=status).is_transient_error())

    def test_no_status_code_is_not_transient(self):
        # The wrapped-unexpected-error case: do_request raises a bare APIFailure().
        self.assertFalse(APIFailure().is_transient_error())
        self.assertFalse(APIFailure("boom").is_transient_error())

    def test_connection_level_classes_are_transient(self):
        self.assertTrue(APITimeout().is_transient_error())
        self.assertTrue(APIConnectionError().is_transient_error())
        self.assertTrue(APIBadGateway().is_transient_error())

    def test_bad_gateway_carries_502_by_default(self):
        self.assertEqual(APIBadGateway().status_code, 502)

    def test_dedicated_4xx_classes_are_not_transient(self):
        self.assertFalse(APIAccessDenied("denied", status_code=401).is_transient_error())
        self.assertFalse(APIInsufficientPermissions(status_code=403).is_transient_error())
        self.assertFalse(APIOrganizationNotAllowed(status_code=403).is_transient_error())
        self.assertFalse(APIInsufficientQuota(status_code=429).is_transient_error())
        self.assertFalse(APIResourceNotFound(status_code=404).is_transient_error())

    def test_subclass_with_transient_status_follows_the_status(self):
        # Classification is by recorded status, not class identity: if a transient status
        # ever gains a dedicated subclass, is_transient_error() keeps working unchanged.
        class APIServiceUnavailable(APIFailure):
            pass

        self.assertTrue(APIServiceUnavailable(status_code=503).is_transient_error())

    def test_message_text_does_not_affect_classification(self):
        self.assertFalse(
            APIFailure("original_status_code:503 lookalike").is_transient_error()
        )

    def test_single_message_arg_is_preserved(self):
        error = APIFailure("something broke", status_code=503)
        self.assertEqual(str(error), "something broke")


def _mock_response(status_code, json_data=None, headers=None, text=""):
    response = MagicMock()
    response.status_code = status_code
    response.headers = headers if headers is not None else {}
    response.text = text
    if json_data is None:
        response.json.side_effect = ValueError("no json")
    else:
        response.json.return_value = json_data
    return response


class TestDoRequestStatusCodes(unittest.TestCase):
    """do_request attaches the HTTP status to the exceptions it raises."""

    def setUp(self):
        self.api = API()
        self.api.encode_key("test-token")

    def _do_request_raising(self, expected_class, response=None, side_effect=None):
        with patch("socketdev.core.api.requests.request") as mock_request:
            if side_effect is not None:
                mock_request.side_effect = side_effect
            else:
                mock_request.return_value = response
            with self.assertRaises(expected_class) as ctx:
                self.api.do_request("orgs/test/full-scans", method="POST")
        return ctx.exception

    def test_401_access_denied_is_not_transient(self):
        error = self._do_request_raising(APIAccessDenied, _mock_response(401))
        self.assertEqual(error.status_code, 401)
        self.assertFalse(error.is_transient_error())

    def test_403_insufficient_permissions_is_not_transient(self):
        response = _mock_response(
            403,
            json_data={"error": {"message": "Insufficient permissions for API method"}},
        )
        error = self._do_request_raising(APIInsufficientPermissions, response)
        self.assertEqual(error.status_code, 403)
        self.assertFalse(error.is_transient_error())

    def test_404_not_found_is_not_transient(self):
        error = self._do_request_raising(APIResourceNotFound, _mock_response(404))
        self.assertEqual(error.status_code, 404)
        self.assertFalse(error.is_transient_error())

    def test_429_quota_is_not_transient(self):
        error = self._do_request_raising(APIInsufficientQuota, _mock_response(429))
        self.assertEqual(error.status_code, 429)
        self.assertFalse(error.is_transient_error())

    def test_502_bad_gateway_is_transient(self):
        error = self._do_request_raising(APIBadGateway, _mock_response(502))
        self.assertEqual(error.status_code, 502)
        self.assertTrue(error.is_transient_error())

    def test_catch_all_transient_statuses(self):
        for status in (408, 503, 504):
            error = self._do_request_raising(APIFailure, _mock_response(status))
            self.assertIs(type(error), APIFailure)
            self.assertEqual(error.status_code, status)
            self.assertTrue(error.is_transient_error())

    def test_catch_all_deterministic_statuses(self):
        for status in (400, 500):
            error = self._do_request_raising(APIFailure, _mock_response(status))
            self.assertIs(type(error), APIFailure)
            self.assertEqual(error.status_code, status)
            self.assertFalse(error.is_transient_error())

    def test_timeout_is_transient(self):
        error = self._do_request_raising(
            APITimeout, side_effect=requests.exceptions.Timeout("timed out")
        )
        self.assertIsNone(error.status_code)
        self.assertTrue(error.is_transient_error())

    def test_connection_error_is_transient(self):
        error = self._do_request_raising(
            APIConnectionError,
            side_effect=requests.exceptions.ConnectionError("reset"),
        )
        self.assertIsNone(error.status_code)
        self.assertTrue(error.is_transient_error())

    def test_unexpected_error_wrapped_without_status_is_not_transient(self):
        error = self._do_request_raising(APIFailure, side_effect=RuntimeError("boom"))
        self.assertIsNone(error.status_code)
        self.assertFalse(error.is_transient_error())


if __name__ == "__main__":
    unittest.main()
