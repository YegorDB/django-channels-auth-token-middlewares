# Django REST framework middlewares tutorial

- [DRFAuthTokenMiddleware](#drfauthtokenmiddleware)
- [QueryStringDRFAuthTokenMiddleware](#querystringdrfauthtokenmiddleware)
- [DRFAuthTokenMiddlewareStack](#drfauthtokenmiddlewarestack)
- [SimpleJWTAuthTokenMiddleware](#simplejwtauthtokenmiddleware)
- [QueryStringSimpleJWTAuthTokenMiddleware](#queryStringsimplejwtauthtokenmiddleware)
- [SimpleJWTAuthTokenMiddlewareStack](#simplejwtauthtokenmiddlewarestack)


## DRFAuthTokenMiddleware

> Django REST framework [token authentication](https://www.django-rest-framework.org/api-guide/authentication/#tokenauthentication) middleware

### Usage example

> DRFAuthTokenMiddleware could be used directly or behind other auth middlewares or middleware stacks.

Direct usage

```python
from channels.routing import ProtocolTypeRouter, URLRouter

from channels_auth_token_middlewares.middleware import DRFAuthTokenMiddleware


application = ProtocolTypeRouter({

    "websocket": DRFAuthTokenMiddleware(
        URLRouter([
            # app paths
        ]),
    ),

})
```

With AuthMiddlewareStack

```python
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

from channels_auth_token_middlewares.middleware import DRFAuthTokenMiddleware


application = ProtocolTypeRouter({

    "websocket": AuthMiddlewareStack(DRFAuthTokenMiddleware(
        URLRouter([
            # app paths
        ]),
    )),

})
```

### Override token keyword

Override by init argument

```python
from channels.routing import ProtocolTypeRouter, URLRouter

from channels_auth_token_middlewares.middleware import DRFAuthTokenMiddleware


application = ProtocolTypeRouter({

    "websocket": DRFAuthTokenMiddleware(
        URLRouter([
            # app paths
        ]),
        keyword="CustomKeyword",
    ),

})

# Header example
# Authorization: CustomKeyword 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
```

Override by subclass

```python
from channels.routing import ProtocolTypeRouter, URLRouter

from channels_auth_token_middlewares.middleware import DRFAuthTokenMiddleware


class CustomDRFAuthTokenMiddleware(DRFAuthTokenMiddleware):
    keyword = "CustomKeyword"


application = ProtocolTypeRouter({

    "websocket": CustomDRFAuthTokenMiddleware(
        URLRouter([
            # app paths
        ]),
    ),

})
```


## QueryStringDRFAuthTokenMiddleware

> Django REST framework auth token middleware with query string token

### Usage example

> Like DRFAuthTokenMiddleware QueryStringDRFAuthTokenMiddleware could be used directly or behind other auth middlewares or middleware stacks.


## DRFAuthTokenMiddlewareStack

> Combines DRFAuthTokenMiddleware and QueryStringDRFAuthTokenMiddleware

### Usage example

```python
from channels.routing import ProtocolTypeRouter, URLRouter

from channels_auth_token_middlewares.middleware import DRFAuthTokenMiddlewareStack


application = ProtocolTypeRouter({

    "websocket": DRFAuthTokenMiddlewareStack(
        URLRouter([
            # app paths
        ]),
    ),

})
```

Same example without stack

```python
from channels.routing import ProtocolTypeRouter, URLRouter

from channels_auth_token_middlewares.middleware import DRFAuthTokenMiddleware, QueryStringDRFAuthTokenMiddleware


application = ProtocolTypeRouter({

    "websocket": DRFAuthTokenMiddleware(QueryStringDRFAuthTokenMiddleware(
        URLRouter([
            # app paths
        ]),
    )),

})
```


## SimpleJWTAuthTokenMiddleware

> [Simple JWT](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/index.html) middleware

### Usage example

> Like DRFAuthTokenMiddleware SimpleJWTAuthTokenMiddleware could be used directly or behind other auth middlewares or middleware stacks.


## QueryStringSimpleJWTAuthTokenMiddleware

> Simple JWT auth token middleware with query string token

### Usage example

> Like DRFAuthTokenMiddleware QueryStringSimpleJWTAuthTokenMiddleware could be used directly or behind other auth middlewares or middleware stacks.


## SimpleJWTAuthTokenMiddlewareStack

> Like DRFAuthTokenMiddlewareStack but combines SimpleJWTAuthTokenMiddleware and QueryStringSimpleJWTAuthTokenMiddleware
