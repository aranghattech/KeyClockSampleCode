# Keycloak Auth - Python Backend

Reusable Python module for validating Keycloak-issued JWT tokens, with first-class FastAPI integration.

## Architecture

```
+-------------------+       +-------------------+       +-------------------+
|                   |       |                   |       |                   |
|  KeycloakSettings |------>|   Authenticator   |------>|  TokenValidator   |
|  (config.yaml /   |       |   (facade)        |       |  (ABC)            |
|   env vars)       |       |                   |       |                   |
+-------------------+       +-------------------+       +--------+----------+
                                                                 |
                                                    +------------+------------+
                                                    |                         |
                                          +---------+---------+   +-----------+-----------+
                                          | JWKSTokenValidator|   | IntrospectionToken    |
                                          | (offline, default)|   | Validator (online)    |
                                          +---------+---------+   +-----------+-----------+
                                                    |
                                          +---------+---------+
                                          | JWKSKeyManager    |
                                          | (PyJWKClient +    |
                                          |  TTL cache)       |
                                          +-------------------+
```

## Sequence Diagram

```
 Angular SPA                    Python Backend (FastAPI)                 Keycloak Server
 ──────────                     ───────────────────────                  ───────────────
      |                                   |                                    |
      |  (user already authenticated      |                                    |
      |   via Keycloak login page)        |                                    |
      |                                   |                                    |
      |   GET /api/profile                |                                    |
      |   Authorization: Bearer <token>   |                                    |
      |---------------------------------->|                                    |
      |                                   |                                    |
      |                                   |  1. Extract Bearer token           |
      |                                   |     from Authorization header      |
      |                                   |                                    |
      |                                   |  2. Fetch JWKS public keys         |
      |                                   |     (cached with TTL)              |
      |                                   |----------------------------------->|
      |                                   |                                    |
      |                                   |  3. Return JWKS key set            |
      |                                   |<-----------------------------------|
      |                                   |                                    |
      |                                   |  4. Verify JWT signature           |
      |                                   |     locally using public key       |
      |                                   |                                    |
      |                                   |  5. Validate claims:               |
      |                                   |     - exp (not expired)            |
      |                                   |     - iss (correct issuer)         |
      |                                   |     - aud (audience, if set)       |
      |                                   |                                    |
      |                                   |  6. Parse into TokenClaims         |
      |                                   |     (roles, scopes, user info)     |
      |                                   |                                    |
      |   200 OK                          |                                    |
      |   { "sub": "...",                 |                                    |
      |     "username": "...",            |                                    |
      |     "realm_roles": [...] }        |                                    |
      |<----------------------------------|                                    |
      |                                   |                                    |


 === Error Flows ===

      |   GET /api/profile                |                                    |
      |   (no Authorization header)       |                                    |
      |---------------------------------->|                                    |
      |                                   |  TokenMissing raised               |
      |   401 { "detail":                 |                                    |
      |     "Authorization header         |                                    |
      |      missing or invalid" }        |                                    |
      |<----------------------------------|                                    |
      |                                   |                                    |
      |   GET /api/profile                |                                    |
      |   Authorization: Bearer <expired> |                                    |
      |---------------------------------->|                                    |
      |                                   |  TokenExpired raised               |
      |   401 { "detail":                 |                                    |
      |     "Token has expired" }         |                                    |
      |<----------------------------------|                                    |
      |                                   |                                    |
      |   GET /api/admin                  |                                    |
      |   Authorization: Bearer <valid>   |                                    |
      |   (user lacks "admin" role)       |                                    |
      |---------------------------------->|                                    |
      |                                   |  InsufficientPermissions raised    |
      |   403 { "detail":                 |                                    |
      |     "Missing required roles:      |                                    |
      |      admin" }                     |                                    |
      |<----------------------------------|                                    |
      |                                   |                                    |
```

## Project Structure

```
PythonBackned/
├── pyproject.toml                        # Package config (hatchling build)
├── config.yaml                           # Default Keycloak configuration
├── .env.example                          # Environment variable reference
├── src/
│   ├── keycloak_auth/                    # Reusable pip package
│   │   ├── __init__.py                   # Public API exports
│   │   ├── config.py                     # KeycloakSettings (pydantic-settings)
│   │   ├── models.py                     # TokenClaims pydantic model
│   │   ├── exceptions.py                 # AuthError hierarchy (401/403/503)
│   │   ├── jwks.py                       # JWKSKeyManager (PyJWKClient + TTL cache)
│   │   ├── validators.py                 # TokenValidator ABC + implementations
│   │   ├── authenticator.py              # Authenticator facade
│   │   └── fastapi/
│   │       ├── __init__.py
│   │       ├── dependencies.py           # create_auth_dependency(), require_roles()
│   │       └── middleware.py             # register_auth_error_handlers()
│   └── app/                              # FastAPI consumer (not part of pip package)
│       ├── __init__.py
│       ├── main.py                       # App entry point, CORS, wiring
│       └── routes/
│           ├── __init__.py
│           └── protected.py              # /api/profile, /api/admin endpoints
└── tests/
    ├── conftest.py                       # RSA keypair, token factory fixtures
    ├── test_config.py
    ├── test_validators.py
    ├── test_authenticator.py
    ├── test_dependencies.py
    └── test_routes.py
```

## Quick Start

### 1. Install

```bash
# Development (includes FastAPI + test deps)
pip install -e ".[dev]"

# As a library in another project
pip install keycloak-auth

# With FastAPI support
pip install keycloak-auth[fastapi]
```

### 2. Configure

Edit `config.yaml` to match your Keycloak setup:

```yaml
keycloak:
  server_url: "http://localhost:8080"
  realm: "myrealm"
  client_id: "my-angular-app"
```

Or use environment variables (these override `config.yaml`):

```bash
export KEYCLOAK_SERVER_URL=http://localhost:8080
export KEYCLOAK_REALM=myrealm
export KEYCLOAK_CLIENT_ID=my-angular-app
```

### 3. Run the API

```bash
uvicorn src.app.main:app --reload
```

### 4. Test the endpoints

```bash
# Health check
curl http://localhost:8000/health

# Without token -> 401
curl http://localhost:8000/api/profile

# With valid Keycloak token -> 200
curl -H "Authorization: Bearer <your-token>" http://localhost:8000/api/profile

# Admin endpoint without admin role -> 403
curl -H "Authorization: Bearer <user-token>" http://localhost:8000/api/admin
```

## Usage as a Library

```python
from keycloak_auth import Authenticator, KeycloakSettings, TokenClaims
from keycloak_auth.fastapi import create_auth_dependency, require_roles, register_auth_error_handlers

# 1. Create settings and authenticator
settings = KeycloakSettings(server_url="http://localhost:8080", realm="myrealm")
authenticator = Authenticator(settings)

# 2. Wire into FastAPI
app = FastAPI()
register_auth_error_handlers(app)

get_current_user = create_auth_dependency(authenticator)

@app.get("/protected")
async def protected(user: TokenClaims = Depends(get_current_user)):
    return {"hello": user.preferred_username}

@app.get("/admin", dependencies=[Depends(require_roles(authenticator, {"admin"}))])
async def admin():
    return {"msg": "admin only"}
```

## Validation Strategies

### JWKS (default, offline)

Fetches Keycloak's public keys and validates JWT signatures locally. Keys are cached with a configurable TTL (default 300s). No network call per request after initial fetch.

### Introspection (online)

Calls Keycloak's token introspection endpoint for each request. Requires `client_secret`. Useful when you need real-time token revocation checks.

```python
from keycloak_auth import Authenticator, KeycloakSettings
from keycloak_auth.validators import IntrospectionTokenValidator

settings = KeycloakSettings(client_id="my-app", client_secret="secret")
validator = IntrospectionTokenValidator(settings)
authenticator = Authenticator(settings, validator=validator)
```

## Custom Validators

Implement the `TokenValidator` ABC to create your own strategy:

```python
from keycloak_auth.validators import TokenValidator
from keycloak_auth.models import TokenClaims

class MyCustomValidator(TokenValidator):
    def validate(self, token: str) -> TokenClaims:
        # your validation logic here
        ...
```

## Running Tests

```bash
pip install -e ".[dev]"
pytest tests/ -v
```

## Exception Hierarchy

| Exception                | HTTP Status | When                                |
|--------------------------|-------------|-------------------------------------|
| `TokenMissing`           | 401         | No Bearer token in request          |
| `TokenExpired`           | 401         | JWT `exp` claim is in the past      |
| `TokenInvalid`           | 401         | Bad signature, wrong issuer, etc.   |
| `InsufficientPermissions`| 403         | Valid token but missing roles/scopes|
| `KeycloakUnavailable`    | 503         | Cannot reach JWKS/introspection     |

## Requirements

- Python >= 3.11
- PyJWT[crypto] >= 2.8
- httpx >= 0.25
- pydantic >= 2.0
- pydantic-settings >= 2.0
- FastAPI >= 0.104 (optional)
