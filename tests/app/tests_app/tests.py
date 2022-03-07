from django.contrib.auth import get_user_model
from django.test import TestCase

from tests_app.consumer import MockConsumer
from tests_app.middleware import (
    TestBaseAuthTokenMiddleware, TestHeaderAuthTokenMiddleware,
    TestCookieAuthTokenMiddleware, TestQueryStringAuthTokenMiddleware,
)


class MiddlewaresTests(TestCase):

    @classmethod
    def setUpClass(cls):
        User = get_user_model()
        User.objects.create_user("test", password="test", id=1)

    @classmethod
    def tearDownClass(cls):
        pass

    async def test_base_auth_token_middleware(self):
        app = TestBaseAuthTokenMiddleware(MockConsumer())

        scope = {"headers": [(b"test", b"1")]}
        updated_scope = await app(scope, None, None)
        user = updated_scope.get("user")
        assert user
        assert not user.is_anonymous
        assert user.id == 1

        scope = {"headers": [(b"test", b"2")]}
        updated_scope = await app(scope, None, None)
        user = updated_scope.get("user")
        assert user
        assert user.is_anonymous

    async def test_header_auth_token_middleware(self):
        app = TestHeaderAuthTokenMiddleware(MockConsumer())

        scope = {"headers": [(b"test-authorization", b"Id 1")]}
        updated_scope = await app(scope, None, None)
        user = updated_scope.get("user")
        assert user
        assert not user.is_anonymous
        assert user.id == 1

        scope = {"headers": [(b"test-authorization", b"Id 2")]}
        updated_scope = await app(scope, None, None)
        user = updated_scope.get("user")
        assert user
        assert user.is_anonymous
