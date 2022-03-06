from django.test import TestCase

from test_app.consumer import MockConsumer
from test_app.middleware import (
    TestBaseAuthTokenMiddleware, TestHeaderAuthTokenMiddleware,
    TestCookieAuthTokenMiddleware, TestQueryStringAuthTokenMiddleware,
)


class MiddlewaresTests(TestCase):
    pass
