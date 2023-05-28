from channels.generic.http import AsyncHttpConsumer


class MockConsumer:
    async def __call__(self, scope, receive, send):
        return scope


class TestHttpConsumer(AsyncHttpConsumer):
    async def handle(self, body):
        user = self.scope["user"]
        user_id = None if user.is_anonymous else user.id

        await self.send_response(200, str(user_id).encode())
