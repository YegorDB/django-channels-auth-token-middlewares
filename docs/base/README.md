# Base middlewares


## BaseAuthTokenMiddleware(inner, token_regex=None)
> Base auth token middleware class.

> Could be used behind other auth middlewares like channels.auth.AuthMiddleware.

> Subclass of channels.auth.AuthMiddleware.

- inner - ASGI application (like channels.auth.AuthMiddleware inner argument)
- token_regex - token key validation regex, by default any string (".*")


### async BaseAuthTokenMiddleware.get_user(scope)
> Returns user model instance or anonymous user instance.

- scope - channels.auth.AuthMiddleware scope

#### Stages
1. Get token key string from the scope.
2. Parse token key from token key string.
3. Get user instance by token key.


### async BaseAuthTokenMiddleware.get_token_key_string(scope)
> Must be implemented by subclass to get token key string from the scope.

> Implementation need to returns string to parse token key from or None.

- scope - channels.auth.AuthMiddleware scope


### BaseAuthTokenMiddleware.parse_token_key(token_key_string)
> Parse token key from token key string by token key string regex.

> Returns token key as string or None.

- token_key_string - string to parse token key from


### property BaseAuthTokenMiddleware.token_key_string_regex()
> Returns regex to parse token key from token key string.

> Default is rf"({self.token_regex})"


### async BaseAuthTokenMiddleware.get_user_instance(token_key)
> Must be implemented by subclasses to get user instance by token key.

> Implementation need to returns user instance or None.

- token_key - token key as string


## HeaderAuthTokenMiddleware(inner, token_regex=None, header_name=None, keyword=None)
> Base middleware which parses auth token key from request header.

> Subclass of BaseAuthTokenMiddleware.

- inner - ASGI application (like channels.auth.AuthMiddleware inner argument)
- token_regex - token key validation regex, by default any string (".*")
- header_name - name of a header to get token key string from
- keyword - token key string keyword


### async HeaderAuthTokenMiddleware.get_token_key_string(scope)
> Get token key string from header by header name.

> Returns string to parse token key from or None.

- scope - channels.auth.AuthMiddleware scope


### property HeaderAuthTokenMiddleware.token_key_string_regex()
> Returns regex to parse token key from token key string.

> Default is rf"{self.keyword} ({self.token_regex})"


### async HeaderAuthTokenMiddleware.get_user_instance(token_key)
> Must be implemented by subclasses to get user instance by token key.

> Implementation need to returns user instance or None.

- token_key - token key as string


## CookieAuthTokenMiddleware(inner, token_regex=None, cookie_name=None)
> Base middleware which parses token key from request cookie.

> Subclass of BaseAuthTokenMiddleware.

- inner - ASGI application (like channels.auth.AuthMiddleware inner argument)
- token_regex - token key validation regex, by default any string (".*")
- cookie_name - name of a cookie to get token key string from


### async CookieAuthTokenMiddleware.get_token_key_string(scope)
> Get token key string from cookie by cookie name.

> Returns string to parse token key from or None.

- scope - channels.auth.AuthMiddleware scope


### async CookieAuthTokenMiddleware.get_user_instance(token_key)
> Must be implemented by subclasses to get user instance by token key.

> Implementation need to returns user instance or None.

- token_key - token key as string


## QueryStringAuthTokenMiddleware(inner, token_regex=None, query_param=None)
> Base middleware which parses token key from request query string.

> Subclass of BaseAuthTokenMiddleware.

- inner - ASGI application (like channels.auth.AuthMiddleware inner argument)
- token_regex - token key validation regex, by default any string (".*")
- query_param - name of a query param to get token key string from


### async QueryStringAuthTokenMiddleware.get_token_key_string(scope)
> Get token key string from query params by query param name.

> Returns string to parse token key from or None.

- scope - channels.auth.AuthMiddleware scope


### async QueryStringAuthTokenMiddleware.get_user_instance(token_key)
> Must be implemented by subclasses to get user instance by token key.

> Implementation need to returns user instance or None.

- token_key - token key as string
