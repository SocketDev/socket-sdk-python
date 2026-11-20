from collections.abc import Mapping

TOKEN_ENVIRONMENT_VARIABLES = (
    "SOCKET_SECURITY_API_TOKEN",
    "SOCKET_SECURITY_API_KEY",
    "SOCKET_API_KEY",
    "SOCKET_API_TOKEN",
)


def select_token(explicit_token: str | None, environment: Mapping[str, str]) -> str | None:
    if explicit_token is not None:
        return explicit_token
    return next(
        (environment[name] for name in TOKEN_ENVIRONMENT_VARIABLES if environment.get(name)),
        None,
    )
