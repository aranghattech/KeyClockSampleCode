"""Integration tests for FastAPI dependencies using TestClient."""

import pytest
from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient

from keycloak_auth import Authenticator, TokenClaims
from keycloak_auth.fastapi import (
    create_auth_dependency,
    register_auth_error_handlers,
    require_roles,
)


@pytest.fixture()
def app(authenticator):
    """Build a minimal FastAPI app wired to the test authenticator."""
    app = FastAPI()
    register_auth_error_handlers(app)

    get_user = create_auth_dependency(authenticator)

    @app.get("/profile")
    async def profile(user: TokenClaims = Depends(get_user)):
        return {"sub": user.sub, "username": user.preferred_username}

    @app.get(
        "/admin",
        dependencies=[Depends(require_roles(authenticator, {"admin"}))],
    )
    async def admin(user: TokenClaims = Depends(get_user)):
        return {"msg": "admin"}

    return app


@pytest.fixture()
def client(app):
    return TestClient(app)


class TestFastAPIDependencies:

    def test_no_token_returns_401(self, client):
        resp = client.get("/profile")
        assert resp.status_code == 401

    def test_valid_token_returns_200(self, client, make_token):
        token = make_token()
        resp = client.get("/profile", headers={"Authorization": f"Bearer {token}"})
        assert resp.status_code == 200
        data = resp.json()
        assert data["sub"] == "user-123"
        assert data["username"] == "testuser"

    def test_expired_token_returns_401(self, client, make_token):
        token = make_token(expired=True)
        resp = client.get("/profile", headers={"Authorization": f"Bearer {token}"})
        assert resp.status_code == 401

    def test_admin_without_role_returns_403(self, client, make_token):
        token = make_token({"realm_access": {"roles": ["user"]}})
        resp = client.get("/admin", headers={"Authorization": f"Bearer {token}"})
        assert resp.status_code == 403

    def test_admin_with_role_returns_200(self, client, make_token):
        token = make_token({"realm_access": {"roles": ["user", "admin"]}})
        resp = client.get("/admin", headers={"Authorization": f"Bearer {token}"})
        assert resp.status_code == 200
        assert resp.json()["msg"] == "admin"

    def test_invalid_token_returns_401(self, client):
        resp = client.get(
            "/profile",
            headers={"Authorization": "Bearer not-a-jwt"},
        )
        assert resp.status_code == 401
