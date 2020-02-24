from channels.generic.websocket import AsyncWebsocketConsumer
import json

from dashboard.models import Activation, Outlet
from websocketControl.models import Client

class ControlConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        print(f'######## OPEN Channel name: {self.channel_name}')
        await self.channel_layer.group_add("CONTROLGROUP", self.channel_name)

    async def disconnect(self, close_code):
        self.channel_layer.group_discard("CONTROLGROUP", self.channel_name)
        print(f'##############CLOSING {self.channel_name}')
        await self.close()
        
    # Receive message from websocket
    async def receive(self, text_data):
        pass

    # Receive message from redis channel
    async def chat_message(self, event):
        print(f'######## MESSAGE {event}')
        #await self.send(text_data='Hello, World!')
        await self.send(text_data=json.dumps({
            'request_type': event['request_type'],
            'outlet_id': event['outlet'],
            'task': event['task']}))
