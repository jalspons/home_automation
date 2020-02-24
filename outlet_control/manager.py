from outlet import Outlet

import asyncio
import json
import time
import sys


class Manager():
    
    '''
    
    Outlets is a list containing dictionaries with buttons and pins
    
    e.g. with 3 outlets:
    [   {'buttons' : { 'on' : 27, 'off' : 25 }, 'id' : "1"}, 
        {'buttons' : { 'on' : 12, 'off' : 14 }, 'id' : "2"}, 
        {'buttons' : { 'on' : 11, 'off' : 10 }, 'id' : "3"} 
    ]
    
    '''

    def __init__(self, outlets, host, port):
        self.outlets = {}
        self.create_outlets(outlets)
        self.port = port
        self.host = host

#################################################
# Outlet control
#################################################

    def create_outlets(self, outlets):
        for outlet in outlets:
            self.outlets[outlet['id']] = Outlet(outlet['id'], outlet['buttons'])

    def pass_new_request_to_outlet(self, outlet, request):
        return self.outlets[outlet].new_request(request)

    def ping_outlet_worker(self, outlet):
        return self.outlets[outlet].ping_worker()

#################################################
# Message passing
#################################################
    '''
    Messages ():
    {   
        'recipier': _                       # String    *required
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
    def parse_message(self, message):
        request = json.loads(message)
        response = {'response_type': request['request_type']}
        status = {}

        if request['request_type'] == 'ACTIVATION':
            print(request['outlet_data'])
            for outlet,req in request['outlet_data'].items():
                print(outlet)
                status[outlet] = self.pass_new_request_to_outlet(outlet, req)

        elif request['request_type'] == 'PING':
            for outlet, req in request['outlet_data']:
                status[outlet] = self.ping_outlet_worker(outlet)
        
        else:
            status = {'-1': 'Unknown request'}

        response['outlet_status'] = status
        return response

    async def send_message_to_local_server(self, message):
        self.writer.write(message.encode())
        await self.writer.drain()

    async def open_connection(self):
        (self.reader, self.writer) = await asyncio.open_connection(
            host=self.host, port=self.port)

        control_introduction_request = json.dumps({
            'recipient': 'local_server',
            'sender': 'outlet_control'
        })
        await self.send_message_to_local_server(control_introduction_request)
        
        while True:
            data = await self.reader.read(1024)
            message = data.decode()
            print(message)
            self.parse_message(message)
