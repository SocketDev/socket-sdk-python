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


if __name__ == '__main__':
    unittest.main()
