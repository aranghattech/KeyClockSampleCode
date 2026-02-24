export interface UserProfile {
  id: string;
  username: string;
  email: string;
  firstName: string;
  lastName: string;
  emailVerified: boolean;
}

export interface AuthState {
  isAuthenticated: boolean;
  userProfile: UserProfile | null;
  roles: string[];
  token: string | null;
}
