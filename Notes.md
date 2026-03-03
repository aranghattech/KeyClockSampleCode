```
// This regex matches any URL that does NOT start with http:// or https://
const matchAllHttpCondition = createInterceptorCondition<IncludeBearerTokenCondition>({
  urlPattern: /^https?:\/\/.*/i, 
  bearerPrefix: 'Bearer'
});
```
