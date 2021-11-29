import discord
from discord.ext import commands


class Help(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def howtouse(self, ctx):
        embed = discord.Embed(title="How to use Alv", description="Usefull commands", color=0x00c7e6)
        embed.add_field(name="!add_date", value='Add a possible date for the next session')
        embed.add_field(name="!common", value='Find the common dates between the users')
        embed.add_field(name="!delete []", value='Delete a specific number of messages. Admin only')
        await ctx.send(embed=embed)

        #TDO Overwrite help command to give more info to the user

def setup(client):
    client.add_cog(Help(client))
