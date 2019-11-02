import asyncio
import websockets

ws_sock = None
local_read = None
local_write = None

loop = asyncio.get_event_loop()

def test():
    return input('Give cmd:')

async def local_server_handler(reader, writer):
    print('New connection')
    await send_cmd(writer, test().encode())
    await receive_response(reader)

async def init_local_server():
    print('Starting server')
    server = await asyncio.start_unix_server(
            local_server_handler, path='socket')

    async with server:
        await server.serve_forever()

async def send_cmd(writer, cmd):
    writer.write(cmd)
    await writer.drain()
    
async def receive_response(reader):
    data = await reader.read()
    cmd = data.decode()
    print(cmd)


'''
async def init_websocket_client():
    async with websockets.connect(uri) as websocket:
        await websocket.read 
'''
asyncio.run(init_local_server())




