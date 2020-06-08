import discord
from discord.ext import commands
from .Server import Server

import datetime

class BasicCog(commands.Cog, Server):
    def __init__(self, client):
        self.client = client
        self.delays = {} #Keep track of last issued commands

        Server.__init__(self)
    
    #Sends the repo to requested channel
    @commands.command()
    async def repo(self, ctx):
        
        #Get time since last command issued
        if ("repo" not in self.delays):
            self.delays["repo"] = datetime.datetime.now()
        now = datetime.datetime.now()
        secondsSince = (now - self.delays["repo"]).total_seconds()
        
        if (secondsSince > 60 or secondsSince == 0.0):
            await ctx.channel.send("https://github.com/okj/DonkeyBot")
            self.delays["repo"] = now

def setup(client):
    client.add_cog(BasicCog(client))