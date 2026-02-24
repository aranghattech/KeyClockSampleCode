"""Keycloak configuration powered by pydantic-settings.

Settings are loaded in this priority order (highest wins):
  1. Explicit constructor kwargs
  2. Environment variables (prefixed ``KEYCLOAK_``)
  3. ``config.yaml`` in the working directory
"""

from __future__ import annotations

from functools import cached_property
from pathlib import Path
from typing import Any

import yaml
from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


def _yaml_settings(settings: BaseSettings) -> dict[str, Any]:
    """Load values from a ``config.yaml`` next to the working directory."""
    config_path = Path("config.yaml")
    if not config_path.exists():
        return {}
    with config_path.open() as fh:
        data = yaml.safe_load(fh) or {}
    return data.get("keycloak", {})


class KeycloakSettings(BaseSettings):
    """Type-safe, validated Keycloak connection settings."""

    model_config = SettingsConfigDict(
        env_prefix="KEYCLOAK_",
        extra="ignore",
    )

    server_url: str = "http://localhost:8080"
    realm: str = "master"
    client_id: str = ""
    client_secret: str = ""
    audience: str = ""
    verify_ssl: bool = True

    @model_validator(mode="before")
    @classmethod
    def _load_yaml(cls, values: dict[str, Any]) -> dict[str, Any]:
        yaml_vals = _yaml_settings(cls)
        # YAML provides defaults; explicit values / env vars override.
        merged = {**yaml_vals, **{k: v for k, v in values.items() if v is not None}}
        return merged

    # --- Computed URIs ---------------------------------------------------

    @cached_property
    def issuer(self) -> str:
        return f"{self.server_url}/realms/{self.realm}"

    @cached_property
    def jwks_uri(self) -> str:
        return f"{self.issuer}/protocol/openid-connect/certs"

    @cached_property
    def introspection_uri(self) -> str:
        return f"{self.issuer}/protocol/openid-connect/token/introspect"
