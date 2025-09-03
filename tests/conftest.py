"""
Test configuration and utilities for Socket SDK tests.
"""

import os
import tempfile
import json
from pathlib import Path
from typing import Dict, Any


def load_env_file():
    """Load environment variables from .env file in project root if it exists."""
    env_path = Path(__file__).parent.parent / ".env"
    if env_path.exists():
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    # Only set if not already in environment
                    if key.strip() not in os.environ:
                        os.environ[key.strip()] = value.strip()


# Load .env file when module is imported
load_env_file()


class TestConfig:
    """Configuration for Socket SDK tests."""
    
    @classmethod
    def get_api_key(cls) -> str:
        """Get API key from environment."""
        return os.getenv("SOCKET_SECURITY_API_KEY", "")
    
    @classmethod
    def get_org_slug(cls) -> str:
        """Get organization slug from environment."""
        return os.getenv("SOCKET_ORG_SLUG", "")
    
    @classmethod
    def get_repo_slug(cls) -> str:
        """Get repository slug from environment."""
        return os.getenv("SOCKET_REPO_SLUG", "")
    
    @classmethod
    def has_credentials(cls) -> bool:
        """Check if basic credentials are available."""
        return bool(cls.get_api_key() and cls.get_org_slug())
    
    @classmethod
    def has_repo_access(cls) -> bool:
        """Check if repository access is configured."""
        return bool(cls.has_credentials() and cls.get_repo_slug())


class TestDataGenerator:
    """Generate test data for Socket SDK tests."""
    
    @staticmethod
    def create_test_package_json(name: str = "test-package", 
                                 dependencies: Dict[str, str] = None) -> Dict[str, Any]:
        """Create a test package.json structure."""
        if dependencies is None:
            dependencies = {"lodash": "4.17.21"}
            
        return {
            "name": name,
            "version": "1.0.0",
            "description": "Test package for Socket SDK integration tests",
            "dependencies": dependencies
        }
    
    @staticmethod
    def create_empty_package_json(name: str = "test-empty-package") -> Dict[str, Any]:
        """Create an empty package.json structure."""
        return {
            "name": name,
            "version": "1.0.0",
            "description": "Empty test package for Socket SDK integration tests"
        }
    
    @staticmethod
    def create_malware_package_json(name: str = "test-malware-package") -> Dict[str, Any]:
        """Create a package.json with known malware for testing."""
        return {
            "name": name,
            "version": "1.0.0",
            "description": "Package with known malware for testing",
            "dependencies": {
                "flowframe": "1.0.1"  # Known malware package
            }
        }
    
    @classmethod
    def write_package_json(cls, package_data: Dict[str, Any], 
                          file_path: str) -> None:
        """Write package.json data to a file."""
        with open(file_path, 'w') as f:
            json.dump(package_data, f, indent=2)


class TestFileManager:
    """Manage temporary files for testing."""
    
    def __init__(self):
        self.temp_dir = tempfile.mkdtemp()
        self.files = []
    
    def create_package_json(self, name: str = "package.json", 
                           content: Dict[str, Any] = None) -> str:
        """Create a temporary package.json file."""
        if content is None:
            content = TestDataGenerator.create_test_package_json()
            
        file_path = os.path.join(self.temp_dir, name)
        TestDataGenerator.write_package_json(content, file_path)
        self.files.append(file_path)
        return file_path
    
    def create_empty_package_json(self, name: str = "package-empty.json") -> str:
        """Create a temporary empty package.json file."""
        content = TestDataGenerator.create_empty_package_json()
        return self.create_package_json(name, content)
    
    def create_malware_package_json(self, name: str = "package-malware.json") -> str:
        """Create a temporary malware package.json file."""
        content = TestDataGenerator.create_malware_package_json()
        return self.create_package_json(name, content)
    
    def cleanup(self):
        """Clean up temporary files."""
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cleanup()


def skip_if_no_credentials(test_func):
    """Decorator to skip tests if credentials are not available."""
    def wrapper(*args, **kwargs):
        if not TestConfig.has_credentials():
            import unittest
            raise unittest.SkipTest(
                "SOCKET_SECURITY_API_KEY and SOCKET_ORG_SLUG required"
            )
        return test_func(*args, **kwargs)
    return wrapper


def skip_if_no_repo_access(test_func):
    """Decorator to skip tests if repository access is not available."""
    def wrapper(*args, **kwargs):
        if not TestConfig.has_repo_access():
            import unittest
            raise unittest.SkipTest(
                "SOCKET_SECURITY_API_KEY, SOCKET_ORG_SLUG, and SOCKET_REPO_SLUG required"
            )
        return test_func(*args, **kwargs)
    return wrapper
