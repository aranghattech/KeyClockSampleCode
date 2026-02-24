"""Pydantic models for decoded JWT token claims."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class TokenClaims(BaseModel):
    """Validated Keycloak JWT payload.

    Only commonly used claims are typed explicitly; the full payload is
    available via ``raw``.
    """

    sub: str
    exp: int
    iat: int | None = None
    iss: str | None = None
    aud: str | list[str] | None = None
    azp: str | None = None
    preferred_username: str | None = None
    email: str | None = None
    email_verified: bool | None = None
    name: str | None = None
    given_name: str | None = None
    family_name: str | None = None
    scope: str | None = None

    realm_access: dict[str, Any] = Field(default_factory=dict)
    resource_access: dict[str, Any] = Field(default_factory=dict)

    raw: dict[str, Any] = Field(default_factory=dict, exclude=True)

    # --- Convenience helpers ---

    @property
    def realm_roles(self) -> set[str]:
        """Roles granted at the realm level."""
        return set(self.realm_access.get("roles", []))

    def client_roles(self, client_id: str) -> set[str]:
        """Roles granted for a specific client."""
        return set(
            self.resource_access.get(client_id, {}).get("roles", [])
        )

    @property
    def scopes(self) -> set[str]:
        """OAuth2 scopes from the ``scope`` claim."""
        return set(self.scope.split()) if self.scope else set()

    def has_role(self, role: str, client_id: str | None = None) -> bool:
        """Check whether the token carries *role*."""
        if client_id:
            return role in self.client_roles(client_id)
        return role in self.realm_roles

    def has_any_role(self, roles: set[str], client_id: str | None = None) -> bool:
        if client_id:
            return bool(roles & self.client_roles(client_id))
        return bool(roles & self.realm_roles)
