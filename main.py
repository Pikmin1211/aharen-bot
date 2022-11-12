import discord
import json
import os
from discord import app_commands
from discord.ext.commands import Bot

async def load_extensions(aharen):
    cwd = os.getcwd()
    for root, dirs, files in os.walk(cwd + '/Command'):
        for file in files:
            if file.endswith('.py') and '__init__' not in file:
                try:
                    await aharen.load_extension(os.path.join(root, file).replace(cwd, '').replace('.py', '').replace('/', '.')[1:])
                except Exception as e:
                    print(e)

intents = discord.Intents.default()
aharen = Bot(command_prefix='.', intents=intents)

@aharen.event
async def on_ready():
    await load_extensions(aharen)
    await aharen.tree.sync()
    print(f'We have logged in as {aharen.user}')

@aharen.event
async def on_command_error(ctx, error):
    await ctx.send('There was an error...')
    await ctx.send('```\n{0}\n```'.format(error))

config_file = open('config.json')
config = json.load(config_file)
config_file.close()

aharen.run(config['discord-token'])
