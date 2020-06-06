import discord
from discord.ext import commands

from random import seed
from random import choice

def isRob(ctx):
    if (ctx.message.author.id == 151486808247500801):
        return True
    return False

class RobCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def raffle(self, ctx):
        if isRob(ctx):
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
            await ctx.send("<@" + selection + "> won the cool guy raffle")

def setup(client):
    client.add_cog(RobCog(client))