#!/usr/bin/python3.6
''' Figure out which ip adress in this given network range is alive'''
# python -m install pythonping
import asyncio, time, pythonping
from concurrent.futures import ProcessPoolExecutor
def _ping(number, ip):
    try:
        data = pythonping.ping('{}{}'.format(number, ip), timeout=1, count=1)
        if data.success():
            print('{}{} created valid response ({})'.format(number, ip, data._responses[0]))

    except PermissionError:
            print('Premission denied. Failed to create socket. You must be root.')
            return False

async def someloop(loop):
    ip = '.208.82.14'
    for number in range(1, 255):
           loop.run_in_executor(None, _ping(number, ip))
async def counter(loop):
    await someloop(loop)
    #for number in range(1, 255):
    #       await loop.create_task(_ping(number, ip))
           
loop = asyncio.get_event_loop()
loop.run_until_complete(counter(loop))