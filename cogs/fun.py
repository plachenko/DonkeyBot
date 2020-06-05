import discord
from discord.ext import commands

import datetime
from datetime import date
from random import seed
from random import choice
import time

class FunCog(commands.Cog):

    def __init__(self, client):
        self.client = client

        with open("data/activeUsers.txt", "r") as f:
            self.activeUsers = f.read()
            self.activeUsers = self.activeUsers.split("\n")

        with open("data/lastCoolGuy.txt", "r") as f:
            self.lastCoolGuy = datetime.datetime.strptime(f.read().replace("-",""), "%Y%m%d").date()

        with open("data/combo.txt", "r") as f:
            self.combo = f.read()
    
    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if (before.channel.id == 717886687715262554):
            beforeCount = before.content.split(" ", 1)[0]
            if (not after.content.startswith(beforeCount + " ")):
                await before.author.edit(nick="(" + beforeCount + ") im an idiot")

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
        noon = datetime.datetime.now().replace(hour=12, minute=0, second=0, microsecond=0)
        if now > noon and date.today() > self.lastCoolGuy:
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
        
        if (message.channel.id == 718251019661869156):

            if (member.guild_permissions.manage_messages != True):
                count = int(self.combo)
                nextCountStr = str(count+1)

                if (message.content.startswith(nextCountStr + " ") or (message.content == nextCountStr)):
                    self.combo = count + 1
                    with open("data/combo.txt", "w") as f:
                        f.write(str(self.combo))
                    
                    #Update Roles
                    memberRoles = message.author.roles
                    goodRole = message.guild.get_role(718590952947580950)
                    if (goodRole not in memberRoles):
                        await message.author.add_roles(goodRole)
                    
                elif (not message.author.bot):
                    best = message.channel.topic.split("Best: ", 1)[1]

                    countdownMessage = "<@" + str(message.author.id) + "> broke <#718251019661869156> <:luigisad:406759665058185226>"
                    if (count > int(best)):
                        countdownMessage += " **(NEW BEST: " + str(count) + ")**"
                        await message.channel.edit(topic="Best: " + str(count))

                    #Countdown
                    timer = 10
                    countdown = await message.channel.send(countdownMessage + "\nResetting in " + str(timer) + "...")

                    for i in range(timer):
                        time.sleep(1)
                        await countdown.edit(content=countdownMessage + "\nResetting in " + str(timer) + "...")
                        timer -= 1
                    
                    notifChannel = message.guild.get_channel(718600409652133948) #Lab
                    await notifChannel.send(countdownMessage + "\n> " + message.content)

                    #Update Roles
                    memberRoles = message.author.roles
                    goodRole = message.guild.get_role(718590952947580950)
                    badRole = message.guild.get_role(718590813726179398)

                    if (goodRole in memberRoles):
                        await message.author.remove_roles(goodRole)
                    
                    await message.author.add_roles(badRole)

                    #Delete all messages in channel
                    messagesDeleted = await message.channel.purge(limit=100)
                    while (len(messagesDeleted) != 0):
                        messagesDeleted = await message.channel.purge(limit=100)

                    #Reset
                    with open("data/combo.txt", "w") as f:
                        f.write("0")
                    self.combo = 0
            elif (member.guild_permissions.manage_messages and not message.author.bot):
                await message.delete()
                await message.author.send("You cannot participate in experiment because you bypass slowmode.")

def setup(client):
    client.add_cog(FunCog(client))