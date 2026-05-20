"""
Unit tests for lenient SocketCategory parsing in SocketAlert.from_dict.

Regression coverage for
https://github.com/SocketDev/socket-sdk-python/issues/78: the Socket API can
emit category values the SDK does not yet know about (e.g. ``"other"``). Strict
enum parsing turned that into a hard failure that took down every consumer
(notably socketsecurity CI runs) whenever a diff included one of those alerts.

These tests pin the fallback behavior so the SDK stays forward-compatible with
new server-side categories.
"""

import logging
import unittest

from socketdev.fullscans import SocketAlert, SocketCategory, SocketIssueSeverity


class TestSocketAlertCategoryParsing(unittest.TestCase):
    """SocketAlert.from_dict should tolerate unknown category values."""

    def _base_payload(self, category: str) -> dict:
        return {
            "key": "alert-key",
            "type": "someAlertType",
            "severity": "low",
            "category": category,
        }

    def test_known_category_is_preserved(self):
        alert = SocketAlert.from_dict(self._base_payload("supplyChainRisk"))
        self.assertEqual(alert.category, SocketCategory.SUPPLY_CHAIN_RISK)
        self.assertEqual(alert.severity, SocketIssueSeverity.LOW)

    def test_unknown_category_falls_back_to_miscellaneous(self):
        alert = SocketAlert.from_dict(self._base_payload("other"))
        self.assertEqual(alert.category, SocketCategory.MISCELLANEOUS)

    def test_unknown_category_does_not_raise(self):
        # Explicit regression assertion: no ValueError for brand-new categories.
        try:
            SocketAlert.from_dict(self._base_payload("somethingCompletelyNew"))
        except ValueError as exc:
            self.fail(f"SocketAlert.from_dict raised ValueError for unknown category: {exc}")

    def test_unknown_category_emits_warning(self):
        with self.assertLogs("socketdev", level=logging.WARNING) as captured:
            SocketAlert.from_dict(self._base_payload("other"))
        self.assertTrue(
            any("Unknown SocketCategory" in message for message in captured.output),
            f"expected a warning about the unknown category, got: {captured.output}",
        )

    def test_every_known_category_round_trips(self):
        for category in SocketCategory:
            with self.subTest(category=category):
                alert = SocketAlert.from_dict(self._base_payload(category.value))
                self.assertEqual(alert.category, category)


if __name__ == "__main__":
    unittest.main()
