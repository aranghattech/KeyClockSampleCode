
import { KeycloakService } from 'keycloak-angular';

export function initializeKeycloak(keycloak: KeycloakService) {
  return () => {
    // 1. Read the query string before Angular routing takes over
    const urlParams = new URLSearchParams(window.location.search);
    
    // 2. Extract the realm (checking for both 'realm' and 'relm')
    const dynamicRealm = urlParams.get('realm') || urlParams.get('relm');

    if (!dynamicRealm) {
      console.error('No realm provided in the URL! Booting with default or halting.');
      // Depending on your requirements, you might want to redirect to an error page here
      // window.location.href = '/missing-realm-error';
    }

    // 3. Initialize Keycloak
    return keycloak.init({
      config: {
        url: 'http://localhost:8080', // The Keycloak server URL
        realm: dynamicRealm || 'master', // Fallback to a default if absolutely necessary
        clientId: 'angular-client' // The Client ID you created in Step 3 of Keycloak setup
      },
      initOptions: {
        // 'login-required' forces a redirect to Keycloak if not logged in.
        // If you want public pages, use 'check-sso' instead.
        onLoad: 'login-required', 
        checkLoginIframe: false // Recommended for modern browsers to prevent third-party cookie issues
      },
      // Automatically adds the Bearer token to your outgoing HTTP requests
      enableBearerInterceptor: true, 
      bearerPrefix: 'Bearer',
    });
  };
}
