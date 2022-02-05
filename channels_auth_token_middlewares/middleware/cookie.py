import re

from http.cookies import BaseCookie

from .base import BaseAuthTokenMiddleware


class CookieAuthTokenMiddleware(BaseAuthTokenMiddleware):
    """Base middleware which parses token key from request cookie."""

    cookie_name = None

    def __init__(self, *args, cookie_name=None, **kwargs):
        self.cookie_name = str(cookie_name or self.cookie_name)

        super().__init__(*args, **kwargs)

    def parse_token_key(self, scope):
        headers = dict(scope["headers"])
        cookie_raw_data = headers.get(b"cookie", b"").decode()
        cookie = BaseCookie()
        cookie.load(cookie_raw_data)
        key = cookie.get(self.cookie_name, '')

        matched = re.fullmatch(rf"({self.token_regex})", key)
        if not matched:
            return None
        return matched.group(1)
