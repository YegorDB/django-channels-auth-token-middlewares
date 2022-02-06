"""
Django REST framework middlewares.
"""


from django.apps import apps

from channels.db import database_sync_to_async

from .header import HeaderAuthTokenMiddleware


class DRFAuthTokenMiddleware(HeaderAuthTokenMiddleware):
    """
    Django REST framework auth token middleware.

    https://www.django-rest-framework.org/api-guide/authentication/#tokenauthentication
    """

    header_name = "Authorization"
    keyword = "Token"
    token_regex = "[0-9a-f]{40}"

    @database_sync_to_async
    def get_user_instance(self, token_key):
        Token = apps.get_model("authtoken", "Token")
        try:
            token = Token.objects.select_related("user").get(key=token_key)
        except Token.DoesNotExist:
            return None
        return token.user


class SimpleJWTAuthTokenMiddleware(HeaderAuthTokenMiddleware):
    """
    Simple JWT auth token middleware.

    https://django-rest-framework-simplejwt.readthedocs.io/en/latest/index.html
    """

    header_name = "Authorization"
    keyword = "Bearer"

    def __init__(self, *args, **kwargs):
        from rest_framework_simplejwt.authentication import JWTAuthentication
        from rest_framework_simplejwt.exceptions import (
            AuthenticationFailed, InvalidToken, TokenError
        )

        self._auth = JWTAuthentication()
        self._exceptions = (AuthenticationFailed, InvalidToken, TokenError)

        return super().__init__(*args, **kwargs)

    @database_sync_to_async
    def get_user_instance(self, token_key):
        try:
            validated_token = self._auth.get_validated_token(token_key)
            return self._auth.get_user(validated_token)
        except self._exceptions:
            return None
