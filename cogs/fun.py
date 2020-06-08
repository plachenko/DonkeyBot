import discord
from discord.ext import commands
from .Server import Server

import datetime
from datetime import date
from random import seed
from random import choice
import time

class FunCog(commands.Cog, Server):

    def __init__(self, client):
        self.client = client
        self.noon = datetime.datetime.now().replace(hour=12, minute=0, second=0, microsecond=0)

        #List of active user ids
        with open("data/activeUsers.txt", "r") as f:
            self.activeUsers = f.read()
            self.activeUsers = self.activeUsers.split("\n")

        #Date object of the last cool guy raffle
        with open("data/lastCoolGuy.txt", "r") as f:
            self.lastCoolGuy = datetime.datetime.strptime(f.read().replace("-",""), "%Y%m%d").date()

        Server.__init__(self)

    @commands.Cog.listener()
    async def on_message(self, message):
        
        member = message.author
        
        #Add non-staff to list of active users
        if ((str(member.id) not in self.activeUsers) and (not member.guild_permissions.manage_messages and not member.bot)):
            self.activeUsers.append(str(member.id))
            with open("data/activeUsers.txt", "a") as f:
                f.write(str(member.id) + "\n")
        
        #Cool guy raffle once a day
        now = datetime.datetime.now()
        if (now > self.noon and (date.today() > self.lastCoolGuy)):

            #Set date
            with open("data/lastCoolGuy.txt", "w") as f:
                f.write(str(date.today()))
            self.lastCoolGuy = date.today()

            coolGuyRole = message.guild.get_role(self.coolGuyRole)

            #Remove last cool guy(s)
            coolGuys = coolGuyRole.members
            for coolGuy in coolGuys:
                await coolGuy.remove_roles(coolGuyRole)

            #New cool guy
            found = False
            while (not found):
                selection = choice(self.activeUsers)
                if message.guild.get_member(int(selection)) != None:
                    found = True
            winner = message.guild.get_member(int(selection))
            await winner.add_roles(coolGuyRole)
            
            general = message.guild.get_channel(self.generalChannel)
            await general.send("<@" + selection + "> won the cool guy raffle! ")

            #Reset active users
            with open("data/activeUsers.txt", "w") as f:
                f.write("")
            self.activeUsers = []

def setup(client):
    client.add_cog(FunCog(client))