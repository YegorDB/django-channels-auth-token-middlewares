from django.contrib.auth import get_user_model

from channels_auth_token_middlewares.middleware import (
    BaseAuthTokenMiddleware, HeaderAuthTokenMiddleware,
    CookieAuthTokenMiddleware, QueryStringAuthTokenMiddleware,
)


class UserGetterByIdMixin:

    async def get_user_by_id(self, user_id):
        User = get_user_model()
        try:
            return await User.objects.aget(id=user_id)
        except User.DoesNotExist:
            return None


class TestBaseAuthTokenMiddleware(BaseAuthTokenMiddleware, UserGetterByIdMixin):

    def get_token_key_string(self, scope):
        headers = dict(scope["headers"])
        value = headers.get(b"test")
        if not value:
            return None
        return value.decode()

    async def get_user_instance(self, token_key):
        return await self.get_user_by_id(token_key)


class TestHeaderAuthTokenMiddleware(HeaderAuthTokenMiddleware, UserGetterByIdMixin):

    header_name = "Test-Authorization"
    keyword = "Id"

    async def get_user_instance(self, token_key):
        return await self.get_user_by_id(token_key)


class TestCookieAuthTokenMiddleware(CookieAuthTokenMiddleware, UserGetterByIdMixin):

    cookie_name = "test"

    async def get_user_instance(self, token_key):
        return await self.get_user_by_id(token_key)


class TestQueryStringAuthTokenMiddleware(QueryStringAuthTokenMiddleware, UserGetterByIdMixin):

    query_param = "test"

    async def get_user_instance(self, token_key):
        return await self.get_user_by_id(token_key)
