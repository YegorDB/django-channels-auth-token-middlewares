from django.contrib.auth import get_user_model

from channels.db import database_sync_to_async

from channels_auth_token_middlewares.middleware import (
    BaseAuthTokenMiddleware, HeaderAuthTokenMiddleware,
    CookieAuthTokenMiddleware,
)


class UserGetterByIdMixin:

    def get_user_by_id(self, user_id):
        User = get_user_model()
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None


class TestBaseAuthTokenMiddleware(BaseAuthTokenMiddleware, UserGetterByIdMixin):

    def get_token_key_string(self, scope):
        headers = dict(scope["headers"])
        value = headers.get(b"test")
        if not value:
            return None
        return value.decode()

    @database_sync_to_async
    def get_user_instance(self, token_key):
        return self.get_user_by_id(token_key)


class TestHeaderAuthTokenMiddleware(HeaderAuthTokenMiddleware, UserGetterByIdMixin):

    header_name = "Test-Authorization"
    keyword = "Id"

    @database_sync_to_async
    def get_user_instance(self, token_key):
        return self.get_user_by_id(token_key)


class TestCookieAuthTokenMiddleware(CookieAuthTokenMiddleware, UserGetterByIdMixin):

    cookie_name = "test"

    @database_sync_to_async
    def get_user_instance(self, token_key):
        return self.get_user_by_id(token_key)
