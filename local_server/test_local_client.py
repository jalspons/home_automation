import asyncio
import json
import time

local_writer = None

async def send_msg(counter):
    global local_writer
    msg = json.dumps({"req": "ws", "msg" : counter})

    local_writer.write(msg.encode())


async def open_connection():
    reader, writer = await asyncio.open_unix_connection(path="socket")
    global local_writer
    local_writer = writer

    ctr = 0
    while(True):
        await send_msg(ctr)
        await asyncio.sleep(1)
        ctr += 1


asyncio.run(open_connection())
