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

logger = Logger()

class MusicBot(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.logger = logger

    @commands.command(name='Join', aliases=['j'], help='Join the voice channel')
    async def join(self, ctx):
        """Join the voice channel"""
        
        try:
            await ctx.author.voice.channel.connect()
        except AttributeError:
            await ctx.reply(f'{ctx.author.mention} You are not in a voice channel')
        return
        
    @commands.command(name='Leave', aliases=['l'], help='Leave the voice channel')
    async def leave(self, ctx):
        """_summary_
        Leave the voice channel
        """
        try:
            await ctx.voice.channel.disconnect()
        except AttributeError as e:
            await ctx.reply(f'{ctx.author.mention} You are not in a voice channel')
            raise e
        return