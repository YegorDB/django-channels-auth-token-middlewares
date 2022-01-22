import re

from urllib.parse import parse_qs

from django.apps import apps
from django.utils.functional import empty

from channels.auth import AuthMiddleware, UserLazyObject
from channels.db import database_sync_to_async


class BaseAuthTokenMiddleware(AuthMiddleware):
    """
    Base middleware which populates scope["user"] by authorization token key.
    Could be used behind other auth middlewares like AuthMiddleware.
    """

    token_regex = ".*"

    def __init__(self, *args, token_regex=None, **kwargs):
        self.token_regex = str(token_regex or self.token_regex)
        super().__init__(*args, **kwargs)

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

    def __init__(self, *args, header_name=None, keyword=None, **kwargs):
        self.header_name = str(header_name or self.header_name)
        self.header_name = self.header_name.lower().encode()

        self.keyword = str(keyword or self.keyword)

        super().__init__(*args, **kwargs)

    def parse_token_key(self, scope):
        headers = dict(scope["headers"])
        key = headers.get(self.header_name, b"").decode()

        matched = re.fullmatch(rf"{self.keyword} ({self.token_regex})", key)
        if not matched:
            return None
        return matched.group(1)


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


class QueryStringAuthTokenMiddleware(BaseAuthTokenMiddleware):
    """Base middleware which parses token key from request query string."""

    query_param = None

    def __init__(self, *args, query_param=None, **kwargs):
        self.query_param = str(query_param or self.query_param)

        super().__init__(*args, **kwargs)

    def parse_token_key(self, scope):
        raw_query_params = scope["query_string"].decode()
        query_params = parse_qs(raw_query_params)
        key = query_params.get(self.query_param, [""])[0]

        matched = re.fullmatch(rf"({self.token_regex})", key)
        if not matched:
            return None
        return matched.group(1)
