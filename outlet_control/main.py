import asyncio
import json

from manager import Manager

control = None

# TODO event loop for listening server program

async def receive_cmd(reader):
    data = await reader.read(100)
    msg = data.decode()
    return msg
   
async def send_msg(writer, msg):
    data = msg.encode()
    writer.write(data)
    await writer.drain()

async def run_client():
    (reader, writer) = await asyncio.open_unix_connection(path='/home/pi/projects/websocket_client/socket')
    
    msg = await receive_cmd(reader)
    print(msg)
    if msg == 'OK':
        control.activate_outlet(1, 0.1)
        await asyncio.sleep(2)
        print('Is thread active...', control.is_active_outlet(1))
        await send_msg(writer, 'Good job!')
        
        control.deactivate_outlet(1)
        await asyncio.sleep(2)
        print('Is thread active...', control.is_active_outlet(1))

if __name__ == '__main__':
    with open('outlets.json') as f:
        data = json.load(f)
        control = Manager(data)

    asyncio.run(run_client())



