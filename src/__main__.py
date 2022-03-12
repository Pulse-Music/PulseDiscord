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

from modules import resolve_conflicts
resolve_conflicts()

from bot import MusicBot, logger
from basic_util import BasicFunctionility
from discord.ext import commands
import yaml
import discord

with open('config.yml', 'r') as f:
    config = yaml.safe_load(f)

bot = commands.Bot(
    command_prefix=commands.when_mentioned_or(config['prefix']),
    case_insensitive=True,
    owner_ids=config['owners'],
    description=config['description'],
    )

@bot.event
async def on_ready():
    if config['status'].casefold() == 'online':
        status = discord.Status.online
    elif config['status'].casefold() == 'idle':
        status = discord.Status.idle
    else:
        status = discord.Status.dnd
    
    if config['activity']['type'].casefold() == 'listening':
        activity = discord.Activity(type=discord.ActivityType.listening, name=config['activity']['name'])
    elif config['activity']['type'].casefold() == 'watching':
        activity = discord.Activity(type=discord.ActivityType.watching, name=config['activity']['name'])
    elif config['activity']['type'].casefold() == 'playing':
        activity = discord.Game(name=config['activity']['name'])
    elif config['activity']['type'].casefold() == 'streaming':
        activity = discord.Streaming(name=config['activity']['name'], url=config['activity']['url'])

    
    await bot.change_presence(
        activity=activity,
        status=status,
        )
    logger.info(f'Logged in as {bot.user} (ID: {bot.user.id})')

bot.add_cog(BasicFunctionility(bot))
bot.add_cog(MusicBot(bot))
bot.run(config['token'], bot=True, reconnect=True)