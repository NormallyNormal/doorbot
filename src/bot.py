import os
import sys

script_dir = os.path.dirname( __file__ )
sys.path.append( script_dir )

import discord
import command.command_registry as command_registry
from dotenv import load_dotenv
import doorserver.door_server as door_server

class MyClient(discord.Client):
    async def on_ready(self):
        door_server.start_door_server()
        print(f'Successful login as {self.user}')

    async def on_message(self, message):
        if message.author == self.user:
            return
        message_content_array = message.content.split()
        idx = 0
        for arg in message_content_array:
            print(arg[:2])
            if arg[:2] == '<@':
                message_content_array[idx] = arg[2:len(arg)-1]
            idx += 1
        message_content = ' '.join(message_content_array)
        print(f'Message from {message.author}: {message.content}')
        try:
            response = command_registry.execute(message_content, message.author.id)
        except SyntaxError as syntaxError:
            response = str(syntaxError)
        finally:
            await message.channel.send(response)
        
load_dotenv('bot.env')
BOT_TOKEN = os.getenv('BOT_TOKEN')
intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run(BOT_TOKEN)
