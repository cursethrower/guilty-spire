import discord
import json
import os

from discord.ext import commands

# get data
with open('./config/config.json') as f:
    config = json.load(f)
token = config["token"]

if not os.path.exists('./config/memory.json'):
    print('doesn\'t exist')
    memory = dict()
    memory["spellbook"] = dict()
    with open('./config/memory.json', 'w') as f:
        json.dump(memory, f, indent=4)

with open('./config/memory.json') as f:
    memory = json.load(f)
    if not memory.get("spellbook", None):
        memory["spellbook"] = dict()

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
