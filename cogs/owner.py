import discord

from discord.ext import commands

class Owner(commands.Cog, name='Owner', command_attrs=dict(hidden=True)):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='load', brief='Loads a cog.')
    @commands.is_owner()
    async def load(self, ctx, cog: str):
        try:
            self.bot.load_extension('cogs.'+cog)
        except Exception as error:
            await ctx.send(f'Unable to load cog `{cog}`.')
            await ctx.send(f'Error: `{error}`')
        else:
            await ctx.send(f'Loaded cog `{cog}`.')

    @commands.command(name='unload', brief='Unloads a cog.')
    @commands.is_owner()
    async def unload(self, ctx, cog: str):
        try:
            self.bot.unload_extension('cogs.'+cog)
        except Exception as error:
            await ctx.send(f'Unable to unload cog `{cog}`.')
            await ctx.send(f'Error: `{error}`')
        else:
            await ctx.send(f'Unloaded cog `{cog}`.')

    @commands.command(name='reload', brief='Reloads a cog.')
    @commands.is_owner()
    async def reload(self, ctx, cog: str):
        try:
            self.bot.unload_extension('cogs.'+cog)
            self.bot.load_extension('cogs.'+cog)
        except Exception as error:
            await ctx.send(f'Unable to reload cog `{cog}`.')
            await ctx.send(f'Error: `{error}`')
        else:
            await ctx.send(f'Reloaded cog `{cog}`.')

    @commands.command(name='logout', brief='Logs the bot out.')
    @commands.is_owner()
    async def logout(self, ctx):
        await self.bot.logout()

def setup(bot):
    bot.add_cog(Owner(bot))