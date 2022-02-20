# Base classes inheritance


## Intro

### Get user instance by request scope
> There are 3 stages to get user instance by request scope

#### Stages
1. Get token key string from request scope (get_token_key_string method).
2. Parse token key from token key string (parse_token_key method), by default returns full token key string content.
3. Get user instance by token key (get_user_instance async method).


## BaseAuthTokenMiddleware

### Required overrides

> get_token_key_string and get_user_instance methods need to be overrided

```python
from django.contrib.auth import get_user_model

from channels.db import database_sync_to_async

from channels_auth_token_middlewares import HeaderAuthTokenMiddleware


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
    token_regex = r"[1-9]"
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

### Required overrides

> To inherit HeaderAuthTokenMiddleware you need to override "get_user_instance(token_key)" async method

```python
from django.contrib.auth import get_user_model

from channels.db import database_sync_to_async

from channels_auth_token_middlewares import HeaderAuthTokenMiddleware


class CustomHeaderAuthTokenMiddleware(HeaderAuthTokenMiddleware):
    """
    Header example
    Custom-Header-Name: CustomKeyword 12
    User with id 12 or anonymous user would be populated to scope["user"].
    """

    header_name = "Custom-Header-Name"
    keyword = "CustomKeyword"

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
