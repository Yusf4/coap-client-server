import asyncio
import random
from aiocoap import Context, Message

async def main():
    # Define the target server address and port
    host = '127.0.0.1'  # Server address
    port = 5683  # CoAP default port

    # Create the CoAP context
    context = await Context.create_client_context()

    try:
        while True:
            # Generate new sensor data
            temperature = round(random.uniform(20.0, 30.0), 2)
            humidity = round(random.uniform(30.0, 50.0), 2)

            # Print generated data for debugging
            print(f"Generated Data: Temperature = {temperature}°C, Humidity = {humidity}%")

            # Create a CoAP POST request with the generated payload
            payload = f"{temperature},{humidity}"
            request = Message(code=2, uri=f'coap://{host}:{port}/sensor', payload=payload.encode())

            try:
                # Send the request and wait for the response
                response = await asyncio.wait_for(context.request(request).response, timeout=5)
                print("Response from server:", response.payload.decode())
            except asyncio.TimeoutError:
                print("Request timed out.")
            except Exception as e:
                print(f"Error while sending data: {e}")

            # Wait for 5 seconds before generating the next value
            await asyncio.sleep(5)
    except KeyboardInterrupt:
        print("Client stopped.")
    finally:
        # Shutdown the context when exiting
        await context.shutdown()

if __name__ == "__main__":
    asyncio.run(main())
