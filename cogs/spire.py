import discord
import os

from discord.ext import commands, tasks

class Spire(commands.Cog, name='Spire', command_attrs=dict(hidden=False)):
    def __init__(self, bot):
        self.bot = bot
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
    async def harken(self, ctx):
        if not ctx.author.voice: return
        client = ctx.guild.voice_client
        if not client:
            client = await ctx.author.voice.channel.connect()
        self.voice_client = client

    @commands.command(name='forget', brief='Removes the bot from a voice channel.')
    @commands.is_owner()
    async def forget(self, ctx):
        client = ctx.guild.voice_client
        if not client:
            return
        await client.disconnect()
        self.queue = []
        await self.bot.change_presence(activity=None)

    @commands.command(name='sing', brief='Plays music with integrated queue.')
    @commands.is_owner()
    async def sing(self, ctx, *, path):
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
    bot.add_cog(Spire(bot))
