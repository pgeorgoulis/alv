import discord
from discord.ext import commands
from discord.ext.commands import MissingPermissions

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

    @delete.error
    async def delete_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            await ctx.send("This command is only available to sigma males")
        else:
            raise error

async def setup(client):
    await client.add_cog(Admin(client))
