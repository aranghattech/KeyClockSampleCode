"""FastAPI application entry point."""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from keycloak_auth import Authenticator, KeycloakSettings
from keycloak_auth.fastapi import register_auth_error_handlers

settings = KeycloakSettings()
authenticator = Authenticator(settings)

app = FastAPI(title="Keycloak Protected API", version="0.1.0")

# CORS — allow the Angular frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

register_auth_error_handlers(app)


# Deferred import to avoid circular dependency (routes imports authenticator)
def _include_routes() -> None:
    from .routes.protected import router  # noqa: WPS433

    app.include_router(router)


_include_routes()


@app.get("/health")
async def health():
    return {"status": "ok"}
