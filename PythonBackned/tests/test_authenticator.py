"""Tests for the Authenticator facade."""

import pytest

from keycloak_auth.exceptions import InsufficientPermissions, TokenMissing


class TestAuthenticator:

    def test_authenticate_valid(self, authenticator, make_token):
        claims = authenticator.authenticate(make_token())
        assert claims.sub == "user-123"

    def test_authenticate_none_raises(self, authenticator):
        with pytest.raises(TokenMissing):
            authenticator.authenticate(None)

    def test_authenticate_empty_raises(self, authenticator):
        with pytest.raises(TokenMissing):
            authenticator.authenticate("")

    def test_require_roles_pass(self, authenticator, make_token):
        token = make_token({"realm_access": {"roles": ["user", "admin"]}})
        claims = authenticator.authenticate(token)
        authenticator.require_roles(claims, {"admin"})  # should not raise

    def test_require_roles_fail(self, authenticator, make_token):
        token = make_token({"realm_access": {"roles": ["user"]}})
        claims = authenticator.authenticate(token)
        with pytest.raises(InsufficientPermissions, match="admin"):
            authenticator.require_roles(claims, {"admin"})

    def test_require_scopes_pass(self, authenticator, make_token):
        token = make_token({"scope": "openid profile email"})
        claims = authenticator.authenticate(token)
        authenticator.require_scopes(claims, {"openid", "profile"})

    def test_require_scopes_fail(self, authenticator, make_token):
        token = make_token({"scope": "openid"})
        claims = authenticator.authenticate(token)
        with pytest.raises(InsufficientPermissions, match="profile"):
            authenticator.require_scopes(claims, {"openid", "profile"})

    def test_client_roles(self, authenticator, make_token):
        token = make_token({
            "resource_access": {
                "my-app": {"roles": ["viewer", "editor"]},
            },
        })
        claims = authenticator.authenticate(token)
        authenticator.require_roles(claims, {"viewer"}, client_id="my-app")
        with pytest.raises(InsufficientPermissions):
            authenticator.require_roles(claims, {"admin"}, client_id="my-app")
