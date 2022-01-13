import discord
from discord.ext import commands

class Admin(commands.Cog):

    def __init__(self, client):
        self.client = client

    #Alternatively @commands.has_role('RoleName')
    @commands.command(pass_context = True)
    @commands.has_permissions(administrator=True)   #Raises some subclass CommandError
    async def delete(self, ctx, number):
        num = int(number)
        await ctx.channel.purge(limit=num+1)
        await ctx.send("Messages deleted")

def setup(client):
    client.add_cog(Admin(client))