# MIT License
#
# Copyright (c) 2022-Present Advik-B <advik.b@gmail.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from modules import (
    
    search_,
    download_audio,
    FS_NAME,
    get_playlist,
    getinfo,
    index_for_video_locally,
    Logger,
    unzip,
    errors,
)
import emoji
import discord
from discord.ext import commands
from discord.utils import get
import asyncio
import re
import os

logger = Logger()

class MusicBot(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.logger = logger
        self.emoji = [
            ":one:",
            ":two:",
            ":three:",
            ":four:",
            ":five:",
            ":six:",
            ":seven:",
            ":eight:",
            ":nine:",
            ":keycap_ten:",
        ]
        # RegEx for youtube links
        self.RegEx = re.compile(
            r"(?:https?:\/\/)?(?:www\.)?(?:youtu\.be\/|youtube\.com\/(?:embed\/|v\/|watch\?v=|watch\?.+&v=))((\w|-){11})(?:\S+)?",
            re.MULTILINE,
        )
        

    @commands.command(name='Join', aliases=['j'], help='Join the voice channel')
    async def join(self, ctx):
        try:
            await ctx.author.voice.channel.connect()
        except AttributeError:
            await ctx.reply('You are not in a voice channel')
        return
        
    @commands.command(name='Leave', aliases=['l'], help='Leave the voice channel')
    async def leave(self, ctx):
        try:
            voice = get(self.bot.voice_clients, guild=ctx.guild)
            if voice and voice.is_connected():
                await voice.disconnect()
            elif not voice:
                await ctx.reply('I am not in a voice channel')
        except AttributeError as e:
            await ctx.reply('You are not in a voice channel')
            raise e from e
        return
    
    @commands.command(name='Search', aliases=['s'], help='Search for a song to play')
    async def search(self, ctx, *, query: str):
        # Typing the command with no query will return the help message
        self.logger.info(f'{ctx.author} searched for {query}')
        if not query:
            await ctx.reply('Please type the command with a query')
            return
        # Search for the song
        try:
            results = search_(query)
            embed = discord.Embed(title='Search Results', color=0x00ff00)
            for index, result in enumerate(results):
                embed.add_field(name=result.title, value=str(index + 1), inline=False)
            
            # Send the embed to the channel
            message = await ctx.reply(embed=embed)
            # Add reactions to the message from 1 to 10
            for emoji_ in self.emoji:
                await message.add_reaction(
                    emoji.emojize(
                        emoji_,
                        use_aliases=True
                        )
                    )
            # Wait for a reaction
            def check(reaction, user):
                return user == ctx.author and str(reaction.emoji) in self.emoji
            try:
                reaction, user = await self.bot.wait_for('reaction_add', timeout=30.0, check=check)
            except asyncio.TimeoutError:
                await ctx.reply('You took too long to select a song')
                return
            # Get the index of the selected song
            index = self.emoji.index(str(reaction.emoji))
            # Play the selected song
            await self.play(ctx, results[index])
            
        except errors.SearchError as e:
            await ctx.reply(e)
            raise e from e
        return
    
    
    @commands.command(name='Play', aliases=['p'], help='Same as search but will play the first song')
    async def play(self, ctx, *, query: str):
        channel = ctx.message.author.voice.channel
        if not channel:
            await ctx.reply("You are not connected to a voice channel")
            return
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        self.logger.info(f'{ctx.author} asked for to {query}')

        if self.RegEx.match(query):
            if result := index_for_video_locally(getinfo(query)):
                await self.play_aud(ctx, result)
            else:
                path = download_audio(getinfo(query), FS_NAME)
                await self.play_aud(ctx, path)

        # Try searching for the song locally
        results = search_(query)
        result_ = results[0]
        if result := index_for_video_locally(result_):
            await self.play_aud(ctx, result)
        else:
            path = download_audio(result_, FS_NAME)
            await self.play_aud(ctx, path)
    
    async def play_aud(self, ctx, path: str):
        path = str(unzip(path)).replace('mp3.7z.mp3.7z', '.mp3')
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        if not voice or not voice.is_connected():
            voice = await ctx.author.voice.channel.connect()
        voice.play(discord.FFmpegPCMAudio(path, executable=r"ffmpeg\bin\ffmpeg.exe"))
        await ctx.reply('Playing %s' % path.split('\\')[-1])
        return