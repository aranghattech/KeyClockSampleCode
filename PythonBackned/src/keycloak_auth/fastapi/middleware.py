"""FastAPI error handlers for authentication exceptions.

Call :func:`register_auth_error_handlers` once during app startup to
convert :class:`AuthError` exceptions into consistent JSON responses.
"""

from __future__ import annotations

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from ..exceptions import AuthError


def register_auth_error_handlers(app: FastAPI) -> None:
    """Register an exception handler that maps :class:`AuthError` to JSON."""

    @app.exception_handler(AuthError)
    async def _auth_error_handler(request: Request, exc: AuthError) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail},
        )
