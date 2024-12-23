import asyncio
from aiocoap import *
from aiocoap.resource import Resource, Site

class SimpleResource(Resource):
    def __init__(self):
        super().__init__()

    async def render_get(self, request):
        return Message(payload=b"Hello, this is a CoAP server response!")

async def main():
    root = Site()
    root.add_resource(('.well-known/core',), Resource())
    root.add_resource(('hello',), SimpleResource())

    # Explicitly bind to localhost
    context = await Context.create_server_context(root, bind=("127.0.0.1", 5683))
    print("CoAP server is running on 127.0.0.1:5683")
    await asyncio.get_running_loop().create_future()

if __name__ == "__main__":
    asyncio.run(main())
