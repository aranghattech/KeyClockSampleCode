"""FastAPI dependency factories for Keycloak authentication.

Usage::

    from keycloak_auth import Authenticator, KeycloakSettings
    from keycloak_auth.fastapi import create_auth_dependency, require_roles

    settings = KeycloakSettings()
    authenticator = Authenticator(settings)

    get_current_user = create_auth_dependency(authenticator)

    @app.get("/profile")
    async def profile(user: TokenClaims = Depends(get_current_user)):
        return {"sub": user.sub}

    @app.get("/admin", dependencies=[Depends(require_roles(authenticator, {"admin"}))])
    async def admin():
        return {"msg": "welcome admin"}
"""

from __future__ import annotations

from typing import Callable

from fastapi import Depends, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from ..authenticator import Authenticator
from ..models import TokenClaims

_bearer_scheme = HTTPBearer(auto_error=False)


def create_auth_dependency(
    authenticator: Authenticator,
) -> Callable[..., TokenClaims]:
    """Return a FastAPI dependency that extracts and validates the Bearer token."""

    async def _get_current_user(
        credentials: HTTPAuthorizationCredentials | None = Depends(_bearer_scheme),
    ) -> TokenClaims:
        token = credentials.credentials if credentials else None
        return authenticator.authenticate(token)

    return _get_current_user


def require_roles(
    authenticator: Authenticator,
    roles: set[str],
    client_id: str | None = None,
) -> Callable[..., None]:
    """Return a FastAPI dependency that enforces realm (or client) roles."""

    get_user = create_auth_dependency(authenticator)

    async def _check_roles(
        claims: TokenClaims = Depends(get_user),
    ) -> None:
        authenticator.require_roles(claims, roles, client_id=client_id)

    return _check_roles
