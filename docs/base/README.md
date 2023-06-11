# Base middlewares


## BaseAuthTokenMiddleware(inner, token_regex=r".*")
> Base auth token middleware class.

> Could be used behind other auth middlewares like channels.auth.AuthMiddleware.

> Subclass of channels.auth.AuthMiddleware.

- inner - ASGI application (like channels.auth.AuthMiddleware inner argument)
- token_regex - token key validation regex, by default any string (r".*")


### async BaseAuthTokenMiddleware.get_user(scope)
> Returns user model instance or anonymous user instance.

- scope - channels.auth.AuthMiddleware scope

#### Stages
1. Get token key string from the scope.
2. Parse token key from token key string.
3. Get user instance by token key.


### BaseAuthTokenMiddleware.get_token_key_string(scope)
> Must be implemented by subclass to get token key string from the scope.

> Implementation need to returns string to parse token key from or None.

- scope - channels.auth.AuthMiddleware scope


### BaseAuthTokenMiddleware.parse_token_key(token_key_string)
> Parse token key from token key string by token key string regex.

> By default returns full token key string content.

> Returns token key as string or None.

- token_key_string - string to parse token key from


### property BaseAuthTokenMiddleware.token_key_string_regex()
> Returns regex to parse token key from token key string.

> Token key need to be in first group.

> Default is rf"({self.token_regex})"


### async BaseAuthTokenMiddleware.get_user_instance(token_key)
> Must be implemented by subclasses to get user instance by token key.

> Implementation need to returns user instance or None.

- token_key - token key as string


### async BaseAuthTokenMiddleware.get_scope_header_value(scope, header_name)
> Returns scope header value by name or None

- scope - channels.auth.AuthMiddleware scope
- header_name - header name as a string or bytes


## HeaderAuthTokenMiddleware(inner, token_regex=r".*", header_name=None, keyword=None)
> Base middleware which parses auth token key from request header.

> Subclass of BaseAuthTokenMiddleware.

- inner - ASGI application (like channels.auth.AuthMiddleware inner argument)
- token_regex - token key validation regex, by default any string (r".*")
- header_name - name of a header to get token key string from
- keyword - token key string keyword


### HeaderAuthTokenMiddleware.get_token_key_string(scope)
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


## CookieAuthTokenMiddleware(inner, token_regex=r".*", cookie_name=None)
> Base middleware which parses token key from request cookie.

> Subclass of BaseAuthTokenMiddleware.

- inner - ASGI application (like channels.auth.AuthMiddleware inner argument)
- token_regex - token key validation regex, by default any string (r".*")
- cookie_name - name of a cookie to get token key string from


### CookieAuthTokenMiddleware.get_token_key_string(scope)
> Get token key string from cookie by cookie name.

> Returns string to parse token key from or None.

- scope - channels.auth.AuthMiddleware scope


### async CookieAuthTokenMiddleware.get_user_instance(token_key)
> Must be implemented by subclasses to get user instance by token key.

> Implementation need to returns user instance or None.

- token_key - token key as string


## QueryStringAuthTokenMiddleware(inner, token_regex=r".*", query_param=None)
> Base middleware which parses token key from request query string.

> Subclass of BaseAuthTokenMiddleware.

- inner - ASGI application (like channels.auth.AuthMiddleware inner argument)
- token_regex - token key validation regex, by default any string (r".*")
- query_param - name of a query param to get token key string from


### QueryStringAuthTokenMiddleware.get_token_key_string(scope)
> Get token key string from query params by query param name.

> Returns string to parse token key from or None.

- scope - channels.auth.AuthMiddleware scope


### async QueryStringAuthTokenMiddleware.get_user_instance(token_key)
> Must be implemented by subclasses to get user instance by token key.

> Implementation need to returns user instance or None.

- token_key - token key as string
