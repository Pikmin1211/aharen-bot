import discord
import logging
import json
import os
from discord.ext import commands

logging.basicConfig(level=logging.INFO)

aharen = commands.Bot(command_prefix='aharen ')

config_file = open('config.json')
config = json.load(config_file)
config_file.close()

@aharen.event
async def on_ready():
    print('We have logged in as {0.user}'.format(aharen))

@aharen.event
async def on_command_error(ctx, error):
    await ctx.send('There was an error...')
    await ctx.send('```\n{0}\n```'.format(error))

cwd = os.getcwd()
for root, dirs, files in os.walk(cwd + '\\command'):
    for file in files:
        if file.endswith('.py') and 'repos' not in root and '__init__' not in file:
            try:
                aharen.load_extension(os.path.join(root, file).replace(cwd, '').replace('.py', '').replace('\\', '.')[1:])
            except Exception as e:
                print(e)

aharen.run(config['discord-token'])
