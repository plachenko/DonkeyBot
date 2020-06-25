import discord
from discord.ext import commands
from .Server import Server

from tinydb import TinyDB, where
from tinydb.operations import set

from random import seed
from random import choice

class RobCog(commands.Cog, Server):
    def __init__(self, client):
        self.client = client
        self.events = TinyDB('database/events.json')
        self.commands = TinyDB('database/commands.json')

        Server.__init__(self)
    
    async def isRob(ctx):
        if (ctx.message.author.id == 151486808247500801): #  rob#1234 ID
            await ctx.message.delete() #Delete command usage
            return True
        return False

    @commands.command()
    @commands.check(isRob)
    async def addcom(self, ctx, use, *, args):

        self.commands.upsert({
            'use': use,
            'resp': args
        }, where('use') == use)

        await ctx.message.channel.send("Added command `" + use + "`\n**Response:** " + args)
    
    @commands.command()
    @commands.check(isRob)
    async def delcom(self, ctx, use):

        removed = self.commands.remove(where('use') == use)

        if (len(removed) > 0):
            await ctx.message.channel.send("Deleted command `" + use + "`")
        else:
            await ctx.message.channel.send("No command found `" + use + "`")

    @commands.command()
    @commands.check(isRob)
    async def raffle(self, ctx):
        message = ctx.message

        #Get active users
        self.activeUsers = self.events.get(where('name') == 'coolguy')['activeUsers']
        
        #Raffle
        found = False
        while (not found):
            selection = choice(self.activeUsers)
            if message.guild.get_member(int(selection)) != None:
                found = True

        winner = message.guild.get_member(int(selection))
        await winner.add_roles(message.guild.get_role(self.coolGuyRole))
        
        general = message.guild.get_channel(self.generalChannel)
        await general.send("<@" + selection + "> won the cool guy raffle! ")

def setup(client):
    client.add_cog(RobCog(client))