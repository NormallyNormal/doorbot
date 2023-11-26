import os
import sys

script_dir = os.path.dirname( __file__ )
sys.path.append( script_dir )

import discord
import command.command_registry as command_registry
from dotenv import load_dotenv

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Successful login as {self.user}')

    async def on_message(self, message):
        if message.author == self.user:
            return
        print(f'Message from {message.author}: {message.content}')
        try:
            response = command_registry.execute(message.content)
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
