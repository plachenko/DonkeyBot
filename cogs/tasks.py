import discord
from discord.ext import tasks, commands
from .Server import Server

import asyncio

""" 
Read:
https://discordpy.readthedocs.io/en/latest/ext/tasks/index.html#discord-ext-tasks-asyncio-task-helpers 
"""

class TasksCog(commands.Cog, Server):
    def __init__(self, client):
        self.client = client

        Server.__init__(self)

        self.ExampleTask.start() #Start the task

    @tasks.loop(seconds=5.0)
    async def ExampleTask(self):
        print("Task triggered")

def setup(client):
    client.add_cog(TasksCog(client))