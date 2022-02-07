# Base Django Channels auth token middlewares documentation


## BaseAuthTokenMiddleware(inner, token_regex=None)
> Base auth token middleware class.

> Could be used behind other auth middlewares like channels.auth.AuthMiddleware.

> Subclass of channels.auth.AuthMiddleware.

- inner - ASGI application (like channels.auth.AuthMiddleware inner argument)
- token_regex - token key validation regex, by default any string (".*")


### BaseAuthTokenMiddleware.get_user(scope):
> Async method.

> Returns user model instance or anonymous user instance.

- scope - channels.auth.AuthMiddleware scope

#### Stages
1. Get token key string from the scope.
2. Parse token key from token key string.
3. Get user instance by token key.
