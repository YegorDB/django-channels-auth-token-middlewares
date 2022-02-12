# Django REST framework middlewares


## DRFAuthTokenMiddleware(inner, token_regex="[0-9a-f]{40}", header_name="Authorization", keyword="Token")
> Django REST framework auth token middleware class.

> Subclass of HeaderAuthTokenMiddleware.

> Made for [token authentication](https://www.django-rest-framework.org/api-guide/authentication/#tokenauthentication)

- inner - ASGI application (like channels.auth.AuthMiddleware inner argument)
- token_regex - token key validation regex, by default "[0-9a-f]{40}"
- header_name - name of a header to get token key string from, by default "Authorization"
- keyword - token key string keyword, by default "Token"


### async DRFAuthTokenMiddleware.get_user_instance(token_key)
> Get user instance by token key.

> Returns user instance or None.

- token_key - token key as string
