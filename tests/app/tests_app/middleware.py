from django.contrib.auth import get_user_model

from channels.db import database_sync_to_async

from channels_auth_token_middlewares.middleware import BaseAuthTokenMiddleware


class TestBaseAuthTokenMiddleware(BaseAuthTokenMiddleware):

    def get_token_key_string(self, scope):
        headers = dict(scope["headers"])
        value = headers.get(b"test")
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
