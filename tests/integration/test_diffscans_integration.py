import unittest
import os
import tempfile
import shutil
from socketdev import socketdev
from socketdev.fullscans import FullScanParams, IntegrationType

class TestDiffScansIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        api_key = os.getenv("SOCKET_SECURITY_API_KEY", "")
        org_slug = os.getenv("SOCKET_ORG_SLUG", "")
        repo_slug = os.getenv("SOCKET_REPO_SLUG", "")
        missing = [
            name for name, val in [
                ("SOCKET_SECURITY_API_KEY", api_key),
                ("SOCKET_ORG_SLUG", org_slug),
                ("SOCKET_REPO_SLUG", repo_slug),
            ] if not val
        ]
        if missing:
            raise RuntimeError(f"Missing required environment variables: {', '.join(missing)}")
        cls.sdk = socketdev(token=api_key)
        cls.org_slug = org_slug
        cls.repo_slug = repo_slug
        # Prepare temp dir for manifest files
        cls.temp_dir = tempfile.mkdtemp()
        cls.package_json_path = os.path.join(cls.temp_dir, "package.json")
        # Copy sample package.json
        shutil.copyfile(
            os.path.join(os.path.dirname(__file__), "package.json"),
            cls.package_json_path
        )

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.temp_dir)

    def test_full_diff_scan_flow(self):
        params_before = FullScanParams(
            org_slug=self.org_slug,
            repo=self.repo_slug,
            branch="main",
            commit_message="before scan commit message",
            commit_hash="deadbeefdeadbeefdeadbeefdeadbeefdeadbeef",
            pull_request=123,
            committers=["integration-tester"],
            integration_type="api"
        )

        # 1. Create 'before' full scan with empty package.json
        empty_package_path = os.path.join(os.path.dirname(__file__), "package-empty.json")
        with open(empty_package_path, "rb") as f_before:
            files_before = [("file", ("package.json", f_before))]
            before_result = self.sdk.fullscans.post(
                files=files_before,
                params=params_before
            )
            if not before_result or "id" not in before_result:
                print("Full scan creation failed. Response:", before_result)
                self.fail(f"Full scan creation failed: {before_result}")
            before_id = before_result["id"]
        self.assertIsNotNone(before_id)

        params_after = FullScanParams(
            org_slug=self.org_slug,
            repo=self.repo_slug,
            branch="main",
            commit_message="after scan commit message",
            commit_hash="beefdeadbeefdeadbeefdeadbeefdeadbeefdead",
            pull_request=124,
            committers=["integration-tester"],
            integration_type="api"
        )

        # 2. Create 'after' full scan with malware package.json
        with open(self.package_json_path, "rb") as f_after:
            files_after = [("file", ("package.json", f_after))]
            after_result = self.sdk.fullscans.post(
                files=files_after,
                params=params_after
            )
            if not after_result or "id" not in after_result:
                print("Full scan creation failed. Response:", after_result)
                self.fail(f"Full scan creation failed: {after_result}")
            after_id = after_result["id"]
        self.assertIsNotNone(after_id)

        # Only print before/after IDs if they are missing
        if not before_id or not after_id:
            print("before_id:", before_id)
            print("after_id:", after_id)
        self.assertIsNotNone(before_id, f"before_id is None. Full scan creation failed.")
        self.assertIsNotNone(after_id, f"after_id is None. Full scan creation failed.")

        diff_body = {"before": before_id, "after": after_id, "description": "Integration test diff scan"}
        diff_result = self.sdk.diffscans.create_from_ids(self.org_slug, diff_body)
        diff_scan_id = (
            (diff_result.get("diff_scan", {}) or {}).get("id")
            or diff_result.get("id")
            or diff_result.get("diff_scan_id")
        )
        if not diff_scan_id:
            print("diff_result:", diff_result)
        self.assertIsNotNone(diff_scan_id, f"Diff scan creation failed: {diff_result}")
        assert isinstance(diff_scan_id, str), "diff_scan_id must be a string"

        # 4. Use diff_scan_id for further tests
        get_result = self.sdk.diffscans.get(self.org_slug, diff_scan_id)
        # The API now returns the diff scan object under 'diff_scan'
        if "diff_scan" in get_result and isinstance(get_result["diff_scan"], dict):
            returned_id = get_result["diff_scan"].get("id")
        else:
            returned_id = (
                get_result.get("id")
                or get_result.get("diff_scan_id")
                or (get_result.get("diff_scan", {}).get("id") if "diff_scan" in get_result else None)
            )
        self.assertEqual(returned_id, diff_scan_id)

        gfm_result = self.sdk.diffscans.gfm(self.org_slug, diff_scan_id)
        self.assertIsInstance(gfm_result, dict)

        # 5. Cleanup
        self.sdk.diffscans.delete(self.org_slug, diff_scan_id)
        self.sdk.fullscans.delete(self.org_slug, before_id)
        self.sdk.fullscans.delete(self.org_slug, after_id)

    def test_diffscans_create_from_repo(self):
        """Integration test for create_from_repo endpoint."""
        # This test assumes a valid repo exists and the environment is set up
        with open(self.package_json_path, "rb") as f:
            files = [("file", ("package.json", f))]
            params = {"description": "Integration test diff scan from repo"}
            result = self.sdk.diffscans.create_from_repo(self.org_slug, self.repo_slug, files, params)
        self.assertTrue("id" in result or "diff_scan" in result)
        # Cleanup if possible
        diff_scan_id = (
            (result.get("diff_scan", {}) or {}).get("id")
            or result.get("id")
            or result.get("diff_scan_id")
        )
        if diff_scan_id:
            self.sdk.diffscans.delete(self.org_slug, diff_scan_id)

    def test_diffscans_get(self):
        """Integration test for get endpoint."""
        # Create a diff scan first
        params_before = FullScanParams(
            org_slug=self.org_slug,
            repo=self.repo_slug,
            branch="main",
            commit_message="before scan commit message",
            commit_hash="deadbeefdeadbeefdeadbeefdeadbeefdeadbeef",
            pull_request=123,
            committers=["integration-tester"],
            integration_type="api"
        )
        empty_package_path = os.path.join(os.path.dirname(__file__), "package-empty.json")
        with open(empty_package_path, "rb") as f_before:
            files_before = [("file", ("package.json", f_before))]
            before_result = self.sdk.fullscans.post(files=files_before, params=params_before)
            before_id = before_result["id"]
        params_after = FullScanParams(
            org_slug=self.org_slug,
            repo=self.repo_slug,
            branch="main",
            commit_message="after scan commit message",
            commit_hash="beefdeadbeefdeadbeefdeadbeefdeadbeefdead",
            pull_request=124,
            committers=["integration-tester"],
            integration_type="api"
        )
        with open(self.package_json_path, "rb") as f_after:
            files_after = [("file", ("package.json", f_after))]
            after_result = self.sdk.fullscans.post(files=files_after, params=params_after)
            after_id = after_result["id"]
        diff_body = {"before": before_id, "after": after_id, "description": "Integration test diff scan"}
        diff_result = self.sdk.diffscans.create_from_ids(self.org_slug, diff_body)
        diff_scan_id = (
            diff_result.get("id")
            or diff_result.get("diff_scan_id")
            or (diff_result.get("diff_scan", {}).get("id") if "diff_scan" in diff_result else None)
        )
        get_result = self.sdk.diffscans.get(self.org_slug, diff_scan_id)
        self.assertTrue(
            ("diff_scan" in get_result and get_result["diff_scan"]["id"] == diff_scan_id) or
            (get_result.get("id") == diff_scan_id)
        )
        # Cleanup
        self.sdk.diffscans.delete(self.org_slug, diff_scan_id)
        self.sdk.fullscans.delete(self.org_slug, before_id)
        self.sdk.fullscans.delete(self.org_slug, after_id)

    def test_diffscans_gfm(self):
        """Integration test for gfm endpoint."""
        # Create a diff scan first
        params_before = FullScanParams(
            org_slug=self.org_slug,
            repo=self.repo_slug,
            branch="main",
            commit_message="before scan commit message",
            commit_hash="deadbeefdeadbeefdeadbeefdeadbeefdeadbeef",
            pull_request=123,
            committers=["integration-tester"],
            integration_type="api"
        )
        empty_package_path = os.path.join(os.path.dirname(__file__), "package-empty.json")
        with open(empty_package_path, "rb") as f_before:
            files_before = [("file", ("package.json", f_before))]
            before_result = self.sdk.fullscans.post(files=files_before, params=params_before)
            before_id = before_result["id"]
        params_after = FullScanParams(
            org_slug=self.org_slug,
            repo=self.repo_slug,
            branch="main",
            commit_message="after scan commit message",
            commit_hash="beefdeadbeefdeadbeefdeadbeefdeadbeefdead",
            pull_request=124,
            committers=["integration-tester"],
            integration_type="api"
        )
        with open(self.package_json_path, "rb") as f_after:
            files_after = [("file", ("package.json", f_after))]
            after_result = self.sdk.fullscans.post(files=files_after, params=params_after)
            after_id = after_result["id"]
        diff_body = {"before": before_id, "after": after_id, "description": "Integration test diff scan"}
        diff_result = self.sdk.diffscans.create_from_ids(self.org_slug, diff_body)
        diff_scan_id = (
            diff_result.get("id")
            or diff_result.get("diff_scan_id")
            or (diff_result.get("diff_scan", {}).get("id") if "diff_scan" in diff_result else None)
        )
        gfm_result = self.sdk.diffscans.gfm(self.org_slug, diff_scan_id)
        self.assertIsInstance(gfm_result, dict)
        # Cleanup
        self.sdk.diffscans.delete(self.org_slug, diff_scan_id)
        self.sdk.fullscans.delete(self.org_slug, before_id)
        self.sdk.fullscans.delete(self.org_slug, after_id)

    def test_diffscans_delete(self):
        """Integration test for delete endpoint."""
        # Create a diff scan first
        params_before = FullScanParams(
            org_slug=self.org_slug,
            repo=self.repo_slug,
            branch="main",
            commit_message="before scan commit message",
            commit_hash="deadbeefdeadbeefdeadbeefdeadbeefdeadbeef",
            pull_request=123,
            committers=["integration-tester"],
            integration_type="api"
        )
        empty_package_path = os.path.join(os.path.dirname(__file__), "package-empty.json")
        with open(empty_package_path, "rb") as f_before:
            files_before = [("file", ("package.json", f_before))]
            before_result = self.sdk.fullscans.post(files=files_before, params=params_before)
            before_id = before_result["id"]
        params_after = FullScanParams(
            org_slug=self.org_slug,
            repo=self.repo_slug,
            branch="main",
            commit_message="after scan commit message",
            commit_hash="beefdeadbeefdeadbeefdeadbeefdeadbeefdead",
            pull_request=124,
            committers=["integration-tester"],
            integration_type="api"
        )
        with open(self.package_json_path, "rb") as f_after:
            files_after = [("file", ("package.json", f_after))]
            after_result = self.sdk.fullscans.post(files=files_after, params=params_after)
            after_id = after_result["id"]
        diff_body = {"before": before_id, "after": after_id, "description": "Integration test diff scan"}
        diff_result = self.sdk.diffscans.create_from_ids(self.org_slug, diff_body)
        diff_scan_id = (
            diff_result.get("id")
            or diff_result.get("diff_scan_id")
            or (diff_result.get("diff_scan", {}).get("id") if "diff_scan" in diff_result else None)
        )
        delete_result = self.sdk.diffscans.delete(self.org_slug, diff_scan_id)
        self.assertTrue(delete_result)
        # Cleanup
        self.sdk.fullscans.delete(self.org_slug, before_id)
        self.sdk.fullscans.delete(self.org_slug, after_id)

    def test_diffscans_list(self):
        """Integration test for list endpoint."""
        result = self.sdk.diffscans.list(self.org_slug)
        self.assertIn("results", result)

    def run(self, result=None):
        try:
            super().run(result)
            if self._testMethodName == "test_full_diff_scan_flow":
                print("Test create_from_ids: success")
            elif self._testMethodName == "test_diffscans_create_from_repo":
                print("Test create_from_repo: success")
            elif self._testMethodName == "test_diffscans_get":
                print("Test get: success")
            elif self._testMethodName == "test_diffscans_gfm":
                print("Test gfm: success")
            elif self._testMethodName == "test_diffscans_delete":
                print("Test delete: success")
            elif self._testMethodName == "test_diffscans_list":
                print("Test list: success")
        except Exception as e:
            if self._testMethodName == "test_full_diff_scan_flow":
                print("Test create_from_ids: failure")
            elif self._testMethodName == "test_diffscans_create_from_repo":
                print("Test create_from_repo: failure")
            elif self._testMethodName == "test_diffscans_get":
                print("Test get: failure")
            elif self._testMethodName == "test_diffscans_gfm":
                print("Test gfm: failure")
            elif self._testMethodName == "test_diffscans_delete":
                print("Test delete: failure")
            elif self._testMethodName == "test_diffscans_list":
                print("Test list: failure")
            raise
