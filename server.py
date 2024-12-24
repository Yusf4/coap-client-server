import asyncio
from aiocoap import Context, Message
from aiocoap.resource import Resource, Site

# Define content type manually
TEXT_PLAIN = 0  # This corresponds to the CoAP content type for plain text


class SensorResource(Resource):
    def __init__(self):
        super().__init__()
        self.temperature = None
        self.humidity = None

    async def render_post(self, request):
        # Extract temperature and humidity from the request payload
        payload = request.payload.decode()
        data = payload.split(",")  # Assume the payload is in the format "temperature,humidity"

        if len(data) == 2:
            try:
                self.temperature = float(data[0])
                self.humidity = float(data[1])
                print(f"message from client:temp:{self.temperature},humidity{self.humidity}")
                response_payload = f"Received Temperature: {self.temperature}°C, Humidity: {self.humidity}%"
            except ValueError:
                response_payload = "Invalid data values. Ensure they are numeric."
        else:
            response_payload = "Invalid data format. Expected: temperature,humidity"

        response = Message(code=65)  # 65 means 'Created'
        response.payload = response_payload.encode()
        response.content_format = TEXT_PLAIN  # Set the content type to plain text

        return response

    async def render_get(self, request):
        if self.temperature is not None and self.humidity is not None:
            response_payload = f"Temperature: {self.temperature}°C, Humidity: {self.humidity}%"
        else:
            response_payload = "No data available"

        response = Message(code=69)  # 69 means 'Content'
        response.payload = response_payload.encode()
        response.content_format = TEXT_PLAIN  # Set the content type to plain text

        return response


async def main():
    site = Site()  # Create a site, which is a container for resources
    sensor = SensorResource()  # Create the sensor resource
    site.add_resource(('sensor',), sensor)  # Add the sensor resource to the site using a tuple

    # Bind the server to localhost (127.0.0.1) and port 5683
    context = await Context.create_server_context(site, bind=("127.0.0.1", 5683))
    print("CoAP server running on 127.0.0.1:5683...")


    try:
        await asyncio.Event().wait()  # Keep the server running
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    asyncio.run(main())
