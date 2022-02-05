import re

from urllib.parse import parse_qs

from .base import BaseAuthTokenMiddleware


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
