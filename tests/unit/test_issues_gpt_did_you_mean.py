"""Contract tests for the gptDidYouMean alert-type class.

The OpenAPI schema (`socket-sdk-js/openapi.json` around line 9343) declares
that the API emits this alert with ``props: { alternatePackage, detectedAt }``.
These tests pin that contract on the Python SDK side without locking exact
copy strings — product/marketing should be free to revise wording without
breaking tests.

Tracks CUS2-4. Parent customer issue: CUS2-2.
"""

import unittest

from socketdev.core.issues import AllIssues, gptDidYouMean


class TestGptDidYouMeanIssueClass(unittest.TestCase):
    def test_class_is_exported(self):
        """gptDidYouMean must be importable directly from socketdev.core.issues."""
        from socketdev.core import issues
        self.assertIn("gptDidYouMean", issues.__all__)
        self.assertTrue(hasattr(issues, "gptDidYouMean"))

    def test_all_issues_has_gpt_did_you_mean_attribute(self):
        all_issues = AllIssues()
        self.assertTrue(hasattr(all_issues, "gptDidYouMean"))
        self.assertIsInstance(all_issues.gptDidYouMean, gptDidYouMean)

    def test_props_match_openapi_schema(self):
        """API emits props { alternatePackage, detectedAt } (openapi.json:9343)."""
        issue = gptDidYouMean()
        self.assertEqual(set(issue.props.keys()), {"alternatePackage", "detectedAt"})

    def test_user_facing_strings_are_non_empty(self):
        """title, description, suggestion, nextStepTitle, emoji must all be non-empty."""
        issue = gptDidYouMean()
        self.assertTrue(issue.title, "title should not be empty")
        self.assertTrue(issue.description, "description should not be empty")
        self.assertTrue(issue.suggestion, "suggestion should not be empty")
        self.assertTrue(issue.nextStepTitle, "nextStepTitle should not be empty")
        self.assertTrue(issue.emoji, "emoji should not be empty")

    def test_title_mentions_typosquat(self):
        """The user-visible title must contain 'typosquat' so it's grep-able and
        clearly tells customers what this alert is about. The exact wording can
        change; the keyword cannot."""
        issue = gptDidYouMean()
        self.assertIn("typosquat", issue.title.lower())

    def test_str_returns_valid_json(self):
        """Consistency with sibling classes: __str__ returns a JSON serialization."""
        import json
        issue = gptDidYouMean()
        parsed = json.loads(str(issue))
        self.assertEqual(parsed["title"], issue.title)
