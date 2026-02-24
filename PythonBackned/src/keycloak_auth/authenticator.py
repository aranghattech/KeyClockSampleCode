"""High-level authentication facade.

``Authenticator`` composes a ``TokenValidator`` and adds role/scope
checking, providing a single entry point for token verification.
"""

from __future__ import annotations

from .config import KeycloakSettings
from .exceptions import InsufficientPermissions, TokenMissing
from .models import TokenClaims
from .validators import JWKSTokenValidator, TokenValidator


class Authenticator:
    """Facade that validates a Bearer token and checks permissions."""

    def __init__(
        self,
        settings: KeycloakSettings,
        validator: TokenValidator | None = None,
    ):
        self._settings = settings
        self._validator = validator or JWKSTokenValidator(settings)

    def authenticate(self, token: str | None) -> TokenClaims:
        """Validate *token* and return claims.

        Raises :class:`TokenMissing` when *token* is ``None`` or empty.
        """
        if not token:
            raise TokenMissing()
        return self._validator.validate(token)

    def require_roles(
        self,
        claims: TokenClaims,
        roles: set[str],
        client_id: str | None = None,
    ) -> None:
        """Raise :class:`InsufficientPermissions` if *claims* lack any role."""
        if client_id:
            user_roles = claims.client_roles(client_id)
        else:
            user_roles = claims.realm_roles

        if not roles.issubset(user_roles):
            missing = roles - user_roles
            raise InsufficientPermissions(
                f"Missing required roles: {', '.join(sorted(missing))}"
            )

    def require_scopes(
        self,
        claims: TokenClaims,
        scopes: set[str],
    ) -> None:
        """Raise :class:`InsufficientPermissions` if *claims* lack any scope."""
        if not scopes.issubset(claims.scopes):
            missing = scopes - claims.scopes
            raise InsufficientPermissions(
                f"Missing required scopes: {', '.join(sorted(missing))}"
            )
