import { AuthService } from './auth.service';

export function keycloakInitFactory(authService: AuthService): () => Promise<void> {
  return () => authService.init();
}
