import re

from django.apps import apps
from django.utils.functional import empty

from channels.auth import AuthMiddleware, UserLazyObject
from channels.db import database_sync_to_async


class BaseAuthTokenMiddleware(AuthMiddleware):
    """
    Base middleware which populates scope["user"] by authorization token key.
    Could be used behind other auth middlewares like AuthMiddleware.
    """

    def populate_scope(self, scope):
        # Add it to the scope if it is not there already
        if "user" not in scope:
            scope["user"] = UserLazyObject()

    async def resolve_scope(self, scope):
        # Get user instance if it is not already in the scope.
        if scope["user"]._wrapped is empty or scope["user"].is_anonymous:
            scope["user"]._wrapped = await self.get_user(scope)

    async def get_user(self, scope):
        # postpone model import to avoid ImproperlyConfigured error before
        # Django setup is complete.
        from django.contrib.auth.models import AnonymousUser

        token_key = self.parse_token_key(scope)
        if not token_key:
            return AnonymousUser()

        user = await self.get_user_instance(token_key)
        return user or AnonymousUser()

    def parse_token_key(self, scope):
        """
        Must be implemented by subclasses to parse token key from the scope.
        Implementation need to returns token key or None.
        """
        raise NotImplementedError(
            "subclasses of BaseAuthTokenMiddleware "
            "must provide a parse_token_key(scope) method")

    async def get_user_instance(self, token_key):
        """
        Must be implemented by subclasses to get user instance by token key.
        Implementation need to returns user instance or None.
        """
        raise NotImplementedError(
            "subclasses of BaseAuthTokenMiddleware "
            "must provide a get_user_instance(token_key) method")


class DRFAuthTokenMiddleware(BaseAuthTokenMiddleware):
    """Django REST framework auth token middleware."""

    keyword = "Token"
    token_regex = "[0-9a-f]{{40}}"

    def __init__(self, *args, keyword=None, token_regex=None, **kwargs):
        self.keyword = keyword or self.keyword
        self.token_regex = token_regex or self.token_regex
        super().__init__(*args, **kwargs)

    def parse_token_key(self, scope):
        headers = dict(scope["headers"])
        key = headers.get(b"authorization", b"").decode()
        matched = re.fullmatch(rf"{self.keyword} ({self.token_regex})", key)
        if not matched:
            return None
        return matched.group(1)

    @database_sync_to_async
    def get_user_instance(self, token_key):
        Token = apps.get_model("authtoken", "Token")
        try:
            token = Token.objects.select_related("user").get(key=token_key)
        except Token.DoesNotExist:
            return None
        return token.user
