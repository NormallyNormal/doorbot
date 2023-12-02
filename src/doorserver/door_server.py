import asyncio
from websockets.server import serve
from threading import Thread
import hashlib
from hmac import compare_digest

websockets_list = dict()

class SocketServerThread(Thread):
     def __init__(self):
         super(SocketServerThread, self).__init__()

     def run(self):
         asyncio.run(connect_serve())

async def connect_serve():
    async with serve(handle_connect, "", 8765):
        try:
            await asyncio.Future()
        except:
            return
         
async def handle_connect(websocket):
    m = hashlib.sha256()
    door_info = await websocket.recv()
    door_info = door_info.split(' ')
    door_name = door_info[0]
    door_password = door_info[1]
    door_salt = "salt" #query door salt
    door_password = door_password + door_salt
    m.update(door_password.encode('utf-8'))
    door_password = m.digest()
    door_known_password = b'\xf3\xabm\x7fw\x9d\xdc)\xdafD\x8f\xf3q\x1a\xf1\xdf\x12\x89\xc9\xde\x16\xf5\xd7l\x91\x8d\x9f>\xf6;.' #query stored door password
    if compare_digest(door_password, door_known_password):
        websockets_list[door_name] = websocket
    else:
        await websocket.close()
    async for message in websocket:
        try:
            await websocket.send(message)
        except:
            return

def open_door(door_name):
    asyncio.run(open_door_async(door_name))

async def open_door_async(door_name):
    try:
        await websockets_list[door_name].send("open")
    except:
        raise ValueError("That door is not currently connected.")

def start_door_server():
    SocketServerThread().start()

start_door_server()
while True:
    continue

#HOW TO USE:
#run once:
#start_door_server()
#then run to open a door with a name:
#open_door("room403")
