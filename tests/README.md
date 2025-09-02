# Socket SDK Python Tests

This directory contains comprehensive tests for the Socket SDK Python client.

## Test Structure

- `unit/` - Unit tests that don't require API credentials
- `integration/` - Integration tests that require API credentials
- `conftest.py` - Test configuration and utilities
- `run_tests.py` - Test runner script

## Setup

1. Make sure you're in the virtual environment:
   ```bash
   source .venv/bin/activate
   ```

2. Install test dependencies:
   ```bash
   pip install pytest
   ```

3. For integration tests, create a `.env` file in the project root with your credentials:
   ```bash
   # .env file in project root
   SOCKET_SECURITY_API_KEY=your_api_key_here
   SOCKET_ORG_SLUG=your_org_slug_here
   SOCKET_REPO_SLUG=your_repo_slug_here  # Optional
   ```

## Running Tests

### Using the test runner (recommended):

```bash
cd tests

# Run unit tests only (no API key required)
python run_tests.py --unit

# Run integration tests (requires API credentials)
python run_tests.py --integration

# Run tests for new endpoints
python run_tests.py --new-endpoints

# Run all tests
python run_tests.py --all
```

### Using pytest directly:

```bash
# From project root

# Run unit tests
python -m pytest tests/unit/ -v

# Run integration tests
python -m pytest tests/integration/ -v

# Run all tests
python -m pytest tests/ -v

# Run specific test file
python -m pytest tests/integration/test_comprehensive_integration.py -v
```

## Test Files

### Unit Tests
- `test_socket_sdk_unit.py` - Core SDK functionality tests (no API required)

### Integration Tests
- `test_comprehensive_integration.py` - Complete workflow tests
- `test_new_endpoints.py` - Tests for newly added endpoints
- `test_diffscans_integration.py` - Legacy diff scan tests

## Environment Variables

The tests support the following environment variables (can be set in `.env` file):

- `SOCKET_SECURITY_API_KEY` - Your Socket.dev API key (required for integration tests)
- `SOCKET_ORG_SLUG` - Your organization slug (required for integration tests)
- `SOCKET_REPO_SLUG` - Repository slug for testing (optional, some tests will be skipped if not provided)

## Test Coverage

The tests cover:

- **SDK Initialization**: Verifying all components are properly initialized
- **Full Scan Workflow**: Creating, retrieving, and managing full scans
- **Diff Scan Workflow**: Creating diff scans from full scans and repositories
- **New Endpoints**: Testing recently added endpoints like threatfeed, analytics, etc.
- **Error Handling**: Testing proper error responses and logging
- **File Handling**: Testing file upload functionality
- **API Compatibility**: Testing backward compatibility

## Skipped Tests

Some tests may be skipped if:
- API credentials are not provided (integration tests)
- Repository access is not configured (some integration tests)
- Specific endpoints are not available for your organization

This is normal behavior and doesn't indicate test failures.

## Troubleshooting

1. **Import Errors**: Make sure you're in the virtual environment and have installed the SDK:
   ```bash
   source .venv/bin/activate
   pip install -e .
   ```

2. **Credential Errors**: Verify your `.env` file is in the project root and contains valid credentials

3. **Permission Errors**: Some endpoints may not be available for all organizations

4. **Network Errors**: Integration tests require internet connectivity to api.socket.dev
