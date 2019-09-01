import discord
import json
import os

from discord.ext import commands
from bot import memory


class Memory(commands.Cog, name='Memory', command_attrs=dict(hidden=False)):
    def __init__(self, bot, memory):
        self.bot = bot
        self.memory = memory

    @commands.command(name='remember', brief='Sets a default voice channel to join.')
    @commands.is_owner()
    async def remember(self, ctx):
        if not ctx.author.voice:
            return await ctx.send('You are not in a voice channel.')
        self.memory["remember"] = str(ctx.author.voice.channel.id)
        with open('./config/memory.json', 'w') as f:
            json.dump(self.memory, f, indent=4)
        await ctx.send('I will remember.')

    @commands.command(name='forget', brief='Removes the default voice channel to join.')
    @commands.is_owner()
    async def forget(self, ctx):
        self.memory["remember"] = 0
        with open('./config/memory.json', 'w') as f:
            json.dump(self.memory, f, indent=4)
        await ctx.send('I have forgotten.')

    @commands.command(name='scribe', brief='Aliases a path for safer queueing.')
    @commands.is_owner()
    async def scribe(self, ctx, *args):
        if len(args) != 2:
            return await ctx.send('Bad paramters.')
        alias, path = args
        if not path.endswith('.mp3') and not path.endswith('\\'): path += '\\'
        if self.memory["spellbook"].get(alias.lower(), None) is not None:
            return await ctx.send('That is already a spell. See `-rescribe`.')
        
        self.memory["spellbook"][alias.lower()] = path
        with open('./config/memory.json', 'w') as f:
            json.dump(self.memory, f, indent=4)
        await ctx.send('Spell inscribed.')

    @commands.command(name='rescribe', brief='Edits an existing path alias.')
    @commands.is_owner()
    async def rescribe(self, ctx, *args):
        if len(args) != 2:
            return await ctx.send('Bad paramters.')
        alias, path = args
        if self.memory["spellbook"].get(alias.lower(), 'None') is None:
            return await ctx.send('That is not a spell.')

        self.memory["spellbook"][alias.lower()] = path
        with open('./config/memory.json', 'w') as f:
            json.dump(self.memory, f, indent=4)
        await ctx.send('Spell rescribed.')

    @commands.command(name='annul', brief='Removes an existing path alias.')
    @commands.is_owner()
    async def annul(self, ctx, *, alias):
        spell = self.memory["spellbook"].pop(alias.lower(), None)
        if not spell:
            return await ctx.send('That is not a spell.')

        with open('./config/memory.json', 'w') as f:
            json.dump(self.memory, f, indent=4)
        await ctx.send('Spell annulled.')


def setup(bot):
    bot.add_cog(Memory(bot, memory))
