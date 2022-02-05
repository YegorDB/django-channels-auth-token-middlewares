from channels.db import database_sync_to_async

from .header import HeaderAuthTokenMiddleware


class JWTAuthTokenMiddleware(HeaderAuthTokenMiddleware):
    """
    Simple JWT auth token middleware.

    https://django-rest-framework-simplejwt.readthedocs.io/en/latest/index.html
    """

    header_name = "Authorization"
    keyword = "Bearer"

    @database_sync_to_async
    def get_user_instance(self, token_key):
        from rest_framework_simplejwt.authentication import JWTAuthentication
        from rest_framework_simplejwt.exceptions import (
            AuthenticationFailed, InvalidToken, TokenError
        )

        auth = JWTAuthentication()
        try:
            validated_token = auth.get_validated_token(token_key)
            return auth.get_user(validated_token)
        except (AuthenticationFailed, InvalidToken, TokenError):
            return None
