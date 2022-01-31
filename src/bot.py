import discord
from discord.ext import commands
import dotenv
import os

dotenv.load_dotenv()
#NOTE: CTX = Context
client = commands.Bot(command_prefix='.', owner_id=765739254164357121)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

client.recursively_remove_all_commands()

@client.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(client.latency * 1000)}ms')


@client.command(aliases=['j'])
async def join(ctx):
    global voice_channels
    # If the bot is not in a voice channel, join the channel
    # get the voice channel the user is in
    try:
        voice_channel = ctx.author.voice.channel
    except AttributeError:
        await ctx.reply("You are not in a voice channel")
        return
    # join the voice channel
    await voice_channel.connect()
    await ctx.send(f'Joined #{voice_channel.name}')

@client.command(aliases=['l'])
async def leave(ctx):
    server = ctx.message.guild.voice_client
    try:
        await server.disconnect()
    except AttributeError:
        await ctx.send("I am not in a voice channel")

client.run(os.getenv('BOT_TOKEN'))