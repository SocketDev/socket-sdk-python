import json

import pytest

from socketdev import socketdev
from socketdev.fullscans import FullScanStreamResponse
from socketdev.exceptions import APIAccessDenied, APIResourceNotFound, APITimeout
from tests.support.socket_api_fixture import SocketApiFixture, SocketResponse


@pytest.fixture
def api_fixture():
    fixture = SocketApiFixture()
    fixture.start()
    yield fixture
    fixture.close()


def sdk_for(fixture, timeout=1):
    sdk = socketdev(token="synthetic-token", timeout=timeout)
    sdk.api.api_url = fixture.base_url
    return sdk


def ndjson(*records):
    return SocketResponse(200, None, raw_body="\n".join(json.dumps(record) for record in records).encode())


def test_cached_polling_returns_dictionary_and_typed_results(api_fixture):
    path = "orgs/org/full-scans/scan"
    artifact = {
        "id": "artifact-1",
        "alerts": [{"key": "test-key", "type": "test", "severity": "high", "category": "quality"}],
    }
    api_fixture.route("GET", path, ndjson(artifact))
    sdk = sdk_for(api_fixture)

    result = sdk.fullscans.stream("org", "scan")
    typed = sdk.fullscans.stream("org", "scan", use_types=True)

    assert result["artifact-1"]["alerts"][0]["type"] == "test"
    assert isinstance(typed, FullScanStreamResponse)
    assert typed.artifacts["artifact-1"].id == "artifact-1"
    assert typed.artifacts["artifact-1"].alerts[0].type == "test"
    assert all(request.query == {"cached": ["true"]} for request in api_fixture.requests)


def test_processing_then_ready_and_empty_stream(api_fixture):
    path = "orgs/org/full-scans/scan"
    responses = iter([SocketResponse(202, {"status": "processing"}), SocketResponse(202, {}), ndjson()])
    api_fixture.route("GET", path, lambda _request: next(responses))
    sdk = sdk_for(api_fixture)

    assert sdk.fullscans.stream("org", "scan", poll_timeout_seconds=0.5, poll_initial_interval_seconds=0.01) == {}
    assert len(api_fixture.requests) == 3


def test_transient_error_retries_and_invalid_ndjson_preserves_unsuccessful_response(api_fixture):
    path = "orgs/org/full-scans/scan"
    responses = iter([SocketResponse(503, {"error": {"message": "try again"}}), ndjson()])
    api_fixture.route("GET", path, lambda _request: next(responses))
    sdk = sdk_for(api_fixture)
    assert sdk.fullscans.stream(
        "org", "scan", poll_timeout_seconds=0.5, poll_initial_interval_seconds=0.01
    ) == {}
    assert len(api_fixture.requests) == 2

    api_fixture.requests.clear()
    api_fixture.route("GET", path, SocketResponse(200, None, raw_body=b"{invalid json"))
    response = sdk.fullscans.stream("org", "scan", use_types=True)
    assert isinstance(response, FullScanStreamResponse)
    assert not response.success


def test_perpetual_processing_times_out(api_fixture):
    api_fixture.route("GET", "orgs/org/full-scans/scan", SocketResponse(202, {}))
    with pytest.raises(APITimeout, match="full scan results"):
        sdk_for(api_fixture).fullscans.stream(
            "org", "scan", poll_timeout_seconds=0.06,
            poll_initial_interval_seconds=0.02, poll_max_interval_seconds=0.02,
        )


def test_persistent_transient_error_expires_with_poll_budget(api_fixture):
    api_fixture.route("GET", "orgs/org/full-scans/scan", SocketResponse(503, {}))
    with pytest.raises(APITimeout, match="full scan results"):
        sdk_for(api_fixture).fullscans.stream(
            "org", "scan", poll_timeout_seconds=0.06,
            poll_initial_interval_seconds=0.02, poll_max_interval_seconds=0.02,
        )
    assert len(api_fixture.requests) >= 1


def test_duplicate_artifacts_merge_alerts_and_preserve_score_event(api_fixture):
    path = "orgs/org/full-scans/scan"
    common = {
        "id": "artifact-1", "type": "pypi", "name": "example", "version": "1.0",
        "inputPurl": "pkg:pypi/example@1.0", "score": {
            "supplyChain": 1, "quality": 2, "maintenance": 3,
            "vulnerability": 4, "license": 5, "overall": 6,
        },
    }
    first = dict(common, release="wheel", alerts=[{
        "key": "alert-1", "type": "test", "severity": "high", "category": "quality",
    }])
    second = dict(common, release="source", alerts=[{
        "key": "alert-1", "type": "test", "severity": "high", "category": "quality",
    }])
    api_fixture.route("GET", path, ndjson(first, second))

    result = sdk_for(api_fixture).fullscans.stream("org", "scan")

    artifact = result["artifact-1"]
    assert artifact["releases"] == ["source", "wheel"]
    assert artifact["score"]["overall"] == 6
    assert len(artifact["alerts"]) == 1
    assert artifact["alerts"][0]["releases"] == ["wheel", "source"]


@pytest.mark.parametrize("status", [403, 404])
def test_deterministic_errors_stop_immediately(api_fixture, status):
    api_fixture.route("GET", "orgs/org/full-scans/scan", SocketResponse(status, {"error": {"message": "denied"}}))
    error_type = APIAccessDenied if status == 403 else APIResourceNotFound
    with pytest.raises(error_type):
        sdk_for(api_fixture).fullscans.stream("org", "scan", poll_timeout_seconds=0.1)
    assert len(api_fixture.requests) == 1


def test_invalid_settings_and_encoded_components(api_fixture):
    sdk = sdk_for(api_fixture)
    with pytest.raises(ValueError):
        sdk.fullscans.stream("org", "scan", poll_initial_interval_seconds=2, poll_max_interval_seconds=1)
    with pytest.raises(ValueError):
        sdk.fullscans.stream("org", "scan", poll_timeout_seconds=0.1, poll_initial_interval_seconds=True)
    assert not api_fixture.requests
    api_fixture.route("GET", "orgs/org%3Fx%3D1/full-scans/scan%3Fx%3D1", ndjson())
    sdk.fullscans.stream("org?x=1", "scan?x=1")
    assert api_fixture.requests[0].query == {"cached": ["true"]}


@pytest.mark.parametrize("value", [0, -1, float("nan"), float("inf"), True])
@pytest.mark.parametrize("parameter", ["poll_timeout_seconds", "poll_initial_interval_seconds", "poll_max_interval_seconds"])
def test_invalid_polling_numbers_fail_before_request(api_fixture, parameter, value):
    with pytest.raises(ValueError):
        sdk_for(api_fixture).fullscans.stream("org", "scan", **{parameter: value})
    assert not api_fixture.requests


@pytest.mark.parametrize("value", [0, -1, float("nan"), float("inf"), True])
def test_invalid_configured_request_timeout_fails_before_request(api_fixture, value):
    sdk = sdk_for(api_fixture)
    sdk.api.request_timeout = value
    with pytest.raises(ValueError):
        sdk.fullscans.stream("org", "scan", poll_timeout_seconds=0.1)
    assert not api_fixture.requests
