import discord
from discord.ext import tasks, commands
from .Server import Server

import random
import time
import asyncio
import datetime
from datetime import date

class LabCog(commands.Cog, Server):
    def __init__(self, client):
        self.client = client
        self.ratRaceInit() # RATRACE: Initialize
        self.Ticker.start()

        Server.__init__(self)

    @tasks.loop(minutes=10)
    async def Ticker(self):
        if (self.client.get_channel(self.labChannel)):

            await self.ratRaceCheckStart() # RATRACE: Check if it's time to start
            
    @commands.Cog.listener()
    async def on_message(self, message):

        # Get member
        member = message.author

        # Listen to lab channel messages
        if (message.channel.id == self.labChannel):

            # Mods canonically mentally unstable and unreliable.
            if (not member.guild_permissions.manage_messages):

                await self.ratRaceMemberMessage(member, message) # RATRACE: check member message when it's time

    # === START RatRace methods ===
    """
        RATRACE:
        At a random time of day donkey bot will announce a photo oppertunity. 
        The first person that says "cheese" will be able to redeem themselves 
        from the "bad role" if applicable.
    """

    def ratRaceInit(self):
        # Read the last date race took place or write it and reset cheese on instantiation
        self.hasCheese = False
        self.ratRaceGetTime()

    def ratRaceSetTime(self):
        tomorrow = datetime.datetime.now() + datetime.timedelta(days=1)
        randTime = tomorrow.replace(hour=random.randint(0, 23), minute=random.randint(0, 59), second=0, microsecond=0)

        with open("data/lastRat.txt", "r+") as f:
            f.seek(0)
            f.write(str(randTime))
            f.truncate()

            self.ratDate = f.read()

    def ratRaceGetTime(self):
        now = datetime.datetime.now()

        with open("data/lastRat.txt", "r+") as f:
            self.ratDate = f.read()

            # Select a random time of day based on current hour / minute
            randTime = now.replace(hour=random.randint(now.hour, 23), minute=random.randint(now.minute, 59), second=0, microsecond=0)

            # Check if date exists or less than today otherwise write today in the file
            if (self.ratDate == "" or datetime.datetime.strptime(self.ratDate, "%Y-%m-%d %H:%M:%S") < now):
                f.seek(0)
                f.write(str(randTime))
                f.truncate()

    async def ratRaceCheckStart(self):
        now = datetime.datetime.now()
        ratDate = datetime.datetime.strptime(self.ratDate, "%Y-%m-%d %H:%M:%S")

        # Start the rat race.
        if (ratDate <= now and self.hasCheese == False):
            await self.client.get_channel(self.labChannel).send('Taking a photo, say **cheese**!')
            self.hasCheese = True

    async def ratRaceMemberMessage(self, member, message):
        # Check if a member wrote the secret phrase
        if (message.content.lower() == "cheese" and self.hasCheese):

            # Announce the lucky person and reset
            msg = "<@" + str(member.id) + "> got the cheese!"
            await self.client.get_channel(self.labChannel).send(msg)
    
            self.hasCheese = False
            self.ratRaceSetTime()
            
            # Give good role to bad rolers
            if (message.guild.get_role(self.badRole) in member.roles):
                await member.remove_roles(message.guild.get_role(self.badRole))
                await member.add_roles(message.guild.get_role(self.goodRole))

    # === END RatRace methods ===

def setup(client):
    client.add_cog(LabCog(client))
