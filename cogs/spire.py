import asyncio
import discord
import json
import mutagen
import os

from discord.ext import commands, tasks
from bot import memory
from mutagen.easyid3 import EasyID3


class Spire(commands.Cog, name='Spire', command_attrs=dict(hidden=False)):
    def __init__(self, bot, memory):
        self.bot = bot
        self.memory = memory
        self.queue = []

    async def player(self, op: str='play'):
        if op == 'play':
            if not self.voice_client.is_playing():
                try:
                    source = await discord.FFmpegOpusAudio.from_probe(self.queue[0], method='native', **dict(before_options='-stats'))
                    self.voice_client.play(source, after=self.next)
                except IndexError:
                    return
        elif op == 'pause':
            if self.voice_client.is_paused(): return
            return self.voice_client.pause()
        elif op == 'resume':
            if not self.voice_client.is_paused(): return
            return self.voice_client.resume()
        elif op == 'skip':
            if not self.voice_client.is_playing(): return
            self.voice_client.stop()

    def next(self, error=discord.ClientException):
        try:
            self.queue.pop(0)
        except IndexError:
            return
        future = asyncio.run_coroutine_threadsafe(self.player(op='play'), self.bot.loop)
        try:
            future.result()
        except:
            pass

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
        del self.queue[:]
        self.queue = []

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
            for f in os.listdir(path):
                if not f.endswith('.mp3'): continue
                self.queue.append(path+f)
        elif path.endswith('.mp3'):
            return self.queue.append(path)
        else:
            return

        if not self.voice_client.is_playing():
            await self.player(op="play")

    @commands.command(name='show', brief='Shows the queue.')
    @commands.is_owner()
    async def show(self, ctx):
        print(EasyID3.valid_keys.keys())
        if not self.queue: return await ctx.send('Queue is empty.')

        string = ''
        for pos, item in enumerate(self.queue):
            try:
                song = EasyID3(item)
            except mutagen.id3.ID3NoHeaderError:
                song = mutagen.File(item, easy=True)
            except mutagen.MutagenError:
                continue
            if pos != 0:
                string += f'{str(pos).zfill(2)}: {song["albumartist"][0]} - {song["title"][0]}\n'
            else:
                string += f'np: {song["albumartist"][0]} - {song["title"][0]}\n'
        return await ctx.send(f'Queue:\n```{string}```')

    @commands.command(name='pause', brief='Pauses the current song.')
    @commands.is_owner()
    async def pause(self, ctx):
        await self.player(op='pause')

    @commands.command(name='resume', brief='Resumes the current paused song.')
    @commands.is_owner()
    async def resume(self, ctx):
        await self.player(op='resume')

    @commands.command(name='skip', brief='Skips the current song.')
    @commands.is_owner()
    async def skip(self, ctx):
        await self.player(op='skip')

    @commands.command(name='remove', brief='Removes a song from the queue.')
    @commands.is_owner()
    async def remove(self, ctx, index: int):
        if index < 1:
            return await ctx.send('You cannot remove the current song.')
        if index > len(self.queue)-1:
            return await ctx.send('Invalid queue position.')
        self.queue.pop(index)
        return await ctx.send(f'Removed song in position {index}.')


def setup(bot):
    bot.add_cog(Spire(bot, memory))
