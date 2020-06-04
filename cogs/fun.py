import discord
from discord.ext import commands


class FunCog(commands.Cog):
    activeUsers = []

    def __init__(self, client):
        self.client = client
        with open("data/activeUsers.txt", "r") as f:
            self.activeUsers = f.read()
            self.activeUsers = self.activeUsers.split("\n")

    @commands.Cog.listener()
    async def on_message(self, message):
        activeUsers = self.activeUsers
        member = message.author

        if str(member.id) not in activeUsers and (member.guild_permissions.manage_messages == False and member.bot == False):
            activeUsers.append(str(member.id))
            with open("data/activeUsers.txt", "a") as f:
                f.write(str(member.id) + "\n")

def setup(client):
    client.add_cog(FunCog(client))