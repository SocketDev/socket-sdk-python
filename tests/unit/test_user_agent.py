import pytest
import requests

from socketdev import socketdev
from socketdev.version import __version__


@pytest.mark.parametrize("method", ["GET", "POST"])
@pytest.mark.parametrize(
    "user_agent",
    [
        None,
        "SocketPythonCLI/2.11.7",
        "socket-python-cli/2.11.7",
        "socket-basics/3.4.1",
        "custom-client/1.0.0",
        "",
    ],
)
def test_prepared_requests_use_sdk_identity_or_explicit_caller(
    monkeypatch, method, user_agent
):
    captured = []

    def send(session, request, **kwargs):
        captured.append(request)
        response = requests.Response()
        response.status_code = 200
        response._content = b"{}"
        return response

    monkeypatch.setattr(requests.sessions.Session, "send", send)
    sdk = socketdev(token="synthetic-test-token", user_agent=user_agent)
    files = [("manifest", ("package.json", b"{}"))] if method == "POST" else None

    sdk.api.do_request("organizations", method=method, files=files)

    assert len(captured) == 1
    expected = user_agent if user_agent is not None else f"socket-sdk-python/{__version__}"
    assert captured[0].headers["User-Agent"] == expected
    assert captured[0].headers["Authorization"].startswith("Basic ")
    if files:
        assert captured[0].headers["Content-Type"].startswith("multipart/form-data;")


def test_endpoint_wrappers_share_the_sdk_identity(monkeypatch):
    captured = []

    def send(session, request, **kwargs):
        captured.append(request)
        response = requests.Response()
        response.status_code = 200
        response._content = b"{}"
        return response

    monkeypatch.setattr(requests.sessions.Session, "send", send)
    sdk = socketdev(token="synthetic-test-token")

    sdk.org.get()
    sdk.basics.get_config("test-org")

    assert len(captured) == 2
    assert all(
        request.headers["User-Agent"] == f"socket-sdk-python/{__version__}"
        for request in captured
    )
