"""Keycloak authentication exception hierarchy.

All exceptions carry an HTTP status code and a user-safe message so that
error handlers can convert them to proper JSON responses without leaking
internal details.
"""

from __future__ import annotations


class AuthError(Exception):
    """Base class for all authentication/authorization errors."""

    status_code: int = 401
    detail: str = "Authentication failed"

    def __init__(self, detail: str | None = None, *, status_code: int | None = None):
        self.detail = detail or self.__class__.detail
        if status_code is not None:
            self.status_code = status_code
        super().__init__(self.detail)


class TokenMissing(AuthError):
    """No Bearer token was provided in the request."""

    status_code = 401
    detail = "Authorization header missing or invalid"


class TokenExpired(AuthError):
    """The JWT has passed its ``exp`` claim."""

    status_code = 401
    detail = "Token has expired"


class TokenInvalid(AuthError):
    """The JWT signature or claims are invalid."""

    status_code = 401
    detail = "Token is invalid"


class InsufficientPermissions(AuthError):
    """The token is valid but lacks required roles/scopes."""

    status_code = 403
    detail = "Insufficient permissions"


class KeycloakUnavailable(AuthError):
    """Could not reach Keycloak (JWKS endpoint, introspection, etc.)."""

    status_code = 503
    detail = "Authentication service unavailable"
