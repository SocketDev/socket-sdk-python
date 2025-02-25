class APIFailure(Exception):
    """Base exception for all Socket API errors"""
    pass


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
    pass


class APIConnectionError(APIFailure):
    """Raised when there's a connection error"""
    pass


class APIBadGateway(APIFailure):
    """Raised when the upstream server returns a 502 Bad Gateway error"""
    pass