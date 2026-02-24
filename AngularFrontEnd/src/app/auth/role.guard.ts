import { inject } from '@angular/core';
import { CanActivateFn, Router } from '@angular/router';
import { AuthService } from './auth.service';

export function roleGuard(...requiredRoles: string[]): CanActivateFn {
  return async () => {
    const authService = inject(AuthService);
    const router = inject(Router);

    if (!authService.isAuthenticated()) {
      await authService.login();
      return false;
    }

    const hasRequiredRole = requiredRoles.some((role) =>
      authService.hasRole(role)
    );

    if (!hasRequiredRole) {
      return router.createUrlTree(['/'], {
        queryParams: { error: 'insufficient_permissions' },
      });
    }

    return true;
  };
}
