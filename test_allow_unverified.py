#!/usr/bin/env python3
"""
Test script to demonstrate the new allow_unverified option in socketdev.

This script shows how to initialize the Socket SDK with SSL verification
disabled, which can be useful for testing against local or self-signed
certificate environments.
"""

from socketdev import socketdev

def test_allow_unverified_option():
    """Test the allow_unverified option with different configurations."""
    
    print("Testing Socket SDK with allow_unverified option...")
    
    # Test 1: Default behavior (SSL verification enabled)
    print("\n1. Default initialization (allow_unverified=False):")
    sdk_default = socketdev(token="test-token")
    print(f"   allow_unverified: {sdk_default.api.allow_unverified}")
    print(f"   This means SSL certificates WILL be verified")
    
    # Test 2: Explicitly set allow_unverified=False
    print("\n2. Explicit allow_unverified=False:")
    sdk_verified = socketdev(token="test-token", allow_unverified=False)
    print(f"   allow_unverified: {sdk_verified.api.allow_unverified}")
    print(f"   This means SSL certificates WILL be verified")
    
    # Test 3: Set allow_unverified=True
    print("\n3. Setting allow_unverified=True:")
    sdk_unverified = socketdev(token="test-token", allow_unverified=True)
    print(f"   allow_unverified: {sdk_unverified.api.allow_unverified}")
    print(f"   This means SSL certificates will NOT be verified")
    
    # Test 4: Show how this affects the requests library verify parameter
    print("\n4. How this translates to requests.request() verify parameter:")
    print(f"   Default SDK: verify={not sdk_default.api.allow_unverified}")
    print(f"   Unverified SDK: verify={not sdk_unverified.api.allow_unverified}")
    
    print("\nUsage example:")
    print("   # For production use (default):")
    print("   sdk = socketdev(token='your-api-key')")
    print("")
    print("   # For testing with self-signed certificates:")
    print("   sdk = socketdev(token='your-api-key', allow_unverified=True)")

if __name__ == "__main__":
    test_allow_unverified_option()