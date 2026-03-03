```
// This regex matches any URL that does NOT start with http:// or https://
const relativeUrlCondition = createInterceptorCondition<IncludeBearerTokenCondition>({
  urlPattern: /^(?!(http:\/\/|https:\/\/)).*$/i 
});

// Inside your appConfig providers:
{
  provide: INCLUDE_BEARER_TOKEN_INTERCEPTOR_CONFIG,
  useValue: [relativeUrlCondition]
}
```
