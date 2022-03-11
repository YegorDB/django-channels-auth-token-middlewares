# Django Channels auth token middlewares

> Provides Django REST framework [token authentication](https://www.django-rest-framework.org/api-guide/authentication/#tokenauthentication) middleware, [Simple JWT](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/index.html) middleware and easily extendable middlewares to work with auth tokens placed in request headers, cookie and query string.


## Requirements
- Python>=3.6
- Channels>=3


## Install
`$ pip install channels_auth_token_middlewares`


## Tutorial
[Explore](tutorial)


## Docs
[Explore](docs)


## Tests

### Requirements
- Docker>=19
- docker-compose>=1.25

### Usage

#### Run
`$ docker-compose -f docker-compose.tests.yml up`

#### Clean
`$ docker-compose -f docker-compose.tests.yml down`
