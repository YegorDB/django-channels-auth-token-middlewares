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
