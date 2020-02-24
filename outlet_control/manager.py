from outlet import Outlet

import asyncio
import json
import time
import sys


class Manager():
    
    '''
    
    Outlets is a list containing dictionaries with buttons and pins
    
    e.g. with 3 outlets:
    [   {'buttons' : { 'on' : 27, 'off' : 25 }, 'id' : 1}, 
        {'buttons' : { 'on' : 12, 'off' : 14 }, 'id' : 2}, 
        {'buttons' : { 'on' : 11, 'off' : 10 }, 'id' : 3} 
    ]
    
    '''

    def __init__(self, outlets, path):
        self.outlets = {}
        self.create_outlets(outlets)
        self.path = path

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

    def parse_message(self, message):
        request = json.loads(message)
        response = {'response_type': request['request_type']}
        status = {}

        if request['request_type'] == 'ACTIVATION':
            for outlet in request['outlet_id']:
                status[outlet] = self.pass_new_request_to_outlet(outlet, request['task'])

        elif request['request_type'] == 'PING':
            for outlet in request['outlet_id']:
                status[outlet] = self.ping_outlet_worker(outlet)
        
        else:
            status = {'-1': 'Unknown request'}

        response['outlet_status'] = status
        return response

    async def open_unix_connection(self):
        (self.reader, self.writer) = await asyncio.open_unix_connection(path=self.path)

        self.writer.write('Hello'.encode())
        await self.writer.drain()
        
        while True:
            data = await self.reader.read(1024)
            message = data.decode()
            print(message)
            self.parse_message(message)
