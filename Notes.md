```
const getDynamicRealm = (): string => {
  if (typeof window !== 'undefined') {
    const urlParams = new URLSearchParams(window.location.search);
    // Checking for both 'realm' and your 'relm' spelling
    const realm = urlParams.get('realm') || urlParams.get('relm');
    
    if (!realm) {
      console.warn('No realm provided in URL. Defaulting to master.');
    }
    
    return realm || 'master'; 
  }
  return 'master'; // Fallback for SSR builds
};
```
