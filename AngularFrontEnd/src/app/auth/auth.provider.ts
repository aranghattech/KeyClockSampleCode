import { APP_INITIALIZER, EnvironmentProviders, makeEnvironmentProviders } from '@angular/core';
import { KeycloakAuthConfig, KEYCLOAK_AUTH_CONFIG } from './auth.config';
import { AuthService } from './auth.service';
import { keycloakInitFactory } from './keycloak-init.factory';

export function provideKeycloakAuth(config: KeycloakAuthConfig): EnvironmentProviders {
  return makeEnvironmentProviders([
    { provide: KEYCLOAK_AUTH_CONFIG, useValue: config },
    {
      provide: APP_INITIALIZER,
      useFactory: keycloakInitFactory,
      deps: [AuthService],
      multi: true,
    },
  ]);
}
