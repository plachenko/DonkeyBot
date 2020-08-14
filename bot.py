import os
import sys, traceback
from dotenv import load_dotenv
load_dotenv() #Load .env file, contains bot secret

import discord
from discord.ext import commands

client = commands.Bot(command_prefix=commands.when_mentioned_or('>'), help_command=None)

initial_extensions = ['cogs.mod', 'cogs.basic','cogs.fun','cogs.experiment','cogs.rob','cogs.lab', 'cogs.minecraft'] #Add cog filenames here

@client.event
async def on_ready():
    print("Logged in")
    presence = discord.Activity(type=discord.ActivityType.watching, name="ASTRO alts")
    await client.change_presence(activity=presence)

    if __name__ == '__main__':
        for extension in initial_extensions:
            client.load_extension(extension)

client.run(os.getenv("BOT_TOKEN"), reconnect=True)