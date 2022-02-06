from urllib.parse import parse_qs

from .base import BaseAuthTokenMiddleware


class QueryStringAuthTokenMiddleware(BaseAuthTokenMiddleware):
    """Base middleware which parses token key from request query string."""

    query_param = None

    def __init__(self, *args, query_param=None, **kwargs):
        self.query_param = str(query_param or self.query_param)

        super().__init__(*args, **kwargs)

    def get_token_key_string(self, scope):
        raw_query_params = scope["query_string"].decode()
        query_params = parse_qs(raw_query_params)
        return query_params.get(self.query_param, [""])[0]
