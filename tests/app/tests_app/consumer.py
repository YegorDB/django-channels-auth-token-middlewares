class MockConsumer:
    async def __call__(self, scope, receive, send):
        return scope
