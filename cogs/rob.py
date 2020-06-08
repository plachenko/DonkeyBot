import discord
from discord.ext import commands
from .Server import Server

from random import seed
from random import choice

def isRob(ctx, robID):
    if (ctx.message.author.id == robID):
        return True
    return False

class RobCog(commands.Cog, Server):
    def __init__(self, client):
        self.client = client
        Server.__init__(self)

    @commands.command()
    async def raffle(self, ctx):
        
        if isRob(ctx, self.robID):
            await ctx.message.delete() #Delete command usage

            #Get active users
            with open("data/activeUsers.txt", "r") as f:
                activeUsers = f.read()
                activeUsers = activeUsers.split("\n")
            
            #Raffle
            found = False
            while (not found):
                selection = choice(activeUsers)
                if ctx.guild.get_member(int(selection)) != None:
                    found = True

            await ctx.guild.get_member(int(selection)).add_roles(ctx.guild.get_role(self.coolGuyRole))
            await ctx.send("<@" + selection + "> won the cool guy raffle")

def setup(client):
    client.add_cog(RobCog(client))