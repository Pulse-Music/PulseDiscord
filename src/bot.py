import discord
import os
from dotenv import load_dotenv
import sys

# Bot invite link is:
# https://discord.com/api/oauth2/authorize?client_id=936976871822872597&permissions=517660462913&scope=bot%20applications.commands
load_dotenv()
client = discord.Client()
PREFIX = 'yt'

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

async def join_voice_channel(channel):
    voice = await channel.connect()
    return voice

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    msg = str(message.content)
    if msg.startswith('yt'):
        cmd = msg.removeprefix('yt').split(' ')

try:
    client.run(os.getenv('BOTTOKEN'))
except RuntimeError:
    sys.exit(1)