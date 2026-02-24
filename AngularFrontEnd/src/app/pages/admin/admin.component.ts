import { Component, inject, OnInit, signal } from '@angular/core';
import { AdminResponse, ApiService } from '../../core/services/api.service';

@Component({
  selector: 'app-admin',
  template: `
    <div class="max-w-2xl mx-auto">
      <h1 class="text-3xl font-bold text-slate-900 mb-6">Admin Dashboard</h1>

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
      } @else if (data()) {
        <div class="bg-white shadow rounded-lg p-6">
          <div class="flex items-center gap-3 mb-4">
            <span
              class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-green-100 text-green-800"
            >
              Admin Access Granted
            </span>
          </div>
          <p class="text-lg text-slate-700 mb-4">{{ data()!.message }}</p>
          <div>
            <h3 class="text-sm font-medium text-slate-500 mb-2">Your Roles</h3>
            <div class="flex flex-wrap gap-2">
              @for (role of data()!.realm_roles; track role) {
                <span
                  class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-purple-100 text-purple-800"
                >
                  {{ role }}
                </span>
              }
            </div>
          </div>
        </div>
      }
    </div>
  `,
})
export class AdminComponent implements OnInit {
  private readonly api = inject(ApiService);

  readonly data = signal<AdminResponse | null>(null);
  readonly loading = signal(true);
  readonly error = signal('');

  ngOnInit(): void {
    this.api.getAdmin().subscribe({
      next: (response) => {
        this.data.set(response);
        this.loading.set(false);
      },
      error: (err) => {
        this.error.set(err.error?.detail ?? 'Failed to load admin data');
        this.loading.set(false);
      },
    });
  }
}
