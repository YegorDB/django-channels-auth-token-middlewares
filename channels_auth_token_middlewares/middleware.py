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


class HeaderAuthTokenMiddleware(BaseAuthTokenMiddleware):
    """Base middleware which parses token key from request header."""

    header_name = None
    keyword = None
    token_regex = ".*"

    def __init__(
            self, *args, header_name=None,
            keyword=None, token_regex=None, **kwargs):

        self.header_name = header_name or self.header_name
        self.keyword = keyword or self.keyword
        self.token_regex = token_regex or self.token_regex

        self._validate_attributes()

        self.header_name = self.header_name.lower().encode()

        super().__init__(*args, **kwargs)

    def parse_token_key(self, scope):
        headers = dict(scope["headers"])
        key = headers.get(self.header_name, b"").decode()
        matched = re.fullmatch(rf"{self.keyword} ({self.token_regex})", key)
        if not matched:
            return None
        return matched.group(1)

    def _validate_attributes(self):
        if not self.header_name:
            raise NotImplementedError(
                "subclasses of HeaderAuthTokenMiddleware "
                "must provide a header_name attribute")
        if not isinstance(self.header_name, str):
            raise TypeError("header_name attribute has to be a string")

        if not self.keyword:
            raise NotImplementedError(
                "subclasses of HeaderAuthTokenMiddleware "
                "must provide a keyword attribute")
        if not isinstance(self.header_name, str):
            raise TypeError("keyword attribute has to be a string")

        if not isinstance(self.token_regex, str):
            raise TypeError("token_regex attribute has to be a string")


class DRFAuthTokenMiddleware(HeaderAuthTokenMiddleware):
    """Django REST framework auth token middleware."""

    header_name = "Authorization"
    keyword = "Token"
    token_regex = "[0-9a-f]{40}"

    @database_sync_to_async
    def get_user_instance(self, token_key):
        Token = apps.get_model("authtoken", "Token")
        try:
            token = Token.objects.select_related("user").get(key=token_key)
        except Token.DoesNotExist:
            return None
        return token.user
