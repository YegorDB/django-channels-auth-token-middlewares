import re

from django.contrib.auth.models import AnonymousUser
from django.utils.functional import empty

from channels.auth import AuthMiddleware, UserLazyObject


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
        token_key_string = self.get_token_key_string(scope)
        token_key = self.parse_token_key(token_key_string)
        if not token_key:
            return AnonymousUser()

        user = await self.get_user_instance(token_key)
        return user or AnonymousUser()

    def get_token_key_string(self, scope):
        """
        Must be implemented by subclasses
        to get token key string from the scope.
        Implementation need to returns string to parse token key from.
        """
        raise NotImplementedError(
            "subclasses of BaseAuthTokenMiddleware "
            "must provide a get_token_key_string(scope) method")

    def parse_token_key(self, token_key_string):
        matched = re.fullmatch(self.token_key_string_regex, token_key_string)
        if not matched:
            return None
        return matched.group(1)

    @property
    def token_key_string_regex(self):
        return rf"({self.token_regex})"

    async def get_user_instance(self, token_key):
        """
        Must be implemented by subclasses to get user instance by token key.
        Implementation need to returns user instance or None.
        """
        raise NotImplementedError(
            "subclasses of BaseAuthTokenMiddleware "
            "must provide a get_user_instance(token_key) method")
