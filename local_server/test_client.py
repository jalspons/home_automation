import asyncio
import json
import time

import unittest

class Test(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        pass

    async def send_request(self, request):
        self.writer.write(request.encode())
        await self.writer.drain()

    async def receive_response(self):
        data = await self.reader.read(100)
        return json.loads(data.decode())

    async def asyncSetUp(self):
        print('opening connection')
        self.reader, self.writer = \
            await asyncio.open_unix_connection(path="socket")

    async def asyncTearDown(self):
        self.writer.close()
    '''
    async def test_ping(self):
        # Sending request
        request = json.dumps({'request_type': 'PING', 'outlet_id': '1'})
        await self.send_request(request)

        # Receiving response
        response = await self.receive_response()
       
        # Check response
        self.assertEqual(response['status'], 'OK')
        self.assertEqual(response['ping'], {'1': True})

    async def test_ping_all(self):
        # Sending request
        request = json.dumps({'request_type': 'PING', 'outlet_id': ['0', '1', '2']})
        await self.send_request(request)

        # Receiving response
        response = await self.receive_response()
       
        # Check response
        self.assertEqual(response['status'], 'OK')
        self.assertEqual(response['ping'], {'0': False, '1': True, '2': True})
    '''

    async def test_status(self):
        # Sending request
        request = json.dumps({'request_type': 'STATUS'})
        await self.send_request(request)

        # Receiving response
        response = await self.receive_response()
        print(response)

        # Check response
        self.assertEqual(response['status'], 'OK')
        self.assertEqual(response['active'], {'1': False, '2': False, '3': False})

        await asyncio.sleep(5)

        # Sending request
        request = json.dumps({'request_type': 'STATUS'})
        await self.send_request(request)

        # Receiving response
        response = await self.receive_response()
        print(response)

        # Check response
        self.assertEqual(response['status'], 'OK')
        self.assertEqual(response['active'], {'1': False, '2': False, '3': False})




    '''
    async def test_send_activation_with_one_request(self):
        # Sending request
        activation_request = {'outlet_id': '1', 'activation_time': time.time(), 'deactivation_time': time.time() + 1}
        request = json.dumps({ \
            'request_type': 'ACTIVATION', \
            'activation_request': [activation_request] })
        await self.send_request(request)

        # Receiving response
        response = await self.receive_response()
        print(response)

        # Check response
        self.assertEqual(response['status'], 'OK')
        self.assertEqual(response['activation'], {'1': True})
    '''

if __name__ == '__main__':
    unittest.main()








