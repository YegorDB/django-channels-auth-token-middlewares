from django.contrib.auth import get_user_model
from django.test import TestCase

from channels.testing import HttpCommunicator

from rest_framework.authtoken.models import Token

from rest_framework_simplejwt.tokens import RefreshToken

from channels_auth_token_middlewares.middleware import (
    DRFAuthTokenMiddleware, QueryStringDRFAuthTokenMiddleware,
    SimpleJWTAuthTokenMiddleware, QueryStringSimpleJWTAuthTokenMiddleware,
)

from tests_app.consumer import MockConsumer, TestHttpConsumer
from tests_app.middleware import (
    TestBaseAuthTokenMiddleware, TestHeaderAuthTokenMiddleware,
    TestCookieAuthTokenMiddleware, TestQueryStringAuthTokenMiddleware,
)


class BaseMiddlewaresTests(TestCase):

    @classmethod
    def setUpClass(cls):
        User = get_user_model()

        try:
            user = User.objects.get(id=1)
        except User.DoesNotExist:
            user = User.objects.create_user("test", password="test", id=1)

        token, _ = Token.objects.get_or_create(user=user)
        cls._drf_token_key = token.key

        refresh = RefreshToken.for_user(user)
        cls._simplejwt_token_key = refresh.access_token

    @classmethod
    def tearDownClass(cls):
        pass


class DirectMiddlewaresTests(BaseMiddlewaresTests):

    async def test_base_auth_token_middleware(self):
        mdwr = TestBaseAuthTokenMiddleware(MockConsumer())
        await self._test_middleware_success(mdwr, {"headers": [
            (b"test", b"1")
        ]})
        await self._test_middleware_fail(mdwr, {"headers": [
            (b"test", b"2")
        ]})

    async def test_header_auth_token_middleware(self):
        mdwr = TestHeaderAuthTokenMiddleware(MockConsumer())
        await self._test_middleware_success(mdwr, {"headers": [
            (b"test-authorization", b"Id 1")
        ]})
        await self._test_middleware_fail(mdwr, {"headers": [
            (b"test-authorization", b"Id 2")
        ]})

    async def test_not_lower_header_auth_token_middleware(self):
        mdwr = TestHeaderAuthTokenMiddleware(MockConsumer())
        await self._test_middleware_success(mdwr, {"headers": [
            (b"Test-Authorization", b"Id 1")
        ]})
        await self._test_middleware_fail(mdwr, {"headers": [
            (b"Test-Authorization", b"Id 2")
        ]})

    async def test_cookie_auth_token_middleware(self):
        mdwr = TestCookieAuthTokenMiddleware(MockConsumer())
        await self._test_middleware_success(mdwr, {"headers": [
            (b"cookie", b"test=1")
        ]})
        await self._test_middleware_fail(mdwr, {"headers": [
            (b"cookie", b"test=2")
        ]})

    async def test_query_string_auth_token_middleware(self):
        mdwr = TestQueryStringAuthTokenMiddleware(MockConsumer())
        await self._test_middleware_success(mdwr, {"query_string": b"test=1"})
        await self._test_middleware_fail(mdwr, {"query_string": b"test=2"})

    async def test_drf_auth_token_middleware(self):
        mdwr = DRFAuthTokenMiddleware(MockConsumer())
        await self._test_middleware_success(mdwr, {"headers": [
            (b"authorization", f"Token {self._drf_token_key}".encode())
        ]})
        await self._test_middleware_fail(mdwr, {"headers": [
            (b"authorization", b"Token wrong_token_key")
        ]})

    async def test_query_string_drf_auth_token_middleware(self):
        mdwr = QueryStringDRFAuthTokenMiddleware(MockConsumer())
        await self._test_middleware_success(mdwr, {
            "query_string": f"authorization={self._drf_token_key}".encode()
        })
        await self._test_middleware_fail(mdwr, {
            "query_string": b"authorization=wrong_token_key"
        })

    async def test_simplejwt_auth_token_middleware(self):
        mdwr = SimpleJWTAuthTokenMiddleware(MockConsumer())
        await self._test_middleware_success(mdwr, {"headers": [
            (b"authorization", f"Bearer {self._simplejwt_token_key}".encode())
        ]})
        await self._test_middleware_fail(mdwr, {"headers": [
            (b"authorization", b"Token wrong_token_key")
        ]})

    async def test_query_string_simplejwt_auth_token_middleware(self):
        mdwr = QueryStringSimpleJWTAuthTokenMiddleware(MockConsumer())
        await self._test_middleware_success(mdwr, {
            "query_string": f"authorization={self._simplejwt_token_key}".encode()
        })
        await self._test_middleware_fail(mdwr, {
            "query_string": b"authorization=wrong_token_key"
        })

    async def _test_middleware_success(self, mdwr, scope):
        updated_scope = await mdwr(scope, None, None)
        user = updated_scope.get("user")
        assert user
        assert not user.is_anonymous
        assert user.id == 1

    async def _test_middleware_fail(self, mdwr, scope):
        updated_scope = await mdwr(scope, None, None)
        user = updated_scope.get("user")
        assert user
        assert user.is_anonymous


class CommunicatorMiddlewaresTests(BaseMiddlewaresTests):

    async def test_base_auth_token_middleware(self):
        mdwr = TestBaseAuthTokenMiddleware(TestHttpConsumer())
        await self._test_middleware_success(mdwr, headers=[
            (b"test", b"1")
        ])
        await self._test_middleware_fail(mdwr, headers=[
            (b"test", b"2")
        ])

    async def test_header_auth_token_middleware(self):
        mdwr = TestHeaderAuthTokenMiddleware(TestHttpConsumer())
        await self._test_middleware_success(mdwr, headers=[
            (b"test-authorization", b"Id 1")
        ])
        await self._test_middleware_fail(mdwr, headers=[
            (b"test-authorization", b"Id 0")
        ])

    async def test_not_lower_header_auth_token_middleware(self):
        mdwr = TestHeaderAuthTokenMiddleware(TestHttpConsumer())
        await self._test_middleware_success(mdwr, headers=[
            (b"Test-Authorization", b"Id 1")
        ])
        await self._test_middleware_fail(mdwr, headers=[
            (b"Test-Authorization", b"Id 0")
        ])

    async def test_cookie_auth_token_middleware(self):
        mdwr = TestCookieAuthTokenMiddleware(TestHttpConsumer())
        await self._test_middleware_success(mdwr, headers=[
            (b"cookie", b"test=1")
        ])
        await self._test_middleware_fail(mdwr, headers=[
            (b"cookie", b"test=2")
        ])

    async def test_query_string_auth_token_middleware(self):
        mdwr = TestQueryStringAuthTokenMiddleware(TestHttpConsumer())
        await self._test_middleware_success(mdwr, path="/test/?test=1")
        await self._test_middleware_fail(mdwr,path="/test/?test=2")

    async def test_drf_auth_token_middleware(self):
        mdwr = DRFAuthTokenMiddleware(TestHttpConsumer())
        await self._test_middleware_success(mdwr, headers=[
            (b"authorization", f"Token {self._drf_token_key}".encode())
        ])
        await self._test_middleware_fail(mdwr, headers=[
            (b"authorization", b"Token wrong_token_key")
        ])

    async def test_query_string_drf_auth_token_middleware(self):
        mdwr = QueryStringDRFAuthTokenMiddleware(TestHttpConsumer())
        await self._test_middleware_success(
            mdwr,
            path=f"/test/?authorization={self._drf_token_key}"
        )
        await self._test_middleware_fail(
            mdwr,
            path="/test/?authorization=wrong_token_key"
        )

    async def test_simplejwt_auth_token_middleware(self):
        mdwr = SimpleJWTAuthTokenMiddleware(TestHttpConsumer())
        await self._test_middleware_success(mdwr, headers=[
            (b"authorization", f"Bearer {self._simplejwt_token_key}".encode())
        ])
        await self._test_middleware_fail(mdwr, headers=[
            (b"authorization", b"Token wrong_token_key")
        ])

    async def test_query_string_simplejwt_auth_token_middleware(self):
        mdwr = QueryStringSimpleJWTAuthTokenMiddleware(TestHttpConsumer())
        await self._test_middleware_success(
            mdwr,
            path=f"/test/?authorization={self._simplejwt_token_key}"
        )
        await self._test_middleware_fail(
            mdwr,
            path="/test/?authorization=wrong_token_key"
        )

    async def _test_middleware_success(self, mdwr, path=None, headers=None):
        expected_body = b"1"
        await self._test_middleware_base(mdwr, expected_body, path, headers)

    async def _test_middleware_fail(self, mdwr, path=None, headers=None):
        expected_body = b"None"
        await self._test_middleware_base(mdwr, expected_body, path, headers)

    async def _test_middleware_base(self, mdwr, expected_body, path, headers):
        path = path or "/test/"
        headers = headers or []
        communicator = HttpCommunicator(mdwr, "GET", path, headers=headers)
        response = await communicator.get_response()
        assert response["status"] == 200
        assert response["body"] == expected_body
