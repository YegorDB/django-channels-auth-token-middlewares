# Base classes inheritance


## Intro

### Get user instance by request scope
> There are 3 stages to get user instance by request scope

#### Stages
1. Get token key string from the scope.
2. Parse token key from token key string.
3. Get user instance by token key.

#### Stages methods
1. "get_token_key_string(scope)" async method.
2. "parse_token_key(token_key_string)" method.
3. "get_user_instance(token_key)" async method.


## HeaderAuthTokenMiddleware inheritance

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

```python
class CustomHeaderAuthTokenMiddleware2(CustomHeaderAuthTokenMiddleware):
    """
    Header example
    Custom-Header-Name: CustomKeyword 7
    User with id 7 or anonymous user would be populated to scope["user"].

    In this case only ids from 1 to 9 would be handled.
    """

    # regex need to fullmatch token key, by defaul any string (".*")
    token_regex = "[1-9]"


class CustomHeaderAuthTokenMiddleware3(CustomHeaderAuthTokenMiddleware2):
    """
    Header example
    Custom-Header-Name: 2 CustomKeyword
    User with id 2 or anonymous user would be populated to scope["user"].
    """

    @property
    def token_key_string_regex(self):
        """
        Regex to parse token key from token key string.
        Token key need to be in first group.
        """

        return rf"({self.token_regex}) {self.keyword}"
```
