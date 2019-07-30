import discord
import os

from discord.ext import commands, tasks
from bot import memory


class Sanctum(commands.Cog, name='Sanctum', command_attrs=dict(hidden=False)):
    def __init__(self, bot, memory):
        self.bot = bot
        self.memory = memory
        self.queue = []

    @tasks.loop(seconds=2.0, count=None)
    async def queue_task(self):
        if not self.voice_client.is_playing():
            try:
                track = self.queue.pop(0)
                self.voice_client.play(discord.FFmpegPCMAudio(track))
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
            await ctx.send('You are not in a voice channel.')
            return
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

    @commands.command(name='remember', brief='Sets a default voice channel to join.')
    @commands.is_owner()
    async def remember(self, ctx):
        if not ctx.author.voice:
            await ctx.send('You are not in a voice channel.')
            return
        self.memory["remember"] = str(ctx.author.voice.channel.id)
        await ctx.send('I remember.')

    @commands.command(name='forget', brief='Removes the default voice channel to join.')
    @commands.is_owner()
    async def forget(self, ctx):
        self.memory["remember"] = 0
        await ctx.send('I have forgotten.')

    @commands.command(name='sing', brief='Plays music with integrated queue.')
    @commands.is_owner()
    async def sing(self, ctx, *, path):
        if not ctx.guild.voice_client and self.memory["remember"] != "none":
            channel = await commands.VoiceChannelConverter().convert(ctx, self.memory["remember"])
            await ctx.invoke(self.bot.get_command("harken"), channel)
        if not path.endswith('.mp3'):
            if not path.endswith('/'): path = f'{path}+/'
            files = os.listdir(path)
            for file in files:
                self.queue.append(path+file)
        elif path.endswith('.mp3'):
            self.queue.append(path)
        else:
            return
        
        self.queue_task.start()


def setup(bot):
    bot.add_cog(Sanctum(bot, memory))
