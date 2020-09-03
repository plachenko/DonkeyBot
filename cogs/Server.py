import discord
from discord.ext import commands

""" 
    Server.py
    - Contains various specific guild related IDs
    - Naming scheme must specify the type for setup command (Channel/Role) 
"""

class Server():
    def __init__(self):

        #Server
        self.server = 532749639775027208

        #Channels
        self.generalChannel = 284028535155326976
        self.experimentChannel = 718251019661869156
        self.labChannel = 718600409652133948
        self.spamChannel = 302471952566845440
        self.minecraftChannel = 680316844581847049
        self.logChannel = 299941563302150145

        #Roles
        self.goodRole = 718590952947580950
        self.badRole = 718590813726179398
        self.coolGuyRole = 717900752583917598
        self.regularRole = 289947714630713344
        self.notseriousRole = 519920381507797002

        #Important People
        self.robID = 175151337363734529

