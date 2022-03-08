from django.contrib.auth import get_user_model
from django.test import TestCase

from rest_framework.authtoken.models import Token

from rest_framework_simplejwt.tokens import RefreshToken

from channels_auth_token_middlewares.middleware import (
    DRFAuthTokenMiddleware, SimpleJWTAuthTokenMiddleware,
)

from tests_app.consumer import MockConsumer
from tests_app.middleware import (
    TestBaseAuthTokenMiddleware, TestHeaderAuthTokenMiddleware,
    TestCookieAuthTokenMiddleware, TestQueryStringAuthTokenMiddleware,
)


class MiddlewaresTests(TestCase):

    @classmethod
    def setUpClass(cls):
        User = get_user_model()
        user = User.objects.create_user("test", password="test", id=1)

        token = Token.objects.create(user=user)
        cls._drf_token_key = token.key

        refresh = RefreshToken.for_user(user)
        cls._simplejwt_token_key = refresh.access_token

    @classmethod
    def tearDownClass(cls):
        pass

    async def test_base_auth_token_middleware(self):
        mdwr = TestBaseAuthTokenMiddleware(MockConsumer())
        success_scope = {"headers": [(b"test", b"1")]}
        fail_scope = {"headers": [(b"test", b"2")]}
        await self._test_middleware(mdwr, success_scope, fail_scope)

    async def test_header_auth_token_middleware(self):
        mdwr = TestHeaderAuthTokenMiddleware(MockConsumer())
        success_scope = {"headers": [(b"test-authorization", b"Id 1")]}
        fail_scope = {"headers": [(b"test-authorization", b"Id 2")]}
        await self._test_middleware(mdwr, success_scope, fail_scope)

    async def test_cookie_auth_token_middleware(self):
        mdwr = TestCookieAuthTokenMiddleware(MockConsumer())
        success_scope = {"headers": [(b"cookie", b"test=1")]}
        fail_scope = {"headers": [(b"cookie", b"test=2")]}
        await self._test_middleware(mdwr, success_scope, fail_scope)

    async def test_query_string_auth_token_middleware(self):
        mdwr = TestQueryStringAuthTokenMiddleware(MockConsumer())
        success_scope = {"query_string": b"test=1"}
        fail_scope = {"query_string": b"test=2"}
        await self._test_middleware(mdwr, success_scope, fail_scope)

    async def test_drf_auth_token_middleware(self):
        mdwr = DRFAuthTokenMiddleware(MockConsumer())
        success_scope = {"headers": [(b"authorization", f"Token {self._drf_token_key}".encode())]}
        fail_scope = {"headers": [(b"authorization", b"Token wrong_token_key")]}
        await self._test_middleware(mdwr, success_scope, fail_scope)

    async def test_simplejwt_auth_token_middleware(self):
        mdwr = SimpleJWTAuthTokenMiddleware(MockConsumer())
        success_scope = {"headers": [(b"authorization", f"Bearer {self._simplejwt_token_key}".encode())]}
        fail_scope = {"headers": [(b"authorization", b"Token wrong_token_key")]}
        await self._test_middleware(mdwr, success_scope, fail_scope)

    async def _test_middleware(self, mdwr, success_scope, fail_scope):
        updated_scope = await mdwr(success_scope, None, None)
        user = updated_scope.get("user")
        assert user
        assert not user.is_anonymous
        assert user.id == 1

        updated_scope = await mdwr(fail_scope, None, None)
        user = updated_scope.get("user")
        assert user
        assert user.is_anonymous
