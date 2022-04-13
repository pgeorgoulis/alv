import discord
from discord.ext import commands

class Help(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.group(invoke_without_command=True)
    async def help(self, ctx):
        embed = discord.Embed(title="Help", description="Use !help <command> for extended information on a command", color = ctx.author.color)

        embed.add_field(name="Session scheduling", value="add, remove, show, find_meeting")
        embed.add_field(name="Moderation", value="delete")
        await ctx.send(embed=embed)

    @help.command()
    async def add(self, ctx):
        em = discord.Embed(title="Add", description="Adds a date available for a session", color=ctx.author.color)
        em.add_field(name="**Syntax**", value="!add <date> (<time> - <time>) OR !add <date> (<string>)", inline=False)
        em.add_field(name="<date>", value="Each <date> must follow the format of dd/mm i.e 25/12", inline=False)
        em.add_field(name="<time>", value="Each <time> must follow the format of hh:mm i.e 12:56 (24h format)", inline=False)
        em.add_field(name="<string>", value=("The available values for <string> are: day, morning, noon, night. "
                                            "\nEach string has an assigned start and end time."
                                            "\nday ->\t(9:00-23:59)\nmorning ->\t(11:30-15:30)\nnoon ->\t(15:30-20:30)\nnight ->\t(20:30-23:59)"), inline=False)
        await ctx.send(embed=em)

    @help.command()
    async def show(self, ctx):
        em = discord.Embed(title="Show", description="Shows a sorted list of every date the user has entered so far", color=ctx.author.color)
        em.add_field(name="**Syntax**", value="!show", inline=False)
        await ctx.send(embed=em)

    @help.command()
    async def remove(self, ctx):
        em = discord.Embed(title="Remove", description="Removes one or more dates", color=ctx.author.color)
        em.add_field(name="**Syntax**", value="!remove", inline=False)
        em.add_field(name="", value=("After calling !remove the user will be shown every date he has entered "
                                    "and will be asked to write the index number of each one he wishes to remove\n"
                                    "**Syntax** <integer> OR <integer>,<integer>,...,<integer>"))
        await ctx.send(embed=em)

    @help.command()
    async def find_meeting(self, ctx):
        em = discord.Embed(title="Find Meeting", description="Finds and prints the common dates and hours of all the members in the channel the command was called", color=ctx.author.color)
        em.add_field(name="**Syntax**", value="!find_meeting <integer>", inline=False)
        em.add_field(name="<integer>", value="A number indicating how many hours the meeting should last")
        em.add_field(name="Permissions", value="This command is only available to users with administrator role")
        await ctx.send(embed=em)

    @help.command()
    async def delete(self, ctx):
        em = discord.Embed(title="Delete", description="Deletes a number of messages in the channel that its called in", color=ctx.author.color)
        em.add_field(name="**Syntax**", value="!delete <integer>", inline=False)
        em.add_field(name="<integer>", value="A number indicating how many messages should be deleted")
        em.add_field(name="Permissions", value="This command is only available to users with administrator role")
        await ctx.send(embed=em)


def setup(client):
    client.add_cog(Help(client))
