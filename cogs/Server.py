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
        self.server = 284028259027648513

        #Channels
        self.generalChannel = 284028535155326976
        self.experimentChannel = 718251019661869156
        self.labChannel = 718600409652133948

        #Roles
        self.goodRole = 718590952947580950
        self.badRole = 718590813726179398
        self.coolGuyRole = 717900752583917598

        #Important People
        self.robID = 151486808247500801

