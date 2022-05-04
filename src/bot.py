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
import pytube
import requests

logger = Logger()

class MusicBot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = logger
        self.init_()
    
    def init_(self):
        """ Initialize the bot """
        self.logger.info(emoji.emojize('✅ MusicBot Cog initialized'))

    async def get_voice_channel(self, ctx, guild_id):
        """ Get the voice channel of the guild """
        guild = self.bot.get_guild(guild_id)
        channel = get(guild.voice_channels, name=FS_NAME)
        if channel is None:
            channel = await guild.create_voice_channel(FS_NAME)
        return channel

    async def get_voice_client(self, ctx, guild_id):
        """A helper function to get the voice client for the guild"""
        guild = self.bot.get_guild(guild_id)
        channel = get(guild.voice_channels, name=FS_NAME)
        if channel is None:
            channel = await guild.create_voice_channel(FS_NAME)
        return channel.voice_client
    
    @commands.command(name='search', aliases=['s'])
    async def search_(self, ctx, *, query):
        """ Search for a song and play"""
        