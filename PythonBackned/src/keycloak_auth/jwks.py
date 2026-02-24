"""JWKS key management using PyJWT's built-in PyJWKClient.

``PyJWKClient`` handles:
  - Fetching the JWKS endpoint
  - Matching the ``kid`` header to the correct key
  - TTL-based caching (``lifespan`` parameter)
"""

from __future__ import annotations

import jwt
from jwt import PyJWKClient

from .config import KeycloakSettings
from .exceptions import KeycloakUnavailable


class JWKSKeyManager:
    """Thin wrapper around :class:`jwt.PyJWKClient` with sensible defaults."""

    def __init__(self, settings: KeycloakSettings, cache_ttl: int = 300):
        self._settings = settings
        try:
            self._client = PyJWKClient(
                uri=settings.jwks_uri,
                cache_jwk_set=True,
                lifespan=cache_ttl,
            )
        except Exception as exc:
            raise KeycloakUnavailable(
                f"Failed to initialise JWKS client: {exc}"
            ) from exc

    def get_signing_key(self, token: str) -> jwt.algorithms.RSAPublicKey:
        """Return the RSA public key that matches the token's ``kid``."""
        try:
            signing_key = self._client.get_signing_key_from_jwt(token)
        except (jwt.PyJWKClientError, jwt.DecodeError) as exc:
            raise KeycloakUnavailable(
                f"Unable to fetch signing key: {exc}"
            ) from exc
        return signing_key.key
