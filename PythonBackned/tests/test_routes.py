"""Tests for the sample app routes (kept lightweight — main logic tested elsewhere)."""

import pytest

from keycloak_auth.models import TokenClaims


class TestTokenClaimsModel:

    def test_realm_roles(self):
        claims = TokenClaims(
            sub="u1", exp=0,
            realm_access={"roles": ["admin", "user"]},
        )
        assert claims.realm_roles == {"admin", "user"}
        assert claims.has_role("admin")
        assert not claims.has_role("superadmin")

    def test_client_roles(self):
        claims = TokenClaims(
            sub="u1", exp=0,
            resource_access={"app1": {"roles": ["editor"]}},
        )
        assert claims.client_roles("app1") == {"editor"}
        assert claims.has_role("editor", client_id="app1")
        assert not claims.has_role("editor", client_id="app2")

    def test_scopes(self):
        claims = TokenClaims(sub="u1", exp=0, scope="openid profile")
        assert claims.scopes == {"openid", "profile"}

    def test_empty_scope(self):
        claims = TokenClaims(sub="u1", exp=0)
        assert claims.scopes == set()

    def test_has_any_role(self):
        claims = TokenClaims(
            sub="u1", exp=0,
            realm_access={"roles": ["viewer"]},
        )
        assert claims.has_any_role({"viewer", "admin"})
        assert not claims.has_any_role({"admin", "editor"})
