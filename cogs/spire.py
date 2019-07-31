import discord
import json
import os

from discord.ext import commands, tasks
from bot import memory


class Spire(commands.Cog, name='Spire', command_attrs=dict(hidden=False)):
    def __init__(self, bot, memory):
        self.bot = bot
        self.memory = memory
        self.queue = []

    @tasks.loop(seconds=2.0, count=None)
    async def queue_task(self):
        if not self.voice_client.is_playing():
            try:
                track = self.queue.pop(0)
                source = await discord.FFmpegOpusAudio.from_probe(track, method='native', **dict(before_options='-stats'))
                self.voice_client.play(source)
                activity = track[track.rfind('\\'):-4][track.index(' ')-1:]
                await self.bot.change_presence(activity=discord.Activity(name=activity, type=2))
            except IndexError:
                self.queue_task.cancel()

    @commands.command(name='harken', brief='Adds the bot to a voice channel.')
    @commands.is_owner()
    async def harken(self, ctx, channel: discord.VoiceChannel=None):
        if channel:
            await channel.connect()
        elif not ctx.author.voice:
            return await ctx.send('You are not in a voice channel.')
        client = ctx.guild.voice_client
        if not client:
            client = await ctx.author.voice.channel.connect()
        self.voice_client = client

    @commands.command(name='ignore', brief='Removes the bot from a voice channel.')
    @commands.is_owner()
    async def ignore(self, ctx):
        client = ctx.guild.voice_client
        if not client:
            return
        await client.disconnect()
        self.queue = []
        await self.bot.change_presence(activity=None)

    @commands.command(name='cast', brief='Plays music with integrated queue.')
    @commands.is_owner()
    async def cast(self, ctx, *, path: str):
        if not ctx.guild.voice_client and self.memory["remember"] != "none":
            channel = await commands.VoiceChannelConverter().convert(ctx, self.memory["remember"])
            await ctx.invoke(self.bot.get_command("harken"), channel)
        spell = self.memory["spellbook"].get(path.lower(), None)
        if spell is not None: 
            path = spell
        if not path.endswith('.mp3'):
            if not path.endswith('\\'): path += '\\'
            files = os.listdir(path)
            for file in files:
                self.queue.append(path+file)
        elif path.endswith('.mp3'):
            self.queue.append(path)
        else:
            return

        if not self.queue_task.current_loop:
            self.queue_task.start()


def setup(bot):
    bot.add_cog(Spire(bot, memory))
