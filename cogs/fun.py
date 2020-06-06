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
        self.noon = datetime.datetime.now().replace(hour=12, minute=0, second=0, microsecond=0)

        #List of active user ids
        with open("data/activeUsers.txt", "r") as f:
            self.activeUsers = f.read()
            self.activeUsers = self.activeUsers.split("\n")

        #Date object of the last cool guy raffle
        with open("data/lastCoolGuy.txt", "r") as f:
            self.lastCoolGuy = datetime.datetime.strptime(f.read().replace("-",""), "%Y%m%d").date()

        #Experiment channel combo
        with open("data/combo.txt", "r") as f:
            self.combo = f.read()
    
    @commands.Cog.listener()
    async def on_message_edit(self, before, after):

        if (before.channel.id == 717886687715262554): #Experiment channel

            #Change nickname if someone removes their combo in an edit
            beforeCount = before.content.split(" ", 1)[0] 
            if (not after.content.startswith(beforeCount + " ")):
                await before.author.edit(nick="(" + beforeCount + ") im an idiot")

    @commands.Cog.listener()
    async def on_message(self, message):

        member = message.author
        
        #Add non-staff to list of active users
        if ( str(member.id) not in self.activeUsers and (not member.guild_permissions.manage_messages and not member.bot) ):
            self.activeUsers.append(str(member.id))
            with open("data/activeUsers.txt", "a") as f:
                f.write(str(member.id) + "\n")
        
        #Raffle once a day
        now = datetime.datetime.now()
        if (now > self.noon and (date.today() > self.lastCoolGuy)):

            #Set date
            with open("data/lastCoolGuy.txt", "w") as f:
                f.write(str(date.today()))
            self.lastCoolGuy = date.today()

            coolGuyRole = message.guild.get_role(717900752583917598)

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
            
            general = message.guild.get_channel(284028535155326976)
            await general.send("<@" + selection + "> won the cool guy raffle! ")

            #Reset active users
            with open("data/activeUsers.txt", "w") as f:
                f.write("")
            self.activeUsers = []
        
        if (message.channel.id == 718251019661869156): #Experiment channel

            #Only non-staff can participate in the experiment!
            if (not member.guild_permissions.manage_messages):

                count = int(self.combo)
                nextCountStr = str(count+1) #Expected next combo

                #Successful combo
                if (message.content.startswith(nextCountStr + " ") or (message.content == nextCountStr)):

                    self.combo = count + 1
                    with open("data/combo.txt", "w") as f:
                        f.write(str(self.combo))
                    
                    #Give good role to first time participants
                    goodRole = message.guild.get_role(718590952947580950)
                    if (goodRole not in member.roles):
                        await member.add_roles(goodRole)
                
                #Unsuccessful combo
                elif (not member.bot):
                    best = message.channel.topic.split("Best: ", 1)[1] #Get record from topic

                    countdownMessage = "<@" + str(member.id) + "> broke <#718251019661869156> <:luigisad:406759665058185226>"
                    if (count > int(best)): #If new record, append to message
                        countdownMessage += " **(NEW BEST: " + str(count) + ")**"
                        await message.channel.edit(topic="Best: " + str(count))

                    #Countdown
                    timer = 10
                    countdown = await message.channel.send(countdownMessage + "\nResetting in " + str(timer) + "...")

                    for i in range(timer):
                        time.sleep(1)
                        await countdown.edit(content=countdownMessage + "\nResetting in " + str(timer) + "...")
                        timer -= 1
                    
                    notifChannel = message.guild.get_channel(718600409652133948) #currently set to the-lab
                    await notifChannel.send(countdownMessage + "\n> " + message.content)

                    #Update Roles
                    goodRole = message.guild.get_role(718590952947580950)
                    badRole = message.guild.get_role(718590813726179398)
                    
                    if (goodRole in member.roles):
                        await member.remove_roles(goodRole)
                    await member.add_roles(badRole)

                    #Delete all messages in the channel
                    messagesDeleted = await message.channel.purge(limit=100)
                    while (len(messagesDeleted) != 0):
                        messagesDeleted = await message.channel.purge(limit=100)

                    #Reset combo
                    with open("data/combo.txt", "w") as f:
                        f.write("0")
                    self.combo = 0
            
            #Mods gay
            elif (member.guild_permissions.manage_messages and not member.bot):
                await message.delete()
                await member.send("You cannot participate in experiment because you bypass slowmode.")

def setup(client):
    client.add_cog(FunCog(client))