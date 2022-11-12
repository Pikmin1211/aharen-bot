import discord
from discord import app_commands

@app_commands.command(
    name = 'ping',
    description = 'replies pong'
)
async def ping(ctx):
    await ctx.response.send_message('Pong!')

async def setup(aharen):
	aharen.tree.add_command(ping)
