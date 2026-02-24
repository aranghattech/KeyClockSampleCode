"""Tests for KeycloakSettings."""

import os

from keycloak_auth import KeycloakSettings


def test_computed_uris():
    s = KeycloakSettings(server_url="http://kc:8080", realm="demo")
    assert s.issuer == "http://kc:8080/realms/demo"
    assert s.jwks_uri == "http://kc:8080/realms/demo/protocol/openid-connect/certs"
    assert "introspect" in s.introspection_uri


def test_explicit_values_override_yaml():
    s = KeycloakSettings(realm="explicit-realm", server_url="http://explicit:8080")
    assert s.realm == "explicit-realm"
    assert s.verify_ssl is True


def test_env_override(monkeypatch):
    monkeypatch.setenv("KEYCLOAK_REALM", "from-env")
    monkeypatch.setenv("KEYCLOAK_SERVER_URL", "http://env-host:9090")
    s = KeycloakSettings()
    assert s.realm == "from-env"
    assert s.server_url == "http://env-host:9090"
