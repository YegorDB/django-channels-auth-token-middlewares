# Django REST framework middlewares tutorial

- [DRFAuthTokenMiddleware](#drfauthtokenmiddleware)
- [SimpleJWTAuthTokenMiddleware](#simplejwtauthtokenmiddleware)


### DRFAuthTokenMiddleware

#### Usage example

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

#### Override token keyword

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


### SimpleJWTAuthTokenMiddleware

#### Usage example

> SimpleJWTAuthTokenMiddleware could be used directly or behind other auth middlewares or middleware stacks.

Direct usage

```python
from channels.routing import ProtocolTypeRouter, URLRouter

from channels_auth_token_middlewares.middleware import SimpleJWTAuthTokenMiddleware


application = ProtocolTypeRouter({

    "websocket": SimpleJWTAuthTokenMiddleware(
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

from channels_auth_token_middlewares.middleware import SimpleJWTAuthTokenMiddleware


application = ProtocolTypeRouter({

    "websocket": AuthMiddlewareStack(SimpleJWTAuthTokenMiddleware(
        URLRouter([
            # app paths
        ]),
    )),

})
```
