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
import discord
from discord.ext import commands
from discord.utils import get

logger = Logger()

class MusicBot(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.logger = logger
        self.emoji = {
            "1":":one:",
            "2":":two:",
            "3":":three:",
            "4":":four:",
            "5":":five:",
            "6":":six:",
            "7":":seven:",
            "8":":eight:",
            "9":":nine:",
            "10":":keycap_ten:",
        }

    @commands.command(name='Join', aliases=['j'], help='Join the voice channel')
    async def join(self, ctx):
        """Join the voice channel"""
        
        try:
            await ctx.author.voice.channel.connect()
        except AttributeError:
            await ctx.reply('You are not in a voice channel')
        return
        
    @commands.command(name='Leave', aliases=['l'], help='Leave the voice channel')
    async def leave(self, ctx):
        """_summary_
        Leave the voice channel
        """
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
        if not query:
            await ctx.reply('Please type the command with a query')
            return
        # Search for the song
        try:
            results = search_(query)
            embed = discord.Embed(title='Search Results', color=0x00ff00)
            for index, result in enumerate(results):
                embed.add_field(name=result.title, value=str(index), inline=False)
            
        except errors.SearchError as e:
            await ctx.reply(e)
            raise e from e
        return
    