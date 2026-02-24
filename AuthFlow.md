┌──────────┐      ┌──────────┐      ┌──────────┐      ┌──────────┐
│  Angular  │      │ Keycloak │      │ Keycloak │      │  Python  │
│   App     │      │  Server  │      │Login Page│      │ Backend  │
└────┬─────┘      └────┬─────┘      └────┬─────┘      └────┬─────┘
     │                  │                  │                  │
     │  1. User clicks "Login"             │                  │
     │──────────────────>                  │                  │
     │  (redirect to Keycloak              │                  │
     │   /auth?client_id=..&               │                  │
     │   redirect_uri=..&                  │                  │
     │   response_type=code&               │                  │
     │   code_challenge=...)               │                  │
     │                  │                  │                  │
     │                  │  2. Shows login  │                  │
     │                  │     form         │                  │
     │                  │<────────────────>│                  │
     │                  │                  │                  │
     │                  │  3. User enters  │                  │
     │                  │  username/password│                  │
     │                  │<─────────────────│                  │
     │                  │                  │                  │
     │  4. Redirect back to Angular        │                  │
     │<──────────────────                  │                  │
     │  (your-app.com/callback?code=ABC)   │                  │
     │                  │                  │                  │
     │  5. Exchange code for tokens        │                  │
     │──────────────────>                  │                  │
     │  (POST /token with code + verifier) │                  │
     │                  │                  │                  │
     │  6. Returns access_token,           │                  │
     │     refresh_token, id_token         │                  │
     │<──────────────────                  │                  │
     │                  │                  │                  │
     │  7. API call with Bearer token      │                  │
     │─────────────────────────────────────────────────────>  │
     │                  │                  │                  │
     │                  │    8. Validate token (via Keycloak  │
     │                  │       public key / introspection)   │
     │                  │<─────────────────────────────────── │
     │                  │                  │                  │
     │  9. API response │                  │                  │
     │<─────────────────────────────────────────────────────  │
