# Copyright 2022 Yegor Bitensky

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""
Django REST framework middlewares.
"""


from django.apps import apps

from channels.db import database_sync_to_async

from .base import HeaderAuthTokenMiddleware, QueryStringAuthTokenMiddleware


class DRFAuthTokenMiddlewareMixin:
    """Django REST framework auth token middleware mixin."""

    @database_sync_to_async
    def get_drf_user_instance(self, token_key):
        Token = apps.get_model("authtoken", "Token")
        try:
            token = Token.objects.select_related("user").get(key=token_key)
        except Token.DoesNotExist:
            return None
        return token.user


class DRFAuthTokenMiddleware(
    HeaderAuthTokenMiddleware,
    DRFAuthTokenMiddlewareMixin,
):
    """
    Django REST framework auth token middleware.

    https://www.django-rest-framework.org/api-guide/authentication/#tokenauthentication
    """

    header_name = "Authorization"
    keyword = "Token"
    token_regex = "[0-9a-f]{40}"

    async def get_user_instance(self, token_key):
        return await self.get_drf_user_instance(token_key)


class QueryStringDRFAuthTokenMiddleware(
    QueryStringAuthTokenMiddleware,
    DRFAuthTokenMiddlewareMixin,
):
    """Django REST framework auth token middleware with query string token."""

    query_param = "token"

    async def get_user_instance(self, token_key):
        return await self.get_drf_user_instance(token_key)


def DRFAuthTokenMiddlewareStack(inner):
    return DRFAuthTokenMiddleware(QueryStringDRFAuthTokenMiddleware(inner))


class SimpleJWTAuthTokenMiddlewareMixin:
    """Simple JWT auth token middleware mixin."""

    _auth = None
    _exceptions = None

    def _setup(self):
        from rest_framework_simplejwt.authentication import JWTAuthentication
        from rest_framework_simplejwt.exceptions import (
            AuthenticationFailed, InvalidToken, TokenError
        )

        self._auth = JWTAuthentication()
        self._exceptions = (AuthenticationFailed, InvalidToken, TokenError)

    @database_sync_to_async
    def get_jwt_user_instance(self, token_key):
        if self._auth is None or self._exceptions is None:
            raise RuntimeError("_setup method has to be called before.")

        try:
            validated_token = self._auth.get_validated_token(token_key)
            return self._auth.get_user(validated_token)
        except self._exceptions:
            return None


class SimpleJWTAuthTokenMiddleware(
    HeaderAuthTokenMiddleware,
    SimpleJWTAuthTokenMiddlewareMixin,
):
    """
    Simple JWT auth token middleware.

    https://django-rest-framework-simplejwt.readthedocs.io/en/latest/index.html
    """

    header_name = "Authorization"
    keyword = "Bearer"

    def __init__(self, *args, **kwargs):
        self._setup()
        return super().__init__(*args, **kwargs)

    async def get_user_instance(self, token_key):
        return await self.get_jwt_user_instance(token_key)


class QueryStringSimpleJWTAuthTokenMiddleware(
    QueryStringAuthTokenMiddleware,
    SimpleJWTAuthTokenMiddlewareMixin,
):
    """Simple JWT auth token middleware with query string token."""

    query_param = "token"

    def __init__(self, *args, **kwargs):
        self._setup()
        return super().__init__(*args, **kwargs)

    async def get_user_instance(self, token_key):
        return await self.get_jwt_user_instance(token_key)


def SimpleJWTAuthTokenMiddlewareStack(inner):
    return SimpleJWTAuthTokenMiddleware(
        QueryStringSimpleJWTAuthTokenMiddleware(inner))
