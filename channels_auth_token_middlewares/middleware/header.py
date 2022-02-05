import re

from .base import BaseAuthTokenMiddleware


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
