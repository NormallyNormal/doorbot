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
        if(message_content != 'button'):
            try:
                response = command_registry.execute(message_content, message.author.id)
            except SyntaxError as syntaxError:
                response = str(syntaxError)
            finally:
                response_chunked = chunk_string(response)
                for response_part in response_chunked:
                    await message.channel.send(response_part)
        else:
            await message.channel.send("This button will open your default door!", view=MyView())
            
class MyView(discord.ui.View):
    @discord.ui.button(label="Open Door", style=discord.ButtonStyle.primary)
    async def button_callback(self, interaction, button):
        response = command_registry.execute('open', interaction.user.id)
        await interaction.response.defer()
            
def chunk_string(text, chunk_size=2000):
    chunks = []
    while len(text) > chunk_size:
        last_newline_index = text.rfind('\n', 0, chunk_size)
        if last_newline_index == -1:
            # No newline found within the chunk_size
            chunks.append(text[:chunk_size])
            text = text[chunk_size:]
        else:
            chunks.append(text[:last_newline_index])
            text = text[last_newline_index+1:]
    chunks.append(text)
    return chunks

load_dotenv('bot.env')
BOT_TOKEN = os.getenv('BOT_TOKEN')
intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run(BOT_TOKEN)
