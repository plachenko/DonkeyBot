import discord
from discord.ext import commands


class FunCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    # @commands.command()
    # @commands.guild_only()
    # async def test(self, ctx):
    #     await ctx.send("Yo")

def setup(client):
    client.add_cog(FunCog(client))