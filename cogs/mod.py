import discord
from discord.ext import commands
from .Server import Server

import re
import datetime

class ModCog(commands.Cog, Server):
    def __init__(self, client):
        self.client = client

        Server.__init__(self)

    async def isMod(ctx):
        if (ctx.message.author.guild_permissions.manage_messages):
            await ctx.message.delete() #Delete command usage
            return True
        return False

    #Takes string, returns User
    def parseUser(self, string):
        regEx = re.findall('\d+', string)
        ID = 0 if len(regEx) < 1 else int(regEx[0])
        return self.client.get_guild(self.server).get_member(ID)
    
    #Takes action + issued moderator and sends to log channel
    async def logAction(self, action, message):
        logChannel = self.client.get_guild(self.server).get_channel(self.logChannel)
        embed = discord.Embed(colour=8280315,timestamp=datetime.datetime.now())
        embed.add_field(name="Action",value=action,inline=True)
        embed.add_field(name="Moderator",value=message.author.mention,inline=True)
        embed.add_field(name="Issued",value="> " + message.content,inline=False)

        await logChannel.send(embed=embed)

    #Alt detection system
    @commands.Cog.listener()
    async def on_member_join(self, user):
        user = self.client.get_user(user.id)
        if (not user.bot):

            #Get account age
            if ((datetime.datetime.utcnow() - user.created_at).days <= 7):
                infractions = ("- " + str((datetime.datetime.utcnow() - user.created_at).days) + " days old")

                #Default avatar
                if (user.default_avatar_url == user.avatar_url):
                    infractions += "\n- Default profile picture"
                
                #Discord badges (nitro, hypesquad etc.)
                connections = []
                for flag in user.public_flags:
                    if (flag[1]):
                        connections.append(flag[0])
                if (len(connections) == 0):
                    infractions += "\n- No Discord badges"
                
                logChannel = self.client.get_guild(self.server).get_channel(self.logChannel)
                embed = discord.Embed(colour=8280315,timestamp=datetime.datetime.now())
                embed.add_field(name="User",value=user.mention,inline=False)
                embed.add_field(name="Reason(s)",value=infractions,inline=False)
                await logChannel.send(":warning: **@here possible alt detected** :warning:",embed=embed)
    
    #Give/remove Not Serious Role
    @commands.command()
    @commands.check(isMod)
    async def notserious(self, ctx, user):

        user = self.parseUser(user)
        message = ctx.message

        if (user is None):
            await ctx.message.channel.send("Could not find user")
        elif (message.guild.get_role(self.notseriousRole) not in user.roles):
            await user.add_roles(message.guild.get_role(self.notseriousRole))
            await self.logAction("Gave \"Not Serious\" Role", message)
        else:
            await user.remove_roles(message.guild.get_role(self.notseriousRole))
            await self.logAction("Removed \"Not Serious\" Role", message)

def setup(client):
    client.add_cog(ModCog(client))