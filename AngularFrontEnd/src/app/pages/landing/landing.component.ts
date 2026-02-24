import { Component, inject, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { AuthService } from '../../auth';

@Component({
  selector: 'app-landing',
  template: `
    <div class="flex flex-col items-center justify-center py-20">
      @if (errorMessage) {
        <div
          class="mb-8 px-6 py-4 bg-red-50 border border-red-200 text-red-700 rounded-lg"
        >
          {{ errorMessage }}
        </div>
      }

      <h1 class="text-4xl font-bold text-slate-900 mb-4">
        Welcome to Keycloak App
      </h1>
      <p class="text-lg text-slate-600 mb-8 text-center max-w-xl">
        A sample Angular application demonstrating authentication with Keycloak
        using the Authorization Code + PKCE flow.
      </p>

      @if (!auth.isAuthenticated()) {
        <button
          (click)="auth.login()"
          class="px-8 py-3 text-lg font-semibold bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors shadow-md cursor-pointer"
        >
          Sign in with Keycloak
        </button>
      } @else {
        <div class="text-center">
          <p class="text-xl text-slate-700 mb-4">
            Hello, <span class="font-semibold">{{ auth.userProfile()?.firstName }}</span>!
          </p>
          <p class="text-slate-500">
            Use the navigation above to explore your profile or admin pages.
          </p>
        </div>
      }
    </div>
  `,
})
export class LandingComponent implements OnInit {
  readonly auth = inject(AuthService);
  private readonly route = inject(ActivatedRoute);
  errorMessage = '';

  ngOnInit(): void {
    this.route.queryParams.subscribe((params) => {
      if (params['error'] === 'insufficient_permissions') {
        this.errorMessage = 'You do not have sufficient permissions to access that page.';
      }
    });
  }
}
