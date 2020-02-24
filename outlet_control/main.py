import asyncio
import json

from manager import Manager

control = None
path = '../local_server/socket'

if __name__ == '__main__':
    with open('outlets.json') as f:
        data = json.load(f)
        control = Manager(data, path)

    asyncio.run(control.open_unix_connection())
