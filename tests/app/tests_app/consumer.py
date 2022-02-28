from channels.generic.http import AsyncHttpConsumer


class TestHttpConsumer(AsyncHttpConsumer):
    async def handle(self, body):
        if not self.scope["user"] or self.scope["user"].is_anonymous:
            response_code = 401
        else:
            response_code = 200

        await self.send_response(response_code, b"Response bytes", headers=[
            (b"Content-Type", b"text/plain"),
        ])
