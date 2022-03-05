from django.test import TestCase

from channels.testing import ApplicationCommunicator

from test_app.consumer import TestHttpConsumer
from test_app.middleware import (
    TestBaseAuthTokenMiddleware, TestHeaderAuthTokenMiddleware,
    TestCookieAuthTokenMiddleware, TestQueryStringAuthTokenMiddleware,
)


class MiddlewaresTests(TestCase):
    pass
