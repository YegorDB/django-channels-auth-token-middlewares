from channels.testing import HttpCommunicator

from channels_auth_token_middlewares.middleware import (
    DRFAuthTokenMiddleware, QueryStringDRFAuthTokenMiddleware,
    SimpleJWTAuthTokenMiddleware, QueryStringSimpleJWTAuthTokenMiddleware,
)

from tests_app.consumer import TestHttpConsumer
from tests_app.middleware import (
    TestBaseAuthTokenMiddleware, TestHeaderAuthTokenMiddleware,
    TestCookieAuthTokenMiddleware, TestQueryStringAuthTokenMiddleware,
)

from .base import BaseMiddlewaresTests


class HttpCommunicatorMiddlewaresTests(BaseMiddlewaresTests):

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
