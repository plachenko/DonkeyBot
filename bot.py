import os
import sys, traceback
from dotenv import load_dotenv
load_dotenv() #Load .env file, contains bot secret

import discord
from discord.ext import commands

client = commands.Bot(command_prefix=commands.when_mentioned, help_command=None)

<<<<<<< HEAD
initial_extensions = ['cogs.basic','cogs.experiment','cogs.rob'] #Add cog filenames here
=======
initial_extensions = ['cogs.basic','cogs.fun','cogs.experiment','cogs.tasks','cogs.rob'] #Add cog filenames here
>>>>>>> upstream/master

if __name__ == '__main__':
    for extension in initial_extensions:
        client.load_extension(extension)

@client.event
async def on_ready():
    print("Logged in")
    game = discord.Game("ALL HAIL ROB") #Never ever change this because it is the truth
    await client.change_presence(activity=game)

client.run(os.getenv("BOT_TOKEN"), reconnect=True)