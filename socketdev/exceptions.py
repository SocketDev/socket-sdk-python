from typing import Optional

# HTTP statuses classified as transient by APIFailure.is_transient_error(): gateway /
# availability failures where the request was dropped before the application produced a
# definitive response, so retrying the same request may succeed (408 Request Timeout,
# 502 Bad Gateway, 503 Service Unavailable, 504 Gateway Timeout).
TRANSIENT_HTTP_STATUS_CODES = frozenset({408, 502, 503, 504})


class APIFailure(Exception):
    """Base exception for all Socket API errors"""

    def __init__(self, *args, status_code: Optional[int] = None):
        super().__init__(*args)
        self.status_code = status_code

    def is_transient_error(self) -> bool:
        """Whether this failure is transient, i.e. retrying the same request may succeed.

        Transient failures happen at the gateway/connection level - HTTP 408/502/503/504,
        dropped or reset connections, and client-side timeouts - before the server produced
        a definitive response. Deterministic errors (e.g. 400/401/403/404/429) are not
        transient: retrying the same request fails the same way. Classification is based on
        the HTTP status code recorded when the exception was raised (or overridden by
        subclasses without an HTTP status, like timeouts), so it stays correct even if a
        status code gains a dedicated exception subclass later.
        """
        return self.status_code in TRANSIENT_HTTP_STATUS_CODES


class APIKeyMissing(APIFailure):
    """Raised when the api key is not passed and the headers are empty"""


class APIAccessDenied(APIFailure):
    """Raised when access is denied to the API"""
    pass


class APIInsufficientPermissions(APIFailure):
    """Raised when the API token doesn't have required permissions"""
    pass


class APIOrganizationNotAllowed(APIFailure):
    """Raised when organization doesn't have access to the feature"""
    pass


class APIInsufficientQuota(APIFailure):
    """Raised when access is denied to the API due to quota limits"""
    pass


class APIResourceNotFound(APIFailure):
    """Raised when the requested resource is not found"""
    pass


class APITimeout(APIFailure):
    """Raised when a request times out"""

    def is_transient_error(self) -> bool:
        # No HTTP status: the request timed out client-side, so a retry may succeed.
        return True


class APIConnectionError(APIFailure):
    """Raised when there's a connection error"""

    def is_transient_error(self) -> bool:
        # No HTTP status: the connection was dropped/reset mid-request, so a retry may succeed.
        return True


class APIBadGateway(APIFailure):
    """Raised when the upstream server returns a 502 Bad Gateway error"""

    def __init__(self, *args, status_code: Optional[int] = 502):
        super().__init__(*args, status_code=status_code)
