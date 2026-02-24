"""Token validation strategies (Strategy pattern).

Two concrete implementations:
  - ``JWKSTokenValidator`` – offline, verifies the signature locally.
  - ``IntrospectionTokenValidator`` – online, calls Keycloak's introspection
    endpoint (requires ``client_secret``).
"""

from __future__ import annotations

from abc import ABC, abstractmethod

import httpx
import jwt

from .config import KeycloakSettings
from .exceptions import (
    KeycloakUnavailable,
    TokenExpired,
    TokenInvalid,
)
from .jwks import JWKSKeyManager
from .models import TokenClaims


class TokenValidator(ABC):
    """Interface that every validator must implement."""

    @abstractmethod
    def validate(self, token: str) -> TokenClaims:
        """Validate *token* and return parsed claims.

        Raises an :class:`AuthError` subclass on failure.
        """


class JWKSTokenValidator(TokenValidator):
    """Validates tokens offline using the JWKS public key."""

    def __init__(
        self,
        settings: KeycloakSettings,
        key_manager: JWKSKeyManager | None = None,
    ):
        self._settings = settings
        self._key_manager = key_manager or JWKSKeyManager(settings)

    def validate(self, token: str) -> TokenClaims:
        key = self._key_manager.get_signing_key(token)

        decode_options: dict = {}
        algorithms = ["RS256"]
        kwargs: dict = {
            "algorithms": algorithms,
            "options": decode_options,
        }
        if self._settings.audience:
            kwargs["audience"] = self._settings.audience
        else:
            decode_options["verify_aud"] = False

        kwargs["issuer"] = self._settings.issuer

        try:
            payload = jwt.decode(token, key, **kwargs)
        except jwt.ExpiredSignatureError as exc:
            raise TokenExpired() from exc
        except jwt.InvalidTokenError as exc:
            raise TokenInvalid(str(exc)) from exc

        return TokenClaims(**payload, raw=payload)


class IntrospectionTokenValidator(TokenValidator):
    """Validates tokens online via Keycloak's introspection endpoint."""

    def __init__(self, settings: KeycloakSettings):
        self._settings = settings
        if not settings.client_secret:
            raise ValueError(
                "client_secret is required for introspection validation"
            )

    def validate(self, token: str) -> TokenClaims:
        try:
            response = httpx.post(
                self._settings.introspection_uri,
                data={
                    "token": token,
                    "client_id": self._settings.client_id,
                    "client_secret": self._settings.client_secret,
                },
                verify=self._settings.verify_ssl,
                timeout=10.0,
            )
            response.raise_for_status()
        except httpx.HTTPError as exc:
            raise KeycloakUnavailable(
                f"Introspection request failed: {exc}"
            ) from exc

        payload = response.json()
        if not payload.get("active"):
            raise TokenInvalid("Token is not active")

        return TokenClaims(**payload, raw=payload)
