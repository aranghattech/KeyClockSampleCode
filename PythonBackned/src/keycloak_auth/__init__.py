"""keycloak-auth — Reusable Keycloak JWT validation for Python.

Public API
----------
::

    from keycloak_auth import Authenticator, KeycloakSettings, TokenClaims

"""

from .authenticator import Authenticator
from .config import KeycloakSettings
from .exceptions import (
    AuthError,
    InsufficientPermissions,
    KeycloakUnavailable,
    TokenExpired,
    TokenInvalid,
    TokenMissing,
)
from .models import TokenClaims
from .validators import (
    IntrospectionTokenValidator,
    JWKSTokenValidator,
    TokenValidator,
)

__all__ = [
    "Authenticator",
    "AuthError",
    "InsufficientPermissions",
    "IntrospectionTokenValidator",
    "JWKSTokenValidator",
    "KeycloakSettings",
    "KeycloakUnavailable",
    "TokenClaims",
    "TokenExpired",
    "TokenInvalid",
    "TokenMissing",
    "TokenValidator",
]
