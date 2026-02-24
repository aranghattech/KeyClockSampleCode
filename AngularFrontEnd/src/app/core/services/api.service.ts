import { HttpClient } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';

export interface ProfileResponse {
  sub: string;
  username: string;
  email: string;
  name: string;
  realm_roles: string[];
}

export interface AdminResponse {
  message: string;
  realm_roles: string[];
}

export interface HealthResponse {
  status: string;
}

@Injectable({ providedIn: 'root' })
export class ApiService {
  private readonly http = inject(HttpClient);
  private readonly baseUrl = environment.apiBaseUrl;

  getProfile(): Observable<ProfileResponse> {
    return this.http.get<ProfileResponse>(`${this.baseUrl}/api/profile`);
  }

  getAdmin(): Observable<AdminResponse> {
    return this.http.get<AdminResponse>(`${this.baseUrl}/api/admin`);
  }

  healthCheck(): Observable<HealthResponse> {
    return this.http.get<HealthResponse>(`${this.baseUrl}/health`);
  }
}
