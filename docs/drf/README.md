# Django REST framework middlewares


## DRFAuthTokenMiddleware(inner, token_regex=r"[0-9a-f]{40}", header_name="Authorization", keyword="Token")
> Django REST framework [token authentication](https://www.django-rest-framework.org/api-guide/authentication/#tokenauthentication) middleware class.

> Subclass of HeaderAuthTokenMiddleware.

- inner - ASGI application (like channels.auth.AuthMiddleware inner argument)
- token_regex - token key validation regex, by default r"[0-9a-f]{40}"
- header_name - name of a header to get token key string from, by default "Authorization"
- keyword - token key string keyword, by default "Token"


### async DRFAuthTokenMiddleware.get_user_instance(token_key)
> Get user instance by token key.

> Returns user instance or None.

- token_key - token key as string


## SimpleJWTAuthTokenMiddleware(inner, token_regex=r".*", header_name="Authorization", keyword="Bearer")
> [Simple JWT](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/index.html) middleware class.

> Subclass of HeaderAuthTokenMiddleware.

- inner - ASGI application (like channels.auth.AuthMiddleware inner argument)
- token_regex - token key validation regex, by default any string (r".*")
- header_name - name of a header to get token key string from, by default "Authorization"
- keyword - token key string keyword, by default "Bearer"


### async SimpleJWTAuthTokenMiddleware.get_user_instance(token_key)
> Get user instance by token key.

> Returns user instance or None.

- token_key - token key as string
