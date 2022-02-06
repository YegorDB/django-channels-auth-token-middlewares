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

    def get_token_key_string(self, scope):
        headers = dict(scope["headers"])
        return headers.get(self.header_name, b"").decode()

    @property
    def token_key_string_regex(self):
        return rf"{self.keyword} ({self.token_regex})"
