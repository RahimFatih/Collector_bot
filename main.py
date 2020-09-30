import asyncio
import discord
from discord.ext import commands
import json
import os


def get_prefix(ctx, message):
    with open('./config/prefixes.json', 'r') as f:
        prefixes = json.load(f)

    return prefixes[str(message.guild.id)]

bot = commands.Bot(command_prefix = get_prefix)

def read_token():
    with open(f'./token.txt', 'r') as f:
        lines = f.readlines()
        return lines[0].strip()

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.command(hidden=True)
@commands.is_owner()
async def reload(ctx, extension):

    if extension == 'all':

        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                try:
                    bot.unload_extension(f'cogs.{filename[:-3]}')
                except commands.ExtensionNotLoaded:
                    pass
                bot.load_extension(f'cogs.{filename[:-3]}')
                print(f'Reloaded {filename}')
        print(f'Reloaded all')
    else:
        bot.unload_extension(f'cogs.{extension}')
        bot.load_extension(f'cogs.{extension}')
        print(f'Reloaded {extension}')

#execution part

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')
        print(f'Loaded {filename}')

token = read_token()

bot.run(token)