import discord
from discord.ext import tasks, commands
from .Server import Server

from tinydb import TinyDB, where
from tinydb.operations import set


class MinecraftCog(commands.Cog, Server):
    def __init__(self, client):
        self.client = client
        self.minecraft = TinyDB('database/minecraft.json')
        self.whitelistTXT = r"PATH_TO_WHITELIST"

        Server.__init__(self)

    @commands.command()
    async def whitelist(self, ctx, username):
        message = ctx.message
        member = message.author
        minecraftChannel = message.guild.get_channel(self.minecraftChannel)

        await message.delete()

        if (message.guild.get_role(self.regularRole) in member.roles):

            user = self.minecraft.get(where('id') == member.id)
            
            self.minecraft.upsert({
                'id': member.id,
                'username': username
            }, where('id') == member.id)

            if (user != None):
                
                if (user["username"] != username):
                    #Find and replace usernames
                    with open(self.whitelistTXT, "r+") as f:
                        whitelist = f.read()
                        whitelist = whitelist.replace(user["username"], username)
                        
                        f.seek(0)
                        f.write(whitelist)
                        f.truncate()
                
                #Send confirmation in DMs or MC channel
                try:
                    await member.send("Whitelisted `" + username + "` (replaced `" + user["username"] + "`)")
                except:
                    await minecraftChannel.send("<@" + str(member.id) + "> changed your whitelisted account. Allow direct messages from server members in your privacy settings and use `@Donkey ip` to receive the IP and server info :confused:")

            else:
                #Write username to file
                with open(self.whitelistTXT, "a") as f:
                    f.write(username + "\n")

                #Send confirmation in DMs or MC channel
                try:
                    await member.send("Whitelisted `" + username + "`")
                    await member.send("**IMPORTANT PLEASE READ:** *The whitelist updates automatically every 10 minutes*. Please be patient and do not ask anyone to whitelist you!\n\nThis server is __anarchy__ meaning that it is __NOT__ moderated. Do not @ anyone in the Discord asking for help because you will not get any. Keep discussion in the #minecraft channel and have fun :thumbsup:\n\n**Server IP:** 10.101.10\n**Version:** 1.16.2")

                except:
                    await minecraftChannel.send("<@" + str(member.id) + "> Allow direct messages from server members in your privacy settings and use `@Donkey ip` to receive the IP and server info :confused:")

        else:
            await minecraftChannel.send("Sorry <@" + str(member.id) + "> but you do not have **Regular** role :frowning:")

    #Sends IP if whitelisted
    @commands.command()
    async def ip(self, ctx):
        member = ctx.message.author
        user = self.minecraft.get(where('id') == member.id)
        minecraftChannel = ctx.message.guild.get_channel(self.minecraftChannel)

        await ctx.message.delete()
        if (user != None):
            try:
                await member.send("**IMPORTANT PLEASE READ:** *The whitelist updates automatically every 10 minutes*. Please be patient and do not ask anyone to whitelist you!\n\nThis server is __anarchy__ meaning that it is __NOT__ moderated. Do not @ anyone in the Discord asking for help because you will not get any. Keep discussion in the #minecraft channel and have fun :thumbsup:\n\n**Server IP:** 10.101.10\n**Version:** 1.16.2")
            except:
                await minecraftChannel.send("<@" + str(member.id) + "> Allow direct messages from server members in your privacy settings :confused:")
        else:
            try:
                await member.send("You must be whitelisted to use this command. Use `@Donkey whitelist username` first.")
            except:
                await minecraftChannel.send("<@" + str(member.id) + "> you must be whitelisted to use this command. Use `@Donkey whitelist username` first. (Also, allow direct messages from server members in your privacy settings)")
    
    #Rob only command to search DB
    @commands.command()
    async def whois(self, ctx, username):
        if (ctx.message.author.id == self.robID):
            await ctx.message.delete()

            user = self.minecraft.get(where('username') == username)
            if (user != None):
                await ctx.message.channel.send("`" + username + "` is <@" + str(user["id"]) + ">")
            else:
                await ctx.message.channel.send("`" + username + "` was not found in the whitelist")

def setup(client):
    client.add_cog(MinecraftCog(client))