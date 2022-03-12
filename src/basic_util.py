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

from bot import (
    logger,
    commands,
    discord
    )

class BasicFunctionility(commands.Cog):
    
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.logger = logger
    
    @commands.command(name='Ping')
    async def ping(self, ctx):
        """_summary_
        Ping the bot
        """
        await ctx.reply(f'Pong! {round(self.bot.latency * 1000)}ms')
        return
    
    @commands.command(aliases=['h'], help='Get help')
    async def help_(self, ctx):
        """_summary_
        Get help
        """
        # Create embed
        embed = discord.Embed(
            title = "Help",
            description = f"{self.bot.user.name} command list",
            color = discord.Color.blue(),
            )

        # Add commands
        for c in self.bot.commands:
            embed.add_field(
                name = f"{c.name}",
                value = f"{c.help}"
                )
        # Send embed
        await ctx.reply(embed=embed)
        return