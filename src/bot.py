import discord
from discord.ext import commands
import os
import indexer
import re
import yaml
import sys

with open('config.yml', 'r') as f:
    yaml_config = yaml.safe_load(f)
    BOT_PREFIX = yaml_config.get('bot_prefix')
    BOT_TOKEN = yaml_config.get('bot_token')

try:
    #NOTE: CTX = Context
    play_queue = []
    client = commands.Bot(command_prefix=BOT_PREFIX, owner_id=765739254164357121)

    @client.event
    async def on_ready():
        print(f'Logged in as {client.user}')

    client.recursively_remove_all_commands()

    @client.command()
    async def ping(ctx):
        with ctx.typing():
            await ctx.send(f'Pong! {round(client.latency * 1000)}ms')
        return

    @client.command(aliases=['j'])
    async def join(ctx):
        with ctx.typing():
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
        with ctx.typing():
            server = ctx.message.guild.voice_client
            try:
                await server.disconnect()
            except AttributeError:
                await ctx.send("I am not in a voice channel")
        return

    @client.command(aliases=['p', 'pl'])
    async def play(ctx, *, query):
        with ctx.typing():
            # Check if query is a URL
            if re.match(r'https?://(?:www\.)?youtube\.com/watch\?v=', query):
                vid = indexer.download_audio_raw(query, os.getcwd())
            else:
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
            try:
                await ctx.send(f'Playing {video.title}')
            except UnboundLocalError:
                await ctx.send(f'Playing {indexer.getinfo(query).title}')
        return

    @client.command(aliases=['o'])
    async def owner(ctx):
        with ctx.typing():
            await ctx.send(f'My owner is <@{client.owner_id}>')

    # @client.command(aliases=['pls'])
    # async def playlist(ctx, *, query):
    #     with ctx.typing():
    #         await ctx.reply('Fetching playlist...')
            

    client.run(BOT_TOKEN)

except RuntimeError:
    sys.exit(0)

finally:
    sys.exit(0)