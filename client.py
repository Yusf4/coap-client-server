import asyncio
from aiocoap import *

async def fetch_coap_resource():
    protocol = await Context.create_client_context()

    request = Message(code=GET, uri="coap://127.0.0.1:5683/hello")

    try:
        response = await protocol.request(request).response
        print(f"Response: {response.payload.decode('utf-8')}")
    except Exception as e:
        print(f"Failed to fetch resource: {e}")
    finally:
        await protocol.shutdown()  # Clean up the protocol context

if __name__ == "__main__":
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(fetch_coap_resource())
    finally:
        loop.run_until_complete(loop.shutdown_asyncgens())  # Clean async generators
        loop.close()  # Ensure the event loop is properly closed
