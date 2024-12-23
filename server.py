import asyncio
from aiocoap import Context, Message
from aiocoap.resource import Resource, Site

class HumidityResource(Resource):
    async def render_get(self, request):
        # Your resource logic here
        response = Message(code=aiocoap.CONTENT)
        response.payload = b"Humidity data"
        return response

async def main():
    # Create the CoAP site
    site = Site()

    # Add the resource to the site
    site.add_resource(('humidity',), HumidityResource())

    # Create the server context and bind to port 5683
    context = await Context.create_server_context(site, bind=('localhost', 5683))
    print("Server listening on coap://localhost:5683")
    await asyncio.Event().wait()  # Keep the server running

if __name__ == "__main__":
    asyncio.run(main())
