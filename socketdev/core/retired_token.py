import hashlib
import hmac

RETIRED_TOKEN_SHA256 = "9cab58b24140ee12c08e265729d246f9200f8ef9b1d884f90c06c4e6b69adf18"  # noqa: S105  # public fingerprint or error text
RETIRED_TOKEN_ERROR = "This API token has been retired. Create a new API token in Socket and update your configuration."  # noqa: S105  # public fingerprint or error text


# Fingerprint identifies a retired credential; it is not a password verifier.
def _matches_retired_digest(token: str | None, digest: str) -> bool:
    if token is None:
        return False
    token_digest = hashlib.sha256(token.strip().encode("utf-8")).hexdigest()
    return hmac.compare_digest(token_digest, digest)


def _reject_retired_token(token: str | None, digest: str) -> None:
    if _matches_retired_digest(token, digest):
        raise ValueError(RETIRED_TOKEN_ERROR)


def _reject_basic_auth_token(token: str, digest: str) -> None:
    _reject_retired_token(token.partition(":")[0], digest)


def reject_retired_token(token: str | None) -> None:
    _reject_retired_token(token, RETIRED_TOKEN_SHA256)


def reject_retired_basic_auth_token(token: str) -> None:
    _reject_basic_auth_token(token, RETIRED_TOKEN_SHA256)
