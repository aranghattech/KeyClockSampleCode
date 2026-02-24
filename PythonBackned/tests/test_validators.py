"""Tests for token validators."""

import pytest

from keycloak_auth.exceptions import TokenExpired, TokenInvalid


class TestDirectKeyValidator:
    """Tests using the DirectKeyValidator from conftest."""

    def test_valid_token(self, validator, make_token):
        token = make_token()
        claims = validator.validate(token)
        assert claims.sub == "user-123"
        assert claims.preferred_username == "testuser"

    def test_expired_token(self, validator, make_token):
        token = make_token(expired=True)
        with pytest.raises(TokenExpired):
            validator.validate(token)

    def test_invalid_signature(self, validator, settings):
        """A token signed with a different key should fail."""
        import jwt as pyjwt
        from cryptography.hazmat.primitives.asymmetric import rsa
        from cryptography.hazmat.primitives import serialization
        import time

        other_key = rsa.generate_private_key(65537, 2048)
        other_pem = other_key.private_bytes(
            serialization.Encoding.PEM,
            serialization.PrivateFormat.PKCS8,
            serialization.NoEncryption(),
        )
        token = pyjwt.encode(
            {"sub": "bad", "iss": settings.issuer, "exp": int(time.time()) + 3600},
            other_pem,
            algorithm="RS256",
            headers={"kid": "other-key"},
        )
        with pytest.raises(TokenInvalid):
            validator.validate(token)

    def test_wrong_issuer(self, validator, make_token):
        token = make_token({"iss": "http://evil.example.com/realms/bad"})
        with pytest.raises(TokenInvalid):
            validator.validate(token)

    def test_claims_parsing(self, validator, make_token):
        token = make_token({
            "realm_access": {"roles": ["user", "editor"]},
            "scope": "openid profile",
        })
        claims = validator.validate(token)
        assert claims.realm_roles == {"user", "editor"}
        assert claims.scopes == {"openid", "profile"}
