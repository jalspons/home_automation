import asyncio
import logging
import json
from socket import socket
import websockets

logger = logging.getLogger('websockets')
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())
logging.basicConfig(level=logging.DEBUG)

ws_sock = None
local_writer = None
uri = "ws://127.0.0.1:8000/ws/control/"
sockpath = "socket"

#------------------ Websockets ------------------

async def open_ws_connection():
    global ws_sock
    async with websockets.connect(uri) as websocket:
        ws_sock = websocket
        async for message in websocket:
            #await send_local_message(message)
            await print_msg(message)

async def print_msg(message):
    print(message)

async def send_ws_msg(message):
    await ws_sock.send(message)
    print(message)

def close_ws_sock():
    if (ws_sock != None):
        ws_sock.close()


# ------------------- Local IPC ------------------------

async def open_local_server():
    print('Starting server')
    server = await asyncio.start_unix_server(open_local_connection, path=sockpath)
    server.get_loop().create_task(open_ws_connection())
    async with server:
        await server.serve_forever()

async def open_local_connection(reader, writer):
    global local_writer
    local_writer = writer
    await local_receive_request(reader)


async def local_receive_request(reader):
    while(True):
        message = await reader.read(100)
        await send_ws_msg(message.decode())
        
        data = json.loads(message.decode())
        print(data['req'], data['msg'])

async def send_local_message(message):
    global local_writer
    if (local_writer != None):
        local_writer.write(message.encode())

def close_local_connection():
    if (local_writer != None):
        local_writer.close()


# -------------- Helper funcs --------------------

def test():
    return input('Give cmd:')

def testJson():
    msg = json.dumps({"req": "WS", "msg" : "Jepajee"})
    return msg

# ------------- Start the server -------------------

asyncio.run(open_ws_connection())
