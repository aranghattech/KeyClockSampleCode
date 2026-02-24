"""FastAPI integration helpers for keycloak-auth."""

from .dependencies import create_auth_dependency, require_roles
from .middleware import register_auth_error_handlers

__all__ = [
    "create_auth_dependency",
    "register_auth_error_handlers",
    "require_roles",
]
