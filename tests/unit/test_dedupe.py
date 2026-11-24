import unittest
from socketdev.core.dedupe import Dedupe


class TestDedupe(unittest.TestCase):
    
    def test_consolidate_by_input_purl(self):
        """Test that packages are correctly grouped by inputPurl"""
        # Sample data similar to what the user provided
        packages = [
            {
                "id": "15591824355",
                "name": "pyonepassword",
                "version": "5.0.0",
                "type": "pypi",
                "release": "py3-none-any-whl",
                "inputPurl": "pkg:pypi/pyonepassword@5.0.0",
                "batchIndex": 0,
                "alerts": []
            },
            {
                "id": "15594798924",
                "name": "pyonepassword", 
                "version": "5.0.0",
                "type": "pypi",
                "release": "tar-gz",
                "inputPurl": "pkg:pypi/pyonepassword@5.0.0",
                "batchIndex": 0,
                "alerts": []
            },
            {
                "id": "77600911089",
                "name": "socketsecurity",
                "version": "2.2.7",
                "type": "pypi",
                "release": "py3-none-any-whl",
                "inputPurl": "pkg:pypi/socketsecurity",
                "batchIndex": 0,
                "alerts": []
            },
            {
                "id": "77600911090",
                "name": "socketsecurity",
                "version": "2.2.7",
                "type": "pypi",
                "release": "tar-gz",
                "inputPurl": "pkg:pypi/socketsecurity",
                "batchIndex": 0,
                "alerts": []
            }
        ]
        
        # Group by inputPurl
        grouped = Dedupe.consolidate_by_input_purl(packages)
        
        # Should have 2 groups
        self.assertEqual(len(grouped), 2)
        
        # Check pyonepassword group
        pyonepassword_group = grouped["pkg:pypi/pyonepassword@5.0.0"]
        self.assertEqual(len(pyonepassword_group), 2)
        self.assertEqual(pyonepassword_group[0]["name"], "pyonepassword")
        self.assertEqual(pyonepassword_group[1]["name"], "pyonepassword")
        
        # Check socketsecurity group  
        socketsecurity_group = grouped["pkg:pypi/socketsecurity"]
        self.assertEqual(len(socketsecurity_group), 2)
        self.assertEqual(socketsecurity_group[0]["name"], "socketsecurity")
        self.assertEqual(socketsecurity_group[1]["name"], "socketsecurity")

    def test_dedupe_with_input_purl_grouping(self):
        """Test that dedupe returns separate results when grouping by inputPurl"""
        packages = [
            {
                "id": "15591824355",
                "name": "pyonepassword",
                "version": "5.0.0",
                "type": "pypi",
                "release": "py3-none-any-whl",
                "inputPurl": "pkg:pypi/pyonepassword@5.0.0",
                "batchIndex": 0,
                "alerts": []
            },
            {
                "id": "15594798924",
                "name": "pyonepassword", 
                "version": "5.0.0",
                "type": "pypi",
                "release": "tar-gz",
                "inputPurl": "pkg:pypi/pyonepassword@5.0.0",
                "batchIndex": 0,
                "alerts": []
            },
            {
                "id": "77600911089",
                "name": "socketsecurity",
                "version": "2.2.7",
                "type": "pypi",
                "release": "py3-none-any-whl",
                "inputPurl": "pkg:pypi/socketsecurity",
                "batchIndex": 0,
                "alerts": []
            },
            {
                "id": "77600911090",
                "name": "socketsecurity",
                "version": "2.2.7",
                "type": "pypi",
                "release": "tar-gz",
                "inputPurl": "pkg:pypi/socketsecurity",
                "batchIndex": 0,
                "alerts": []
            }
        ]
        
        # Test with new inputPurl grouping (now the default and only method)
        result = Dedupe.dedupe(packages)
        
        # Should return 2 deduplicated packages
        self.assertEqual(len(result), 2)
        
        # Find each package in results
        pyonepassword_result = None
        socketsecurity_result = None
        
        for pkg in result:
            if pkg["name"] == "pyonepassword":
                pyonepassword_result = pkg
            elif pkg["name"] == "socketsecurity":
                socketsecurity_result = pkg
        
        # Both should be present
        self.assertIsNotNone(pyonepassword_result)
        self.assertIsNotNone(socketsecurity_result)
        
        # Check that releases are consolidated
        self.assertIn("releases", pyonepassword_result)
        self.assertIn("releases", socketsecurity_result)
        self.assertEqual(len(pyonepassword_result["releases"]), 2)
        self.assertEqual(len(socketsecurity_result["releases"]), 2)
        
        # Check that batchIndex is removed from results
        self.assertNotIn("batchIndex", pyonepassword_result)
        self.assertNotIn("batchIndex", socketsecurity_result)
        
    def test_dedupe_batched_parameter_backward_compatibility(self):
        """Test that batched parameter is kept for backward compatibility but doesn't change behavior"""
        packages = [
            {
                "id": "15591824355",
                "name": "pyonepassword",
                "version": "5.0.0",
                "type": "pypi",
                "release": "py3-none-any-whl",
                "inputPurl": "pkg:pypi/pyonepassword@5.0.0",
                "batchIndex": 0,
                "alerts": []
            },
            {
                "id": "77600911089",
                "name": "socketsecurity",
                "version": "2.2.7",
                "type": "pypi",
                "release": "py3-none-any-whl",
                "inputPurl": "pkg:pypi/socketsecurity@2.2.7",
                "batchIndex": 0,
                "alerts": []
            }
        ]
        
        # Test with batched=True
        result_batched_true = Dedupe.dedupe(packages, batched=True)
        
        # Test with batched=False  
        result_batched_false = Dedupe.dedupe(packages, batched=False)
        
        # Both should return 2 results (same behavior regardless of batched parameter)
        self.assertEqual(len(result_batched_true), 2)
        self.assertEqual(len(result_batched_false), 2)
        
        # Results should be the same
        names_true = sorted([pkg['name'] for pkg in result_batched_true])
        names_false = sorted([pkg['name'] for pkg in result_batched_false])
        self.assertEqual(names_true, names_false)
        
        # Should not contain batchIndex
        for pkg in result_batched_true + result_batched_false:
            self.assertNotIn("batchIndex", pkg)

    @staticmethod
    def _cve(ghsa, action, cve="", severity="critical", alert_type="criticalCVE", key=None):
        return {
            "key": key or f"key-{ghsa}",
            "type": alert_type,
            "severity": severity,
            "category": "vulnerability",
            "action": action,
            "props": {"ghsaId": ghsa, "cveId": cve},
        }

    def test_same_severity_advisories_on_one_package_stay_separate(self):
        """Each advisory keeps its own alert even when type and severity match"""
        ghsa_ids = [
            "GHSA-8r5x-fm3f-whwj", "GHSA-p8wg-vrv2-v86f", "GHSA-2w6w-674q-4c4q",
            "GHSA-w457-6q6x-cgp9", "GHSA-765h-qjxv-5f44", "GHSA-f2jv-r9rf-7988",
        ]
        packages = [{
            "id": "artifact-1", "type": "npm", "name": "handlebars", "version": "4.0.11",
            "alerts": [self._cve(ghsa, "error") for ghsa in ghsa_ids],
        }]

        result = Dedupe.dedupe(packages, batched=False)

        alerts = result[0]["alerts"]
        self.assertEqual(len(alerts), 6)
        self.assertEqual(sorted(a["props"]["ghsaId"] for a in alerts), sorted(ghsa_ids))
        self.assertTrue(all(a["action"] == "error" for a in alerts))

    def test_blocking_advisory_is_kept_when_an_earlier_one_is_triaged(self):
        """A monitored or ignored advisory listed first must not hide a later Block one"""
        for triaged_action in ("ignore", "monitor", "warn"):
            with self.subTest(triaged_action=triaged_action):
                packages = [{
                    "id": "artifact-1", "type": "npm", "name": "example", "version": "1.0.0",
                    "alerts": [
                        self._cve("GHSA-aaaa-aaaa-aaaa", triaged_action),
                        self._cve("GHSA-bbbb-bbbb-bbbb", "error"),
                    ],
                }]

                alerts = Dedupe.dedupe(packages, batched=False)[0]["alerts"]

                actions = {a["props"]["ghsaId"]: a["action"] for a in alerts}
                self.assertEqual(actions, {
                    "GHSA-aaaa-aaaa-aaaa": triaged_action,
                    "GHSA-bbbb-bbbb-bbbb": "error",
                })

    def test_same_advisory_across_releases_merges_with_most_severe_action(self):
        """One advisory seen in several releases is one alert carrying the strictest action"""
        orders = [
            ["ignore", "monitor", "error", "warn"],
            ["error", "ignore", "monitor", "warn"],
            ["monitor", "warn", "ignore", "error"],
        ]
        for actions in orders:
            with self.subTest(actions=actions):
                packages = [
                    {
                        "id": f"artifact-{i}", "type": "pypi", "name": "example", "version": "1.0",
                        "release": release, "inputPurl": "pkg:pypi/example@1.0",
                        "alerts": [self._cve("GHSA-cccc-cccc-cccc", action, cve="CVE-2020-0001",
                                             key=f"key-{release}")],
                    }
                    for i, (release, action) in enumerate(zip(["a", "b", "c", "d"], actions))
                ]

                alerts = Dedupe.dedupe(packages)[0]["alerts"]

                self.assertEqual(len(alerts), 1)
                self.assertEqual(alerts[0]["action"], "error")
                self.assertEqual(alerts[0]["releases"], ["a", "b", "c", "d"])

    def test_merged_action_ranks_error_warn_monitor_ignore(self):
        cases = [
            (["ignore", "monitor"], "monitor"),
            (["monitor", "warn"], "warn"),
            (["warn", "ignore"], "warn"),
            ([None, "ignore"], "ignore"),
            (["ignore", None], "ignore"),
            (["unknown-action", "monitor"], "monitor"),
            # An unknown action yields to any known one, "ignore" included,
            # and never replaces a known "error", in either order.
            (["unknown-action", "ignore"], "ignore"),
            (["error", "unknown-action"], "error"),
            (["unknown-action", "error"], "error"),
        ]
        for actions, expected in cases:
            with self.subTest(actions=actions):
                packages = [
                    {
                        "id": f"artifact-{i}", "type": "pypi", "name": "example", "version": "1.0",
                        "release": f"r{i}", "inputPurl": "pkg:pypi/example@1.0",
                        "alerts": [self._cve("GHSA-dddd-dddd-dddd", action)],
                    }
                    for i, action in enumerate(actions)
                ]
                alerts = Dedupe.dedupe(packages)[0]["alerts"]
                self.assertEqual(len(alerts), 1)
                self.assertEqual(alerts[0]["action"], expected)

    def test_merged_alert_keeps_first_key_when_action_comes_from_a_later_release(self):
        """Only the action moves to the most severe sighting; key and props stay with the first"""
        packages = [
            {
                "id": f"artifact-{release}", "type": "pypi", "name": "example", "version": "1.0",
                "release": release, "inputPurl": "pkg:pypi/example@1.0",
                "alerts": [self._cve("GHSA-eeee-eeee-eeee", action, key=f"key-{release}")],
            }
            for release, action in [("sdist", "monitor"), ("wheel", "error")]
        ]

        alerts = Dedupe.dedupe(packages)[0]["alerts"]

        self.assertEqual(len(alerts), 1)
        self.assertEqual(alerts[0]["key"], "key-sdist")
        self.assertEqual(alerts[0]["action"], "error")

    def test_non_advisory_alert_on_a_package_with_cves_keeps_its_own_entry(self):
        packages = [{
            "id": "artifact-1", "type": "npm", "name": "example", "version": "1.0.0",
            "alerts": [
                self._cve("GHSA-ffff-ffff-ffff", "monitor"),
                {"key": "key-malware", "type": "malware", "severity": "critical",
                 "category": "supplyChainRisk", "action": "error", "props": {}},
            ],
        }]

        alerts = Dedupe.dedupe(packages, batched=False)[0]["alerts"]

        self.assertEqual({a["type"]: a["action"] for a in alerts}, {"criticalCVE": "monitor", "malware": "error"})

    def test_dedupe_of_no_packages_is_empty(self):
        self.assertEqual(Dedupe.dedupe([]), [])

    def test_advisory_id_falls_back_to_cve_and_ignores_case(self):
        self.assertEqual(Dedupe.advisory_id({"props": {"ghsaId": "", "cveId": "cve-2021-1"}}), "CVE-2021-1")
        self.assertEqual(Dedupe.advisory_id({"props": {"ghsaId": " ghsa-x "}}), "GHSA-X")
        self.assertEqual(Dedupe.advisory_id({"props": {"cve": ["", "CVE-2022-2"]}}), "CVE-2022-2")
        self.assertEqual(Dedupe.advisory_id({"props": []}), "")
        self.assertEqual(Dedupe.advisory_id({}), "")

        packages = [{
            "id": "artifact-1", "type": "npm", "name": "example", "version": "1.0.0",
            "alerts": [
                self._cve("", "error", cve="CVE-2021-0001"),
                self._cve("", "error", cve="CVE-2021-0002"),
                self._cve("", "monitor", cve="cve-2021-0001"),
            ],
        }]
        alerts = Dedupe.dedupe(packages, batched=False)[0]["alerts"]
        self.assertEqual(sorted(a["props"]["cveId"] for a in alerts), ["CVE-2021-0001", "CVE-2021-0002"])

    def test_alerts_without_advisory_still_merge_across_releases(self):
        """Alerts without an advisory ID merge on type, severity and location, with file paths normalized"""
        def file_alert(path, action):
            return {
                "key": f"key-{path}", "type": "networkAccess", "severity": "middle",
                "category": "supplyChainRisk", "file": path, "start": 10, "end": 20,
                "action": action, "props": {"module": "http"},
            }
        packages = [
            {"id": "1", "type": "pypi", "name": "example", "version": "1.0", "release": "wheel",
             "inputPurl": "pkg:pypi/example@1.0", "alerts": [file_alert("wheel/example/net.py", "monitor")]},
            {"id": "2", "type": "pypi", "name": "example", "version": "1.0", "release": "sdist",
             "inputPurl": "pkg:pypi/example@1.0", "alerts": [file_alert("sdist/example/net.py", "warn")]},
        ]

        alerts = Dedupe.dedupe(packages)[0]["alerts"]

        self.assertEqual(len(alerts), 1)
        self.assertEqual(alerts[0]["file"], "example/net.py")
        self.assertEqual(alerts[0]["action"], "warn")
        self.assertEqual(alerts[0]["releases"], ["wheel", "sdist"])


if __name__ == '__main__':
    unittest.main()
