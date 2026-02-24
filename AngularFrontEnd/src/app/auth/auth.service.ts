import { inject, Injectable, signal } from '@angular/core';
import Keycloak from 'keycloak-js';
import { KEYCLOAK_AUTH_CONFIG } from './auth.config';
import { UserProfile } from './auth.models';

@Injectable({ providedIn: 'root' })
export class AuthService {
  private readonly config = inject(KEYCLOAK_AUTH_CONFIG);
  private keycloak!: Keycloak;

  readonly isAuthenticated = signal(false);
  readonly userProfile = signal<UserProfile | null>(null);
  readonly roles = signal<string[]>([]);

  async init(): Promise<void> {
    this.keycloak = new Keycloak({
      url: this.config.url,
      realm: this.config.realm,
      clientId: this.config.clientId,
    });

    const authenticated = await this.keycloak.init({
      onLoad: 'check-sso',
      pkceMethod: 'S256',
      silentCheckSsoRedirectUri:
        window.location.origin + '/assets/silent-check-sso.html',
    });

    if (authenticated) {
      await this.loadUserProfile();
    }
  }

  async login(): Promise<void> {
    await this.keycloak.login();
  }

  async logout(): Promise<void> {
    await this.keycloak.logout({ redirectUri: window.location.origin });
  }

  async getToken(): Promise<string | undefined> {
    try {
      await this.keycloak.updateToken(30);
    } catch {
      await this.login();
    }
    return this.keycloak.token;
  }

  hasRole(role: string): boolean {
    return this.keycloak.hasRealmRole(role);
  }

  private async loadUserProfile(): Promise<void> {
    try {
      const profile = await this.keycloak.loadUserProfile();
      this.userProfile.set({
        id: profile.id ?? '',
        username: profile.username ?? '',
        email: profile.email ?? '',
        firstName: profile.firstName ?? '',
        lastName: profile.lastName ?? '',
        emailVerified: profile.emailVerified ?? false,
      });
      this.roles.set(this.keycloak.realmAccess?.roles ?? []);
      this.isAuthenticated.set(true);
    } catch {
      this.isAuthenticated.set(false);
    }
  }
}
