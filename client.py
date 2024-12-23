import asyncio
from aiocoap import Context, Message
from aiocoap.numbers.codes import GET

async def test_client():
    context = await Context.create_client_context()
    request = Message(code=GET, uri='coap://localhost:5683/humidity')
    try:
        response = await context.request(request).response
        print(f"Response payload: {response.payload.decode()}")
    except Exception as e:
        print(f"Request failed: {e}")
    finally:
        await asyncio.sleep(1)  # Ensure clean termination

if __name__ == "__main__":
    asyncio.run(test_client())  # Properly handles event loop creation and cleanup
