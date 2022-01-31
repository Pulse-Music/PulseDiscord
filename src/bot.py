import discord
from discord.ext import commands
import dotenv
import os
import indexer
import asyncio


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
        return None
    # join the voice channel
    await voice_channel.connect()
    await ctx.send(f'Joined <#{voice_channel.id}>')
    return voice_channel

@client.command(aliases=['l'])
async def leave(ctx):
    server = ctx.message.guild.voice_client
    try:
        await server.disconnect()
    except AttributeError:
        await ctx.send("I am not in a voice channel")

@client.command(aliases=['p'])
async def play(ctx, *, query):
    await ctx.send(f'Searching for {query}...')
    # If the bot is not in a voice channel, join the channel
    video = indexer.search(query)[0]
    vid = indexer.download_audio(video, os.getcwd())
    
    try:
        os.rename(vid, 'audio.mp3')
    except FileExistsError:
        os.remove('audio.mp3')
        os.rename(vid, 'audio.mp3')
    
    vid = 'audio.mp3'
    tmp = await join(ctx)
    if tmp is None:
        return
    audio = discord.FFmpegPCMAudio(
            executable=os.path.abspath(
                'ffmpeg/bin/ffmpeg.exe'
            ),
            source=vid,
        )

    ctx.voice_client.play(audio)
    await ctx.send(f'Playing {video.title}')

client.run(os.getenv('BOT_TOKEN'))