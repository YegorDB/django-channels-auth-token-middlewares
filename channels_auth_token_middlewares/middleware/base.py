# Copyright 2022 Yegor Bitensky

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import re

from http.cookies import BaseCookie
from urllib.parse import parse_qs

from django.contrib.auth.models import AnonymousUser
from django.utils.functional import empty

from channels.auth import AuthMiddleware, UserLazyObject


class BaseAuthTokenMiddleware(AuthMiddleware):
    """
    Base middleware which populates scope["user"] by authorization token key.
    Could be used behind other auth middlewares like AuthMiddleware.
    """

    # regex need to fullmatch token key
    token_regex = r".*"

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
        if not token_key_string:
            return AnonymousUser()

        token_key = self.parse_token_key(token_key_string)
        if not token_key:
            return AnonymousUser()

        user = await self.get_user_instance(token_key)
        return user or AnonymousUser()

    def get_token_key_string(self, scope):
        """
        Must be implemented by subclass
        to get token key string from the scope.
        Implementation need to returns string to parse token key from or None.
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
        """
        Regex to parse token key from token key string.
        Token key need to be in first group.
        """

        return rf"({self.token_regex})"

    async def get_user_instance(self, token_key):
        """
        Must be implemented by subclass to get user instance by token key.
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

    def get_token_key_string(self, scope):
        headers = dict(scope["headers"])
        value = headers.get(self.header_name)
        if not value:
            return None
        return value.decode()

    @property
    def token_key_string_regex(self):
        """
        Regex to parse token key from token key string.
        Token key need to be in first group.
        """

        return rf"{self.keyword} ({self.token_regex})"


class CookieAuthTokenMiddleware(BaseAuthTokenMiddleware):
    """Base middleware which parses token key from request cookie."""

    cookie_name = None

    def __init__(self, *args, cookie_name=None, **kwargs):
        self.cookie_name = str(cookie_name or self.cookie_name)

        super().__init__(*args, **kwargs)

    def get_token_key_string(self, scope):
        headers = dict(scope["headers"])
        cookie_raw_data = headers.get(b"cookie", b"").decode()
        cookie = BaseCookie()
        cookie.load(cookie_raw_data)
        cookie_item = cookie.get(self.cookie_name)
        if not cookie_item:
            return None
        return cookie_item.value


class QueryStringAuthTokenMiddleware(BaseAuthTokenMiddleware):
    """Base middleware which parses token key from request query string."""

    query_param = None

    def __init__(self, *args, query_param=None, **kwargs):
        self.query_param = str(query_param or self.query_param)

        super().__init__(*args, **kwargs)

    def get_token_key_string(self, scope):
        raw_query_params = scope["query_string"].decode()
        query_params = parse_qs(raw_query_params)
        query_param = query_params.get(self.query_param)
        if not query_param:
            return None
        return query_param[0]
