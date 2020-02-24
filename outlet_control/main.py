import asyncio
import json

from manager import Manager

control = None
host = 'localhost'
local_server_port = 15562

if __name__ == '__main__':
    with open('outlets.json') as f:
        data = json.load(f)
        control = Manager(data, host, local_server_port)

    asyncio.run(control.open_connection())
