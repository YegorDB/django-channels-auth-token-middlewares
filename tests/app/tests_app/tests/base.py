from django.contrib.auth import get_user_model
from django.test import TestCase

from rest_framework.authtoken.models import Token

from rest_framework_simplejwt.tokens import RefreshToken


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
