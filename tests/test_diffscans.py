import unittest
from unittest.mock import MagicMock
from socketdev.diffscans import DiffScans

class TestDiffScans(unittest.TestCase):
    def setUp(self):
        self.api = MagicMock()
        self.diffscans = DiffScans(self.api)
        self.org_slug = "test-org"
        self.diff_scan_id = "test-diff-scan-id"
        self.repo_slug = "test-repo"

    def test_list(self):
        self.api.do_request.return_value.status_code = 200
        self.api.do_request.return_value.json.return_value = {"results": []}
        result = self.diffscans.list(self.org_slug)
        self.assertIn("results", result)
        self.api.do_request.assert_called_with(path=f"orgs/{self.org_slug}/diff-scans", method="GET")

    def test_get(self):
        self.api.do_request.return_value.status_code = 200
        # Simulate new API response structure
        self.api.do_request.return_value.json.return_value = {"diff_scan": {"id": self.diff_scan_id}}
        result = self.diffscans.get(self.org_slug, self.diff_scan_id)
        self.assertIn("diff_scan", result)
        self.assertEqual(result["diff_scan"]["id"], self.diff_scan_id)
        self.api.do_request.assert_called_with(path=f"orgs/{self.org_slug}/diff-scans/{self.diff_scan_id}", method="GET")

    def test_create_from_repo(self):
        self.api.do_request.return_value.status_code = 201
        self.api.do_request.return_value.json.return_value = {"created": True}
        body = {"foo": "bar"}
        result = self.diffscans.create_from_repo(self.org_slug, self.repo_slug, body)
        self.assertTrue(result["created"])
        self.api.do_request.assert_called_with(path=f"orgs/{self.org_slug}/diff-scans/from-repo/{self.repo_slug}", method="POST", json=body)

    def test_create_from_ids(self):
        self.api.do_request.return_value.status_code = 201
        self.api.do_request.return_value.json.return_value = {"created": True}
        body = {"before": "id1", "after": "id2"}
        result = self.diffscans.create_from_ids(self.org_slug, body)
        self.assertTrue(result["created"])
        self.api.do_request.assert_called_with(path=f"orgs/{self.org_slug}/diff-scans/from-ids", method="POST", json=body)

    def test_gfm(self):
        self.api.do_request.return_value.status_code = 200
        self.api.do_request.return_value.json.return_value = {"gfm": "markdown"}
        result = self.diffscans.gfm(self.org_slug, self.diff_scan_id)
        self.assertIn("gfm", result)
        self.api.do_request.assert_called_with(path=f"orgs/{self.org_slug}/diff-scans/{self.diff_scan_id}/gfm", method="GET")

    def test_delete(self):
        self.api.do_request.return_value.status_code = 200
        self.api.do_request.return_value.json.return_value = {"deleted": True}
        result = self.diffscans.delete(self.org_slug, self.diff_scan_id)
        self.assertTrue(result["deleted"])
        self.api.do_request.assert_called_with(path=f"orgs/{self.org_slug}/diff-scans/{self.diff_scan_id}", method="DELETE")

if __name__ == "__main__":
    unittest.main()
