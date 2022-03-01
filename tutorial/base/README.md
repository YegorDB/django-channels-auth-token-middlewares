# Base classes inheritance

- [BaseAuthTokenMiddleware](#baseauthtokenmiddleware)
- [HeaderAuthTokenMiddleware](#headerauthtokenmiddleware)
- [CookieAuthTokenMiddleware](#cookieauthtokenmiddleware)
- [CustomQueryStringAuthTokenMiddleware](#customquerystringauthtokenmiddleware)


## Intro

### Get user instance by request scope
> There are 3 stages to get user instance by request scope

#### Stages
1. Get token key string from request scope (get_token_key_string method).
2. Parse token key from token key string (parse_token_key method), by default returns full token key string content.
3. Get user instance by token key (get_user_instance async method).


## BaseAuthTokenMiddleware

> Base middleware which populates scope["user"] by authorization token key.

> Could be used behind other auth middlewares like AuthMiddleware.


### Required overrides

> get_token_key_string and get_user_instance methods need to be overrided

```python
from django.contrib.auth import get_user_model

from channels.db import database_sync_to_async

from channels_auth_token_middlewares.middleware import BaseAuthTokenMiddleware


class CustomAuthTokenMiddleware(BaseAuthTokenMiddleware):
    """
    Middleware which parse user id from "User-Id" request header.

    Header example
    User-Id: 4
    User with id 4 or anonymous user would be populated to scope["user"].
    """

    def get_token_key_string(self, scope):
        headers = dict(scope["headers"])
        value = headers.get(b"user-id")
        if not value:
            return None
        return value.decode()

    @database_sync_to_async
    def get_user_instance(self, token_key):
        User = get_user_model()
        try:
            return User.objects.get(id=token_key)
        except User.DoesNotExist:
            return None
```

### Additional overrides

> Token key is validated by token_regex

> By defaul token_regex is any string (r".*")

```python
class CustomAuthTokenMiddleware2(CustomAuthTokenMiddleware):

    # only ids from 1 to 9 would be handled
    token_regex = r"[1-9]" # may be passed as init kwarg
```

> token_key_string_regex is used to parse token key from token key string

> By defaul token_key_string_regex includes only token key content (rf"({self.token_regex})")

> Token key need to be in first group


```python
class CustomAuthTokenMiddleware3(CustomAuthTokenMiddleware2):
    """
    Header example
    User-Id: foo 4 bar
    """

    @property
    def token_key_string_regex(self):
        return rf"foo ({self.token_regex}) bar"
```


## HeaderAuthTokenMiddleware

> Base middleware which parses token key from request header

### Required overrides

> get_user_instance method need to be overrided

```python
from django.contrib.auth import get_user_model

from channels.db import database_sync_to_async

from channels_auth_token_middlewares.middleware import HeaderAuthTokenMiddleware


class CustomHeaderAuthTokenMiddleware(HeaderAuthTokenMiddleware):
    """
    Header example
    User-Authorization: Id 4
    User with id 4 or anonymous user would be populated to scope["user"].
    """

    header_name = "User-Authorization" # may be passed as init kwarg
    keyword = "Id" # may be passed as init kwarg

    @database_sync_to_async
    def get_user_instance(self, token_key):
        User = get_user_model()
        try:
            return User.objects.get(id=token_key)
        except User.DoesNotExist:
            return None
```

### Additional overrides

> Same as BaseAuthTokenMiddleware


## CookieAuthTokenMiddleware

> Base middleware which parses token key from request cookie

### Required overrides

> get_user_instance method need to be overrided

```python
from django.contrib.auth import get_user_model

from channels.db import database_sync_to_async

from channels_auth_token_middlewares.middleware import CookieAuthTokenMiddleware


class CustomCookieAuthTokenMiddleware(CookieAuthTokenMiddleware):
    """
    Cookie example
    user_id: 4
    User with id 4 or anonymous user would be populated to scope["user"].
    """

    cookie_name = "user_id" # may be passed as init kwarg

    @database_sync_to_async
    def get_user_instance(self, token_key):
        User = get_user_model()
        try:
            return User.objects.get(id=token_key)
        except User.DoesNotExist:
            return None
```

### Additional overrides

> Same as BaseAuthTokenMiddleware


## QueryStringAuthTokenMiddleware

> Base middleware which parses token key from request query string

### Required overrides

> get_user_instance method need to be overrided

```python
from django.contrib.auth import get_user_model

from channels.db import database_sync_to_async

from channels_auth_token_middlewares.middleware import QueryStringAuthTokenMiddleware


class CustomQueryStringAuthTokenMiddleware(QueryStringAuthTokenMiddleware):
    """
    Query string example
    ?user_id=4
    User with id 4 or anonymous user would be populated to scope["user"].
    """

    query_param = "user_id" # may be passed as init kwarg

    @database_sync_to_async
    def get_user_instance(self, token_key):
        User = get_user_model()
        try:
            return User.objects.get(id=token_key)
        except User.DoesNotExist:
            return None
```

### Additional overrides

> Same as BaseAuthTokenMiddleware
