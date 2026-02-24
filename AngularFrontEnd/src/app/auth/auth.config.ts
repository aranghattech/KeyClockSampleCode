import { InjectionToken } from '@angular/core';

export interface KeycloakAuthConfig {
  url: string;
  realm: string;
  clientId: string;
}

export const KEYCLOAK_AUTH_CONFIG = new InjectionToken<KeycloakAuthConfig>(
  'KEYCLOAK_AUTH_CONFIG'
);
