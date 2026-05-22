"""Contract test for the didYouMean alert-type class's props.

The OpenAPI schema (`socket-sdk-js/openapi.json` around line 9298) declares
that the API emits `didYouMean` alerts with ``props: { alternatePackage,
detectedAt }``. The Python SDK previously declared four props
(``alternatePackage``, ``downloads``, ``downloadsRatio``, ``editDistance``);
the latter three are no longer in the API schema and were dead keys at
runtime — and ``detectedAt`` was missing.

Tracks CUS2-5. Sibling of CUS2-4.
"""

import unittest

from socketdev.core.issues import didYouMean


class TestDidYouMeanProps(unittest.TestCase):
    def test_props_match_openapi_schema(self):
        """API emits props { alternatePackage, detectedAt } (openapi.json:9298)."""
        issue = didYouMean()
        self.assertEqual(set(issue.props.keys()), {"alternatePackage", "detectedAt"})

    def test_props_label_strings_are_non_empty(self):
        """Every props key must have a non-empty human-readable label."""
        issue = didYouMean()
        for key, label in issue.props.items():
            self.assertTrue(label, f"props[{key!r}] label should not be empty")
