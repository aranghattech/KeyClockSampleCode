```
import { HttpInterceptorFn } from '@angular/common/http';

export const realmInterceptor: HttpInterceptorFn = (req, next) => {
  // 1. Retrieve the realm we saved during app startup
  let currentRealm = 'master'; // default fallback
  
  if (typeof window !== 'undefined') {
    currentRealm = localStorage.getItem('tenant_realm') || 'master';
  }

  // 2. Clone the outgoing request and append the custom header
  const modifiedReq = req.clone({
    setHeaders: {
      'X-Relm': currentRealm
    }
  });

  // 3. Pass the modified request to the next interceptor (or backend)
  return next(modifiedReq);
};
```
