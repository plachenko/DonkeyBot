import discord
from discord.ext import commands

import datetime
from datetime import date
from random import seed
from random import choice

class FunCog(commands.Cog):
    activeUsers = []
    noon = None
    lastCoolGuy = None

    def __init__(self, client):
        self.client = client
        with open("data/activeUsers.txt", "r") as f:
            self.activeUsers = f.read()
            self.activeUsers = self.activeUsers.split("\n")

        self.noon = datetime.datetime.now().replace(hour=12, minute=0, second=0, microsecond=0)
        with open("data/lastCoolGuy.txt", "r") as f:
            self.lastCoolGuy = datetime.datetime.strptime(f.read().replace("-",""), "%Y%m%d").date()

    @commands.Cog.listener()
    async def on_message(self, message):
        activeUsers = self.activeUsers
        member = message.author

        try:
            if str(member.id) not in activeUsers and (member.guild_permissions.manage_messages == False and member.bot == False):
                activeUsers.append(str(member.id))
                with open("data/activeUsers.txt", "a") as f:
                    f.write(str(member.id) + "\n")
        except: #No guild permissions
            pass
        
        now = datetime.datetime.now()
        if now > self.noon and date.today() > self.lastCoolGuy:
            with open("data/lastCoolGuy.txt", "w") as f:
                f.write(str(date.today()))
            self.lastCoolGuy = date.today()

            coolGuyRole = message.guild.get_role(717900752583917598)

            coolGuys = coolGuyRole.members #Get cool guys
            for coolGuy in coolGuys:
                await coolGuy.remove_roles(coolGuyRole)

            #New cool guy
            found = False
            while (not found):
                selection = choice(self.activeUsers)
                try:
                    if message.guild.get_member(int(selection)) != None:
                        found = True
                except:
                    pass
            
            general = message.guild.get_channel(284028535155326976)
            await general.send("<@" + selection + "> won the cool guy raffle! ")

            winner = message.guild.get_member(int(selection))
            await winner.add_roles(coolGuyRole)
            with open("data/activeUsers.txt", "w") as f:
                f.write("")
            self.activeUsers = []


def setup(client):
    client.add_cog(FunCog(client))