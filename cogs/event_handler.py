import discord

from discord.ext import commands

class EventHandler(commands.Cog, name='Events'):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.owner = (await self.bot.application_info()).owner
        print('Ready.')

def setup(bot):
    bot.add_cog(EventHandler(bot))
