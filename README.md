# Django Channels auth token middlewares

> Provides Django REST framework [token authentication](https://www.django-rest-framework.org/api-guide/authentication/#tokenauthentication) middleware, [Simple JWT](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/index.html) middleware and easily extendable middlewares to work with auth tokens placed in request headers, cookie and query string.


## Requirements
- Channels>=4.1


## Install
1. `$ pip install channels-auth-token-middlewares`
2. Add app name to `INSTALLED_APPS`
```python
INSTALLED_APPS = [
    # base django apps (django.contrib.auth is required)
    # other apps this one depends on (like rest_framework if it's necessary)
    'channels_auth_token_middlewares',
    # custom apps
]
```

## Tutorial
[Explore](tutorial)


## Docs
[Explore](docs)


## Tests

### Requirements
- Docker>=19

### Usage

#### Run
`$ docker compose -f docker-compose.tests.yml up`

#### Clean
`$ docker compose -f docker-compose.tests.yml down`
