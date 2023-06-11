# Django REST framework middlewares


## DRFAuthTokenMiddleware(inner, token_regex=r"[0-9a-f]{40}", header_name="Authorization", keyword="Token")
> Django REST framework [token authentication](https://www.django-rest-framework.org/api-guide/authentication/#tokenauthentication) auth token middleware class.

> Subclass of HeaderAuthTokenMiddleware.

- inner - ASGI application (like channels.auth.AuthMiddleware inner argument)
- token_regex - token key validation regex, by default r"[0-9a-f]{40}"
- header_name - name of a header to get token key string from, by default "Authorization"
- keyword - token key string keyword, by default "Token"


### async DRFAuthTokenMiddleware.get_user_instance(token_key)
> Get user instance by token key.

> Returns user instance or None.

- token_key - token key as a string


## QueryStringDRFAuthTokenMiddleware(inner, token_regex=r".*", query_param="token")
> Django REST framework auth token middleware class with query string token.

> Subclass of QueryStringAuthTokenMiddleware.

- inner - ASGI application (like channels.auth.AuthMiddleware inner argument)
- token_regex - token key validation regex, by default r".*"
- query_param - name of a query param to get token key string from, by default "token"


### async QueryStringDRFAuthTokenMiddleware.get_user_instance(token_key)
> Get user instance by token key.

> Returns user instance or None.

- token_key - token key as a string


## DRFAuthTokenMiddlewareStack(inner)
> Django REST framework auth token middleware stack factory function.

> Includes DRFAuthTokenMiddleware and QueryStringDRFAuthTokenMiddleware.

- inner - ASGI application (like channels.auth.AuthMiddleware inner argument)


## SimpleJWTAuthTokenMiddleware(inner, token_regex=r".*", header_name="Authorization", keyword="Bearer")
> [Simple JWT](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/index.html) auth token middleware class.

> Subclass of HeaderAuthTokenMiddleware.

- inner - ASGI application (like channels.auth.AuthMiddleware inner argument)
- token_regex - token key validation regex, by default any string (r".*")
- header_name - name of a header to get token key string from, by default "Authorization"
- keyword - token key string keyword, by default "Bearer"


### async SimpleJWTAuthTokenMiddleware.get_user_instance(token_key)
> Get user instance by token key.

> Returns user instance or None.

- token_key - token key as a string


## QueryStringSimpleJWTAuthTokenMiddleware(inner, token_regex=r".*", query_param="token")
> Simple JWT auth token middleware class with query string token.

> Subclass of QueryStringAuthTokenMiddleware.

- inner - ASGI application (like channels.auth.AuthMiddleware inner argument)
- token_regex - token key validation regex, by default any string (r".*")
- query_param - name of a query param to get token key string from, by default "token"


### async QueryStringSimpleJWTAuthTokenMiddleware.get_user_instance(token_key)
> Get user instance by token key.

> Returns user instance or None.

- token_key - token key as a string


## SimpleJWTAuthTokenMiddlewareStack(inner)
> Simple JWT auth token middleware stack factory function.

> Includes SimpleJWTAuthTokenMiddleware and QueryStringSimpleJWTAuthTokenMiddleware.

- inner - ASGI application (like channels.auth.AuthMiddleware inner argument)
