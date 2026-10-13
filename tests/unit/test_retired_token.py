import base64
import hashlib

import pytest

from socketdev import socketdev
from socketdev.core.api import API
from socketdev.core.retired_token import (
    RETIRED_TOKEN_ERROR,
    _reject_basic_auth_token,
    _reject_retired_token,
)
from socketdev.core.token_selection import TOKEN_ENVIRONMENT_VARIABLES, select_token


def test_retired_token_rejection_redacts_token_and_digest():
    token = "synthetic-retired-token"
    digest = hashlib.sha256(token.encode()).hexdigest()

    with pytest.raises(ValueError) as exc_info:
        _reject_retired_token(token, digest)

    assert str(exc_info.value) == RETIRED_TOKEN_ERROR
    assert token not in str(exc_info.value)
    assert digest not in str(exc_info.value)


def test_sdk_constructor_accepts_safe_explicit_token_without_network_access():
    sdk = socketdev(token="synthetic-safe-token")

    assert sdk.token == "synthetic-safe-token:"


def test_api_encode_key_preserves_each_input_byte_sequence():
    bare_api = API()
    suffixed_api = API()
    bare_token = "synthetic-safe-token"
    suffixed_token = "synthetic-safe-token:"

    bare_api.encode_key(bare_token)
    suffixed_api.encode_key(suffixed_token)

    assert bare_api.encoded_key == base64.b64encode(bare_token.encode()).decode("ascii")
    assert suffixed_api.encoded_key == base64.b64encode(suffixed_token.encode()).decode("ascii")


def test_api_rejects_retired_basic_username_with_password_suffix():
    token = "synthetic-retired-token"
    digest = hashlib.sha256(token.encode()).hexdigest()

    with pytest.raises(ValueError, match="token has been retired"):
        _reject_basic_auth_token(f"{token}:password", digest)


def test_token_selection_preserves_explicit_and_environment_precedence():
    environment = {
        name: f"token-{index}"
        for index, name in enumerate(TOKEN_ENVIRONMENT_VARIABLES)
    }

    assert select_token("", environment) == ""
    assert select_token("explicit", environment) == "explicit"
    assert select_token(None, environment) == "token-0"
    assert select_token(
        None,
        {TOKEN_ENVIRONMENT_VARIABLES[0]: "", TOKEN_ENVIRONMENT_VARIABLES[1]: "next"},
    ) == "next"
    assert select_token(None, {}) is None


@pytest.mark.parametrize("token", [None, "different-token"])
def test_nonretired_token_is_accepted(token):
    digest = hashlib.sha256(b"synthetic-retired-token").hexdigest()
    _reject_retired_token(token, digest)


def test_retired_token_comparison_trims_whitespace():
    digest = hashlib.sha256(b"synthetic-retired-token").hexdigest()
    with pytest.raises(ValueError):
        _reject_retired_token(" \tsynthetic-retired-token\n", digest)


@pytest.mark.parametrize("name", TOKEN_ENVIRONMENT_VARIABLES)
def test_each_environment_source_is_supported(name):
    assert select_token(None, {name: "selected-token"}) == "selected-token"
