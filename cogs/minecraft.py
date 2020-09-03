import discord
from discord.ext import tasks, commands
from .Server import Server

from tinydb import TinyDB, where
from tinydb.operations import set
import json
from ftplib import FTP_TLS
import requests
import os

class MinecraftCog(commands.Cog, Server):
    def __init__(self, client):
        self.client = client
        self.minecraft = TinyDB('database/minecraft.json')
        self.whitelistJSON = 'database/whitelist.json'

        Server.__init__(self)
    
    def whitelistUpdate(self):
        ftp = FTP_TLS()
        #ftp.set_debuglevel(2)
        ftp.connect(os.getenv("FTP_IP"), int(os.getenv("FTP_PORT")))
        ftp.login(os.getenv("FTP_LOGIN"), os.getenv("FTP_PASSWORD"))
        whitelist = open(self.whitelistJSON, 'rb')
        ftp.storlines('STOR whitelist.json', whitelist)
        ftp.quit()
        return
    
    def getUUID(self, username):
        x = requests.get('https://api.mojang.com/users/profiles/minecraft/' + username)
        if (x.status_code == 200):
            resp = x.json()["id"]
            uuid = resp[:8] + "-" + resp[8:12] + "-" + resp[12:16] + "-" + resp[16:20] + "-" + resp[20:]
            return uuid
        else:
            return False

    @commands.command()
    async def whitelist(self, ctx, username):
        message = ctx.message
        member = message.author
        minecraftChannel = message.guild.get_channel(self.minecraftChannel)

        await message.delete()

        if (message.guild.get_role(self.regularRole) in member.roles):

            user = self.minecraft.get(where('id') == member.id)
            uuid = self.getUUID(username)

            if (not uuid):
                await minecraftChannel.send("<@" + str(member.id) + "> not a real username :frowning:")
                return

            if (user != None):

                if (user["username"] != username):
                    #Find and replace usernames
                    with open(self.whitelistJSON, "r+") as f:
                        whitelist = f.read()
                        whitelist = whitelist.replace(user["username"], username)
                        whitelist = whitelist.replace(user["uuid"], uuid)
                        
                        f.seek(0)
                        f.write(whitelist)
                        f.truncate()
                    self.whitelistUpdate()
                
                #Send confirmation in DMs or MC channel
                try:
                    await member.send("Whitelisted `" + username + "` (replaced `" + user["username"] + "`)")
                except:
                    await minecraftChannel.send("<@" + str(member.id) + "> changed your whitelisted account. Allow direct messages from server members in your privacy settings and use `@Donkey ip` to receive the IP and server info :confused:")

            else:
                #Write username to file
                with open(self.whitelistJSON, "r") as f:
                    whitelist = json.load(f)
                    whitelist.append({
                        "uuid": uuid,
                        "name": username
                    })
                with open(self.whitelistJSON, "w") as f:
                    json.dump(whitelist, f)

                #Send confirmation in DMs or MC channel
                try:
                    await member.send("Whitelisted `" + username + "`")
                    await member.send("**IMPORTANT PLEASE READ:** *The whitelist updates automatically every 2 minutes*. Be patient and if you are not whitelisted after 5 minutes please verify your minecraft name.\n\nThis server is __anarchy__ meaning that it is __NOT__ moderated. Do not @ anyone in the Discord asking for help because you will not get any. Keep discussion in the #minecraft channel and have fun :thumbsup:\n\n**Server IP:** IP.ADDRESS.HERE\n**Version:** 1.16.1 (Latest Release)")

                except:
                    await minecraftChannel.send("<@" + str(member.id) + "> Allow direct messages from server members in your privacy settings and use `@Donkey ip` to receive the IP and server info :confused:")
                
                self.whitelistUpdate()
            
            self.minecraft.upsert({
                'id': member.id,
                'username': username,
                'uuid': uuid
            }, where('id') == member.id)

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
                await member.send("**IMPORTANT PLEASE READ:** *The whitelist updates automatically every 2 minutes*. Be patient and if you are not whitelisted after 5 minutes please verify your minecraft name.\n\nThis server is __anarchy__ meaning that it is __NOT__ moderated. Do not @ anyone in the Discord asking for help because you will not get any. Keep discussion in the #minecraft channel and have fun :thumbsup:\n\n**Server IP:** IP.ADDRESS.HERE\n**Version:** 1.16.1 (Latest Release)")
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