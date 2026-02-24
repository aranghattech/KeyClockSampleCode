# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This project is intented to create a reusable python module that would allow the authentication to be performed against Keyckock backend.

Use the reusable module in a fast api with modules to cerify the token.
Retun correct status codes.

## Expected Flow

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


## Things to keep in mind

1. Ensure the core validation module can be exported as reusable pip package
2. Ensure the authnetiction modules to be extendable
3. Ensure that the authentication module config details are kept in configuration file
4. Use clean code approch and make sure that modules are unit testable
5. Ensure the enterprise pattens to make it reliable.
