import asyncio
import logging
import json
import websockets

logger = logging.getLogger('websockets')
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())
logging.basicConfig(level=logging.DEBUG)

uri = "ws://127.0.0.1:8000/ws/control/"
local_server_port = 15562

#------------------ Websockets ------------------

class LocalServer:
    def __init__(self):
        asyncio.run(self.open_local_server())

    async def open_ws_connection(self):
        async with websockets.connect(uri) as websocket:
            self.ws_sock = websocket
            async for message in websocket:
                await self.print_message(message)
                await self.send_control_message(message)

    async def send_ws_message(self, message):
        await self.ws_sock.send(message)
        await self.print_message(message)

    def close_ws_sock(self):
        try:
            self.ws_sock.close()
        except:
            print('Failed to close websocket')


    # ------------------- Local IPC ------------------------

    '''
    Message form:
    {   
        'recipier': _,                      # String    *required
        'sender': _,                        # String    *required
        'request_type': _,                  # String    *required
        'outlet_data': {                    # 
            '_': {                          # Char (outlet_id)
                'activation_time': _,       # Timestamp (seconds)
                'deactivation_time': _,     # Timestamp (seconds)
                'status': _,                # Boolean (Active)
            },
            '_': { ... },
            ...
        }
    }
    '''

    async def open_local_server(self):
        print('Starting server')
        server = await asyncio.start_server(
            self.open_local_connection, port=local_server_port)
        server.get_loop().create_task(self.open_ws_connection())
        async with server:
            await server.serve_forever()

    async def open_local_connection(self, reader, writer):
        while True:
            message = await reader.read(1024)
            #await self.print_message(message)
            request = json.loads(message.decode())
            #print(request)
            if request['recipient'] == 'local_server':
                await self.set_outlet_control_writer(writer)
            elif request['recipient'] == 'outlet_control':
                await self.send_control_message(message)
            elif request['recipient'] == 'web-server':
                await self.send_ws_message(message.deconde())
            

    async def send_control_message(self, message):
        await self.print_message(message)
        try:
            self.outlet_control_writer.write(message.encode())
            await self.local_writer.drain()
        except:
            print('Failed to send local message')

# ------------- Helper functions -------------------
    async def set_outlet_control_writer(self, writer):
        self.outlet_control_writer = writer

    async def print_message(self, message):
        print(message)

    async def interactive_send_tester(self):
        while True:
            message = input('Give message:')
            await self.send_control_message(message)
        

# ------------- Start the server -------------------
LocalServer()
    
