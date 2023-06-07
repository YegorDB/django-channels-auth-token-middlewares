from channels_auth_token_middlewares.middleware import (
    DRFAuthTokenMiddleware, QueryStringDRFAuthTokenMiddleware,
    SimpleJWTAuthTokenMiddleware, QueryStringSimpleJWTAuthTokenMiddleware,
)

from tests_app.consumer import MockConsumer
from tests_app.middleware import (
    TestBaseAuthTokenMiddleware, TestHeaderAuthTokenMiddleware,
    TestCookieAuthTokenMiddleware, TestQueryStringAuthTokenMiddleware,
)

from .base import BaseMiddlewaresTests


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
