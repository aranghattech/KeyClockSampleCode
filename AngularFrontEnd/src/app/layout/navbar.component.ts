import { Component, inject } from '@angular/core';
import { RouterLink, RouterLinkActive } from '@angular/router';
import { AuthService } from '../auth';

@Component({
  selector: 'app-navbar',
  imports: [RouterLink, RouterLinkActive],
  template: `
    <nav class="bg-slate-800 text-white shadow-lg">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex items-center justify-between h-16">
          <div class="flex items-center gap-6">
            <a routerLink="/" class="text-xl font-bold tracking-tight">
              Keycloak App
            </a>
            <div class="hidden sm:flex items-center gap-1">
              <a
                routerLink="/"
                routerLinkActive="bg-slate-700"
                [routerLinkActiveOptions]="{ exact: true }"
                class="px-3 py-2 rounded-md text-sm font-medium hover:bg-slate-700 transition-colors"
              >
                Home
              </a>
              @if (auth.isAuthenticated()) {
                <a
                  routerLink="/profile"
                  routerLinkActive="bg-slate-700"
                  class="px-3 py-2 rounded-md text-sm font-medium hover:bg-slate-700 transition-colors"
                >
                  Profile
                </a>
              }
              @if (auth.hasRole('admin')) {
                <a
                  routerLink="/admin"
                  routerLinkActive="bg-slate-700"
                  class="px-3 py-2 rounded-md text-sm font-medium hover:bg-slate-700 transition-colors"
                >
                  Admin
                </a>
              }
            </div>
          </div>
          <div class="flex items-center gap-4">
            @if (auth.isAuthenticated()) {
              <span class="text-sm text-slate-300">
                {{ auth.userProfile()?.username }}
              </span>
              <button
                (click)="auth.logout()"
                class="px-4 py-2 text-sm font-medium bg-red-600 hover:bg-red-700 rounded-md transition-colors cursor-pointer"
              >
                Logout
              </button>
            } @else {
              <button
                (click)="auth.login()"
                class="px-4 py-2 text-sm font-medium bg-blue-600 hover:bg-blue-700 rounded-md transition-colors cursor-pointer"
              >
                Login
              </button>
            }
          </div>
        </div>
      </div>
    </nav>
  `,
})
export class NavbarComponent {
  readonly auth = inject(AuthService);
}
