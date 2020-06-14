import discord
from discord.ext import commands
from .Server import Server

import datetime
import os
import sys

class BasicCog(commands.Cog, Server):
    def __init__(self, client):
        self.client = client
        Server.__init__(self)

        self.delays = {} #Keep track of last issued commands

    @commands.command()
    async def setup(self, ctx):
        if (ctx.message.author.id == ctx.guild.owner.id): #Only test server owner can run setup
            
            updated = "Setup Complete:```" #Updated variables

            with open("cogs/Server.py", "r+") as f:
                ServerFile = f.read()

                server = Server()
                for ID in server.__dict__.keys(): #Iterate through defined variables
                    
                    #Get the current ID value
                    oldValue = server.__dict__[ID]

                    if (ID == "server"):
                        newValue = ctx.guild.id
                    elif (ID == "robID"):
                        newValue = ctx.message.author.id

                    elif ("Role" in ID):
                        for role in ctx.guild.roles:
                            if (ID.split("Role", 1)[0].lower() in role.name.replace(" ", "").lower()):
                                newValue = role.id
                                break

                    elif ("Channel" in ID):
                        for channel in ctx.guild.channels:
                            if (ID.split("Channel", 1)[0].lower() in channel.name.replace(" ", "").lower()):
                                newValue = channel.id
                                break
                    else:
                        newValue = "'NOT FOUND'" #This will occur if variables are named incorrectly in Server.py
                    
                    #Update
                    ServerFile = ServerFile.replace(str(oldValue), str(newValue))
                    updated += "\n" + ID + " = " + str(newValue)
                
                #Write to Server.py
                f.seek(0)
                f.write(ServerFile)
                f.truncate()
            
            await ctx.channel.send(updated + "```**(Restart to apply changes)**")

    #Sends the repo to requested channel
    @commands.command()
    async def repo(self, ctx):

        now = datetime.datetime.now()
        
        #Get time since last command issued
        if ("repo" not in self.delays):
            self.delays["repo"] = now
        secondsSince = (now - self.delays["repo"]).total_seconds()
        
        if (secondsSince > 60 or secondsSince == 0.0):
            await ctx.channel.send("https://github.com/okj/DonkeyBot")
            self.delays["repo"] = now

def setup(client):
    client.add_cog(BasicCog(client))