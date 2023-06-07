from channels.testing import WebsocketCommunicator

from channels_auth_token_middlewares.middleware import (
    DRFAuthTokenMiddleware, QueryStringDRFAuthTokenMiddleware,
    SimpleJWTAuthTokenMiddleware, QueryStringSimpleJWTAuthTokenMiddleware,
)

from tests_app.consumer import TestWebsocketConsumer
from tests_app.middleware import (
    TestBaseAuthTokenMiddleware, TestHeaderAuthTokenMiddleware,
    TestCookieAuthTokenMiddleware, TestQueryStringAuthTokenMiddleware,
)

from .base import BaseMiddlewaresTests


class WebsocketCommunicatorMiddlewaresTests(BaseMiddlewaresTests):

    async def test_base_auth_token_middleware(self):
        mdwr = TestBaseAuthTokenMiddleware(TestWebsocketConsumer())
        await self._test_middleware_success(mdwr, headers=[
            (b"test", b"1")
        ])
        await self._test_middleware_fail(mdwr, headers=[
            (b"test", b"2")
        ])

    async def test_header_auth_token_middleware(self):
        mdwr = TestHeaderAuthTokenMiddleware(TestWebsocketConsumer())
        await self._test_middleware_success(mdwr, headers=[
            (b"test-authorization", b"Id 1")
        ])
        await self._test_middleware_fail(mdwr, headers=[
            (b"test-authorization", b"Id 0")
        ])

    async def test_not_lower_header_auth_token_middleware(self):
        mdwr = TestHeaderAuthTokenMiddleware(TestWebsocketConsumer())
        await self._test_middleware_success(mdwr, headers=[
            (b"Test-Authorization", b"Id 1")
        ])
        await self._test_middleware_fail(mdwr, headers=[
            (b"Test-Authorization", b"Id 0")
        ])

    async def test_cookie_auth_token_middleware(self):
        mdwr = TestCookieAuthTokenMiddleware(TestWebsocketConsumer())
        await self._test_middleware_success(mdwr, headers=[
            (b"cookie", b"test=1")
        ])
        await self._test_middleware_fail(mdwr, headers=[
            (b"cookie", b"test=2")
        ])

    async def test_query_string_auth_token_middleware(self):
        mdwr = TestQueryStringAuthTokenMiddleware(TestWebsocketConsumer())
        await self._test_middleware_success(mdwr, path="/test/?test=1")
        await self._test_middleware_fail(mdwr,path="/test/?test=2")

    async def test_drf_auth_token_middleware(self):
        mdwr = DRFAuthTokenMiddleware(TestWebsocketConsumer())
        await self._test_middleware_success(mdwr, headers=[
            (b"authorization", f"Token {self._drf_token_key}".encode())
        ])
        await self._test_middleware_fail(mdwr, headers=[
            (b"authorization", b"Token wrong_token_key")
        ])

    async def test_query_string_drf_auth_token_middleware(self):
        mdwr = QueryStringDRFAuthTokenMiddleware(TestWebsocketConsumer())
        await self._test_middleware_success(
            mdwr,
            path=f"/test/?token={self._drf_token_key}"
        )
        await self._test_middleware_fail(
            mdwr,
            path="/test/?token=wrong_token_key"
        )

    async def test_simplejwt_auth_token_middleware(self):
        mdwr = SimpleJWTAuthTokenMiddleware(TestWebsocketConsumer())
        await self._test_middleware_success(mdwr, headers=[
            (b"authorization", f"Bearer {self._simplejwt_token_key}".encode())
        ])
        await self._test_middleware_fail(mdwr, headers=[
            (b"authorization", b"Token wrong_token_key")
        ])

    async def test_query_string_simplejwt_auth_token_middleware(self):
        mdwr = QueryStringSimpleJWTAuthTokenMiddleware(TestWebsocketConsumer())
        await self._test_middleware_success(
            mdwr,
            path=f"/test/?token={self._simplejwt_token_key}"
        )
        await self._test_middleware_fail(
            mdwr,
            path="/test/?token=wrong_token_key"
        )

    async def _test_middleware_success(self, mdwr, path=None, headers=None):
        path = path or "/test/"
        headers = headers or []

        communicator = WebsocketCommunicator(mdwr, path, headers=headers)
        connected, _ = await communicator.connect()
        assert connected

        await communicator.disconnect()

    async def _test_middleware_fail(self, mdwr, path=None, headers=None):
        path = path or "/test/"
        headers = headers or []

        communicator = WebsocketCommunicator(mdwr, path, headers=headers)
        connected, error_code = await communicator.connect()
        assert not connected
        assert error_code == 401

        await communicator.disconnect()
