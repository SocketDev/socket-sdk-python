#!/usr/bin/env python3
"""
Test runner for Socket SDK Python client.

This script helps run different test suites with proper configuration.

Usage:
    cd tests && python run_tests.py --unit              # Run unit tests only
    cd tests && python run_tests.py --integration       # Run integration tests only  
    cd tests && python run_tests.py --all               # Run all tests
    cd tests && python run_tests.py --new-endpoints     # Run tests for new endpoints
    cd tests && python run_tests.py --help              # Show help
"""

import argparse
import os
import sys
import subprocess
from pathlib import Path


def load_env_file():
    """Load environment variables from .env file in project root."""
    env_path = Path(__file__).parent.parent / ".env"
    if env_path.exists():
        print(f"📁 Loading environment from {env_path}")
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip()
        return True
    return False


def check_environment():
    """Check if the environment is properly configured."""
    print("🔍 Checking environment...")
    
    # Check if we're in a virtual environment
    in_venv = hasattr(sys, 'real_prefix') or (
        hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix
    )
    
    if in_venv:
        print("✅ Running in virtual environment")
    else:
        print("⚠️  Not running in virtual environment")
        print("   Consider activating .venv: source .venv/bin/activate")
    
    # Check for pytest
    try:
        import pytest
        print(f"✅ pytest available: {pytest.__version__}")
    except ImportError:
        print("❌ pytest not found. Install with: pip install pytest")
        return False
    
    # Check for socketdev
    try:
        import socketdev
        print(f"✅ socketdev available: {socketdev.__version__}")
    except ImportError:
        print("❌ socketdev not found. Install with: pip install -e .")
        return False
    
    return True


def check_credentials():
    """Check if API credentials are configured."""
    print("\n🔐 Checking credentials...")
    
    api_key = os.getenv("SOCKET_SECURITY_API_KEY", "")
    org_slug = os.getenv("SOCKET_ORG_SLUG", "")
    repo_slug = os.getenv("SOCKET_REPO_SLUG", "")
    
    if api_key and org_slug:
        print("✅ Basic credentials available (API key and org slug)")
        if repo_slug:
            print("✅ Repository slug available")
        else:
            print("⚠️  Repository slug not set (some tests will be skipped)")
    else:
        print("⚠️  Missing credentials:")
        if not api_key:
            print("   - SOCKET_SECURITY_API_KEY not set")
        if not org_slug:
            print("   - SOCKET_ORG_SLUG not set")
        print("   Integration tests will be skipped")
    
    return bool(api_key and org_slug)


def run_unit_tests():
    """Run unit tests with mocked API calls."""
    print("Running unit tests...")
    
    # Set test environment
    os.environ["SOCKET_TEST_MODE"] = "unit"
    
    cmd = [
        sys.executable, "-m", "pytest", 
        "tests/unit/test_socket_sdk_unit.py",
        "tests/unit/test_working_endpoints_unit.py",
        "-v", "--tb=short"
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print("STDERR:", result.stderr)
    
    return result.returncode == 0


def run_comprehensive_unit_tests():
    """Run comprehensive unit tests for all endpoints (includes failing tests)."""
    print("Running comprehensive unit tests for all endpoints (includes failing tests)...")
    
    # Set test environment
    os.environ["SOCKET_TEST_MODE"] = "unit"
    
    cmd = [
        sys.executable, "-m", "pytest", 
        "tests/unit/test_all_endpoints_unit.py",
        "-v", "--tb=short"
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print("STDERR:", result.stderr)
    
    return result.returncode == 0


def run_all_unit_tests():
    """Run all unit tests including problematic endpoints."""
    print("Running all unit tests (including problematic endpoints)...")
    
    # Set test environment
    os.environ["SOCKET_TEST_MODE"] = "unit"
    
    cmd = [
        sys.executable, "-m", "pytest", 
        "tests/unit/",
        "-v", "--tb=short"
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print("STDERR:", result.stderr)
    
    return result.returncode == 0


def run_integration_tests():
    """Run integration tests with real API calls."""
    if not validate_environment():
        return False
        
    print("Running integration tests...")
    
    # Set test environment
    os.environ["SOCKET_TEST_MODE"] = "integration"
    
    cmd = [
        sys.executable, "-m", "pytest", 
        "tests/integration/",
        "-v", "--tb=short"
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print("STDERR:", result.stderr)
    
    return result.returncode == 0


def run_comprehensive_integration_tests():
    """Run comprehensive integration tests for all endpoints."""
    if not validate_environment():
        return False
        
    print("Running comprehensive integration tests for all endpoints...")
    
    # Set test environment
    os.environ["SOCKET_TEST_MODE"] = "integration"
    
    cmd = [
        sys.executable, "-m", "pytest", 
        "tests/integration/test_all_endpoints.py",
        "-v", "--tb=short"
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print("STDERR:", result.stderr)
    
    return result.returncode == 0


def run_new_endpoints_tests():
    """Run tests for new endpoints."""
    if not validate_environment():
        return False
        
    print("Running new endpoints tests...")
    
    cmd = [
        sys.executable, "-m", "pytest", 
        "tests/integration/test_new_endpoints.py",
        "-v", "--tb=short"
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print("STDERR:", result.stderr)
    
    return result.returncode == 0


def run_legacy_tests():
    """Run legacy integration tests."""
    if not validate_environment():
        return False
        
    print("Running legacy integration tests...")
    
    cmd = [
        sys.executable, "-m", "pytest", 
        "tests/integration/test_diffscans_integration.py",
        "-v", "--tb=short"
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print("STDERR:", result.stderr)
    
    return result.returncode == 0


def run_tests(test_type, verbose=False):
    """
    Run the specified test suite.
    
    Args:
        test_type: One of 'unit', 'integration', 'all', 'new-endpoints', 'legacy', 'comprehensive-unit', 'all-unit'
        verbose: Whether to enable verbose output
    """
    success = True
    
    if test_type == "unit":
        success = run_unit_tests()
    elif test_type == "comprehensive-unit":
        success = run_comprehensive_unit_tests()
    elif test_type == "all-unit":
        success = run_all_unit_tests()
    elif test_type == "integration":
        success = run_integration_tests() and run_comprehensive_integration_tests()
    elif test_type == "new-endpoints":
        success = run_new_endpoints_tests()
    elif test_type == "legacy":
        success = run_legacy_tests()
    elif test_type == "all":
        print("Running all test suites...")
        success = (
            run_unit_tests() and 
            run_integration_tests() and
            run_comprehensive_integration_tests() and
            run_new_endpoints_tests() and
            run_legacy_tests()
        )
    else:
        print(f"Unknown test type: {test_type}")
        print("Available options: unit, integration, all, new-endpoints, legacy, comprehensive-unit, all-unit")
        success = False
    
    return success


def validate_environment():
    """Validate test environment for integration tests."""
    # For integration tests, we need both dependencies and credentials
    print("\n🔍 Validating environment...")
    
    # Check dependencies (always needed)
    deps_ok = True
    try:
        import socketdev
        print(f"✅ socketdev available: {socketdev.__version__}")
    except ImportError:
        print("❌ socketdev not found. Install with: pip install -e .")
        deps_ok = False
    
    # Check credentials (needed for integration tests)
    creds_ok = check_credentials()
    
    return deps_ok and creds_ok


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Test runner for Socket SDK Python client",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  cd tests && python run_tests.py --unit              # Run working unit tests only
  cd tests && python run_tests.py --comprehensive-unit # Run all unit tests (includes failing)
  cd tests && python run_tests.py --all-unit          # Run all unit tests including problematic
  cd tests && python run_tests.py --integration       # Run integration tests only
  cd tests && python run_tests.py --all               # Run all tests
  cd tests && python run_tests.py --new-endpoints     # Run tests for new endpoints
  cd tests && python run_tests.py --legacy           # Run legacy integration tests

Environment Variables:
  Can be set in .env file in project root or as environment variables:
  SOCKET_SECURITY_API_KEY    Your Socket.dev API key (required for integration tests)
  SOCKET_ORG_SLUG           Your organization slug (required for integration tests)
  SOCKET_REPO_SLUG          Your repository slug (optional, some tests will be skipped)
        """
    )
    
    parser.add_argument("--unit", action="store_true", 
                       help="Run working unit tests only (no API key required)")
    parser.add_argument("--comprehensive-unit", action="store_true",
                       help="Run comprehensive unit tests (includes failing tests)")
    parser.add_argument("--all-unit", action="store_true",
                       help="Run all unit tests including problematic endpoints")
    parser.add_argument("--integration", action="store_true",
                       help="Run comprehensive integration tests")
    parser.add_argument("--new-endpoints", action="store_true",
                       help="Run tests for new endpoints")
    parser.add_argument("--legacy", action="store_true",
                       help="Run legacy integration tests")
    parser.add_argument("--all", action="store_true",
                       help="Run all tests")
    parser.add_argument("--quiet", "-q", action="store_true",
                       help="Run tests in quiet mode")
    
    args = parser.parse_args()
    
    # Determine test type
    test_type = "unit"  # Default to working unit tests
    if args.unit:
        test_type = "unit"
    elif args.comprehensive_unit:
        test_type = "comprehensive-unit"
    elif args.all_unit:
        test_type = "all-unit"
    elif args.integration:
        test_type = "integration"
    elif args.new_endpoints:
        test_type = "new-endpoints"
    elif args.legacy:
        test_type = "legacy"
    elif args.all:
        test_type = "all"
    
    verbose = not args.quiet
    
    print("🚀 Socket SDK Python Client Test Runner")
    print("=" * 40)
    
    success = run_tests(test_type, verbose)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
