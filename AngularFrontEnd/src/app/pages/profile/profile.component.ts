import { Component, inject, OnInit, signal } from '@angular/core';
import { ApiService, ProfileResponse } from '../../core/services/api.service';

@Component({
  selector: 'app-profile',
  template: `
    <div class="max-w-2xl mx-auto">
      <h1 class="text-3xl font-bold text-slate-900 mb-6">User Profile</h1>

      @if (loading()) {
        <div class="flex justify-center py-12">
          <div
            class="w-8 h-8 border-4 border-blue-600 border-t-transparent rounded-full animate-spin"
          ></div>
        </div>
      } @else if (error()) {
        <div class="px-6 py-4 bg-red-50 border border-red-200 text-red-700 rounded-lg">
          {{ error() }}
        </div>
      } @else if (profile()) {
        <div class="bg-white shadow rounded-lg divide-y divide-slate-200">
          <div class="px-6 py-5">
            <h2 class="text-lg font-semibold text-slate-900 mb-1">
              {{ profile()!.name || profile()!.username }}
            </h2>
            <p class="text-sm text-slate-500">{{ profile()!.email }}</p>
          </div>
          <dl class="divide-y divide-slate-200">
            <div class="px-6 py-4 sm:grid sm:grid-cols-3 sm:gap-4">
              <dt class="text-sm font-medium text-slate-500">Subject ID</dt>
              <dd class="mt-1 text-sm text-slate-900 sm:mt-0 sm:col-span-2">
                {{ profile()!.sub }}
              </dd>
            </div>
            <div class="px-6 py-4 sm:grid sm:grid-cols-3 sm:gap-4">
              <dt class="text-sm font-medium text-slate-500">Username</dt>
              <dd class="mt-1 text-sm text-slate-900 sm:mt-0 sm:col-span-2">
                {{ profile()!.username }}
              </dd>
            </div>
            <div class="px-6 py-4 sm:grid sm:grid-cols-3 sm:gap-4">
              <dt class="text-sm font-medium text-slate-500">Email</dt>
              <dd class="mt-1 text-sm text-slate-900 sm:mt-0 sm:col-span-2">
                {{ profile()!.email }}
              </dd>
            </div>
            <div class="px-6 py-4 sm:grid sm:grid-cols-3 sm:gap-4">
              <dt class="text-sm font-medium text-slate-500">Realm Roles</dt>
              <dd class="mt-1 text-sm sm:mt-0 sm:col-span-2">
                <div class="flex flex-wrap gap-2">
                  @for (role of profile()!.realm_roles; track role) {
                    <span
                      class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800"
                    >
                      {{ role }}
                    </span>
                  }
                </div>
              </dd>
            </div>
          </dl>
        </div>
      }
    </div>
  `,
})
export class ProfileComponent implements OnInit {
  private readonly api = inject(ApiService);

  readonly profile = signal<ProfileResponse | null>(null);
  readonly loading = signal(true);
  readonly error = signal('');

  ngOnInit(): void {
    this.api.getProfile().subscribe({
      next: (data) => {
        this.profile.set(data);
        this.loading.set(false);
      },
      error: (err) => {
        this.error.set(err.error?.detail ?? 'Failed to load profile');
        this.loading.set(false);
      },
    });
  }
}
