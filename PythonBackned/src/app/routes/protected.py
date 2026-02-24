"""Sample protected API endpoints."""

from __future__ import annotations

from fastapi import APIRouter, Depends

from keycloak_auth import Authenticator, TokenClaims
from keycloak_auth.fastapi import create_auth_dependency, require_roles

from ..main import authenticator

router = APIRouter(prefix="/api", tags=["protected"])

get_current_user = create_auth_dependency(authenticator)


@router.get("/profile")
async def profile(user: TokenClaims = Depends(get_current_user)):
    """Return the authenticated user's profile claims."""
    return {
        "sub": user.sub,
        "username": user.preferred_username,
        "email": user.email,
        "name": user.name,
        "realm_roles": sorted(user.realm_roles),
    }


@router.get(
    "/admin",
    dependencies=[Depends(require_roles(authenticator, {"admin"}))],
)
async def admin(user: TokenClaims = Depends(get_current_user)):
    """Admin-only endpoint."""
    return {
        "message": f"Welcome admin {user.preferred_username}",
        "realm_roles": sorted(user.realm_roles),
    }
