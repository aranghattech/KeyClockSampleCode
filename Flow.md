### Flow

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   Angular    │     │   Keycloak   │     │   Keycloak   │     │    Python    │
│     App      │     │    Server    │     │  Login Page  │     │   Backend    │
└──────┬───────┘     └──────┬───────┘     └──────┬───────┘     └──────┬───────┘
       │                    │                    │                    │
       │ 1. User clicks     │                    │                    │
       │    "Login"         │                    │                    │
       │                    │                    │                    │
       │ 2. Generate PKCE   │                    │                    │
       │    code_verifier & │                    │                    │
       │    code_challenge  │                    │                    │
       │                    │                    │                    │
       │ 3. Redirect ───────>                    │                    │
       │    /auth?                               │                    │
       │      client_id=app&                     │                    │
       │      redirect_uri=app/callback&         │                    │
       │      response_type=code&                │                    │
       │      code_challenge=xyz&                │                    │
       │      code_challenge_method=S256         │                    │
       │                    │                    │                    │
       │                    │ 4. Renders themed  │                    │
       │                    │    login form ─────>                    │
       │                    │                    │                    │
       │                    │ 5. User submits    │                    │
       │                    │    credentials <───│                    │
       │                    │                    │                    │
       │                    │ 6. Validates       │                    │
       │                    │    credentials     │                    │
       │                    │                    │                    │
       │ 7. Redirect back <─┤                    │                    │
       │    /callback?code=AUTH_CODE              │                    │
       │                    │                    │                    │
       │ 8. Exchange code   │                    │                    │
       │    for tokens ─────>                    │                    │
       │    POST /token                          │                    │
       │      grant_type=authorization_code&     │                    │
       │      code=AUTH_CODE&                    │                    │
       │      code_verifier=original_verifier    │                    │
       │                    │                    │                    │
       │ 9. Receive tokens <┤                    │                    │
       │    {                                    │                    │
       │      access_token,                      │                    │
       │      refresh_token,                     │                    │
       │      id_token                           │                    │
       │    }               │                    │                    │
       │                    │                    │                    │
       │ 10. API Request ───────────────────────────────────────────>│
       │     Authorization: Bearer <access_token>                    │
       │                    │                    │                    │
       │                    │ 11. Validate token │                    │
       │                    │<───────────────────────────────────────│
       │                    │  (via public key / │                    │
       │                    │   JWKS endpoint)   │                    │
       │                    │────────────────────────────────────────>
       │                    │                    │                    │
       │ 12. API Response <─────────────────────────────────────────│
       │                    │                    │                    │
```
