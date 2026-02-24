"""Shared test fixtures: RSA keypair, settings, and token factory."""

from __future__ import annotations

import json
import time
from typing import Any

import jwt
import pytest
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

from keycloak_auth import Authenticator, KeycloakSettings
from keycloak_auth.validators import JWKSTokenValidator, TokenValidator
from keycloak_auth.models import TokenClaims


# ---------------------------------------------------------------------------
# RSA keypair (generated once per test session)
# ---------------------------------------------------------------------------

@pytest.fixture(scope="session")
def rsa_private_key():
    return rsa.generate_private_key(public_exponent=65537, key_size=2048)


@pytest.fixture(scope="session")
def rsa_public_key(rsa_private_key):
    return rsa_private_key.public_key()


@pytest.fixture(scope="session")
def rsa_private_pem(rsa_private_key) -> bytes:
    return rsa_private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )


@pytest.fixture(scope="session")
def rsa_public_pem(rsa_public_key) -> bytes:
    return rsa_public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )


# ---------------------------------------------------------------------------
# Settings
# ---------------------------------------------------------------------------

@pytest.fixture()
def settings() -> KeycloakSettings:
    return KeycloakSettings(
        server_url="http://localhost:8080",
        realm="testrealm",
        client_id="test-client",
    )


# ---------------------------------------------------------------------------
# Token factory
# ---------------------------------------------------------------------------

@pytest.fixture()
def make_token(rsa_private_pem, settings):
    """Return a callable that creates signed JWT strings."""

    def _factory(
        claims_override: dict[str, Any] | None = None,
        *,
        expired: bool = False,
        headers: dict[str, Any] | None = None,
    ) -> str:
        now = int(time.time())
        payload: dict[str, Any] = {
            "sub": "user-123",
            "iss": settings.issuer,
            "iat": now,
            "exp": (now - 3600) if expired else (now + 3600),
            "preferred_username": "testuser",
            "email": "test@example.com",
            "name": "Test User",
            "realm_access": {"roles": ["user"]},
            "resource_access": {},
            "scope": "openid profile email",
        }
        if claims_override:
            payload.update(claims_override)

        return jwt.encode(
            payload,
            rsa_private_pem,
            algorithm="RS256",
            headers=headers or {"kid": "test-key-1"},
        )

    return _factory


# ---------------------------------------------------------------------------
# Direct-key validator (bypasses JWKS network call)
# ---------------------------------------------------------------------------

class DirectKeyValidator(TokenValidator):
    """Validator that uses a known public key directly (for testing)."""

    def __init__(self, public_pem: bytes, settings: KeycloakSettings):
        self._public_pem = public_pem
        self._settings = settings

    def validate(self, token: str) -> TokenClaims:
        from keycloak_auth.exceptions import TokenExpired, TokenInvalid

        kwargs: dict[str, Any] = {
            "algorithms": ["RS256"],
            "issuer": self._settings.issuer,
            "options": {"verify_aud": False},
        }
        try:
            payload = jwt.decode(token, self._public_pem, **kwargs)
        except jwt.ExpiredSignatureError as exc:
            raise TokenExpired() from exc
        except jwt.InvalidTokenError as exc:
            raise TokenInvalid(str(exc)) from exc
        return TokenClaims(**payload, raw=payload)


@pytest.fixture()
def validator(rsa_public_pem, settings) -> DirectKeyValidator:
    return DirectKeyValidator(rsa_public_pem, settings)


@pytest.fixture()
def authenticator(validator, settings) -> Authenticator:
    return Authenticator(settings, validator=validator)
