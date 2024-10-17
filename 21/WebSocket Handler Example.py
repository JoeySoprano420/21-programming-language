async def your_websocket_handler(websocket, path):
    async for message in websocket:
        await websocket.send(f"Message received: {message}")
