import asyncio
from websockets.server import serve

C_WEBSOCKET_SERVER_PORT = '8081'

async def echo(websocket):
    async for message in websocket:
        await websocket.send(message)

async def main():
    async with serve(echo, 'localhost', C_WEBSOCKET_SERVER_PORT):
        await asyncio.Future()  # run forever

asyncio.run(main())
