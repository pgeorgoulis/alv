import discord
from discord.ext import commands
from discord.utils import get
import csv
import utils

class Find_meeting(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(administrator=True)   #Raises some subclass CommandError
    async def find_meeting(self, ctx):

        channel_users = []
        print("#######")
        for m in ctx.channel.members:
            channel_users.append(str(m))
        #Remove the bots name from the list
        channel_users.remove("Alv#3487")
        print(channel_users)

        #Fetch the dates for all the users
        



def setup(client):
    client.add_cog(Find_meeting(client))
