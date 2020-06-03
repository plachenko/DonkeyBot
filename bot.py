import os
import sys, traceback
from dotenv import load_dotenv
load_dotenv()

import discord
from discord.ext import commands

client = commands.Bot(command_prefix=commands.when_mentioned, help_command=None)

initial_extensions = ['cogs.fun']

if __name__ == '__main__':
    for extension in initial_extensions:
        client.load_extension(extension)

@client.event
async def on_ready():
    print("Logged in")
    game = discord.Game("ALL HAIL ROB")
    await client.change_presence(activity=game)

client.run(os.getenv("BOT_TOKEN"), reconnect=True)