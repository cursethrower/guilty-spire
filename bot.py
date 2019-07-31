import discord
import json

from discord.ext import commands

# get data
with open('./config/config.json') as f:
    config = json.load(f)
token = config["token"]

with open('./config/memory.json') as f:
    memory = json.load(f)

bot = commands.Bot(command_prefix='-')
cogs = ['cogs.spire',
        'cogs.memory',
        'cogs.owner',
        'cogs.event_handler'
        ]

if __name__ == '__main__':
    for cog in cogs:
        try:
            bot.load_extension(cog)
        except Exception as error:
            print(f'cog {cog} cannot be loaded. [{error}]')

    bot.run(token)
