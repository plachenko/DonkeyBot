import discord
from discord.ext import commands
from .Server import Server

from tinydb import TinyDB, where
from tinydb.operations import set

import re

class ExperimentCog(commands.Cog, Server):
    def __init__(self, client):
        self.client = client
        self.events = TinyDB('database/events.json')
        self.users = TinyDB('database/users.json')

        Server.__init__(self)

        #Experiment channel combo
        self.combo = self.events.get(where('name') == 'experiment')['combo']

    @commands.Cog.listener()
    async def on_member_join(self, member):

        #Give experiment roles
        server = self.client.get_guild(self.server)

        roles = [] if self.users.get(where('id') == member.id) is None else self.users.get(where('id') == member.id)['roles']

        for role in roles:
            await member.add_roles(server.get_role(role))

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):

        if (before.channel.id == self.experimentChannel):

            #Change nickname if someone removes their combo in an edit
            beforeCount = re.search(r'\d+', before.content).group()
            if (beforeCount not in after.content):
                await before.author.edit(nick="(" + beforeCount + ") im an idiot")
    
    @commands.Cog.listener()
    async def on_message_delete(self, message):
        
        member = message.author

        #Punish griefers
        if ((message.channel.id == self.experimentChannel) and (not member.bot and not member.guild_permissions.manage_messages)): #User was not staff or bot
            
            regEx = re.search(r'\d+', message.content)
            firstInt = 0 if regEx is None else regEx.group()
            
            print(message.channel.last_message_id)

            await message.channel.send("> " + firstInt + "\n<@" + str(member.id) + ">")
            
            #Remove good role, add bad role
            if (message.guild.get_role(self.goodRole) in member.roles):
                await member.remove_roles(message.guild.get_role(self.goodRole))
            await member.add_roles(message.guild.get_role(self.badRole))
            self.users.upsert({ 'id': member.id, 'roles': [ self.badRole ] }, where('id') == member.id)
    
    @commands.Cog.listener()
    async def on_message(self, message):

        member = message.author

        if (message.channel.id == self.experimentChannel):
    
            #Only non-staff can participate in the experiment!
            if (not member.guild_permissions.manage_messages):

                count = int(self.combo)
                nextCountStr = str(count+1) #Expected next combo

                #Successful combo
                regEx = re.search(r'\d+', message.content)
                firstInt = 0 if regEx is None else regEx.group()
                if (firstInt == nextCountStr):

                    self.combo = count + 1
                    self.events.update(set('combo', str(self.combo)), where('name') == 'experiment')
                    
                    #Give good role to first time participants
                    if (message.guild.get_role(self.goodRole) not in member.roles):
                        await member.add_roles(message.guild.get_role(self.goodRole))
                        self.users.upsert({ 'id': member.id, 'roles': [ self.goodRole ] }, where('id') == member.id)
                
                #Unsuccessful combo
                elif (not member.bot):

                    best = message.channel.topic.split("Best: ", 1)[1] #Get record from topic

                    countdownMessage = "<@" + str(member.id) + "> broke <#718251019661869156> <:luigisad:406759665058185226>"
                    if (count > int(best)): #If new record, append to message
                        countdownMessage += " **(NEW BEST: " + str(count) + ")**"
                        await message.channel.edit(topic="Best: " + str(count))

                    notifChannel = message.guild.get_channel(self.labChannel)
                    await notifChannel.send(countdownMessage + "\n> " + message.content)

                    #Remove good role, add bad role
                    if (message.guild.get_role(self.goodRole) in member.roles):
                        await member.remove_roles(message.guild.get_role(self.goodRole))
                    await member.add_roles(message.guild.get_role(self.badRole))
                    self.users.upsert({ 'id': member.id, 'roles': [ self.badRole ] }, where('id') == member.id)

                    #Delete all messages in the channel
                    messagesDeleted = await message.channel.purge(limit=100)
                    while (len(messagesDeleted) != 0):
                        messagesDeleted = await message.channel.purge(limit=100)

                    #Reset combo
                    self.combo = 0
                    self.events.update(set('combo', str(self.combo)), where('name') == 'experiment')
            
            #Mods gay
            elif (member.guild_permissions.manage_messages and not member.bot):
                await message.delete()
                try:
                    await member.send("You cannot participate in experiment because you bypass slowmode.")
                except:
                    pass #Cannot send message to this user

def setup(client):
    client.add_cog(ExperimentCog(client))
