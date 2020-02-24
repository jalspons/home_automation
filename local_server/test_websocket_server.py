import asyncio
import logging
import json
import websockets
import time

logger = logging.getLogger('websockets')
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())
logging.basicConfig(level=logging.DEBUG)

ws = None

async def handle_request(websocket, path):
    print("New connection")
    global ws
    ws = websocket
    asyncio.get_event_loop().create_task(send_msg())
    async for message in ws:
        print(message)

async def send_msg():
    while(True):
        new_req = json.dumps({"req" : "local", "msg" : "WS RULEZ!" })
        await ws.send(new_req)
        print(new_req)
        await asyncio.sleep(1)


start_server = websockets.serve(handle_request, "127.0.0.1", 8080)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()