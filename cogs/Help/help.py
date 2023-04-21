import discord
from discord.ext import commands

class Help(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.group(invoke_without_command=True)
    async def help(self, ctx):
        embed = discord.Embed(title="Help", description="Use !help <command> for extended information on a command", color = ctx.author.color)
        embed.add_field(name="<command>", value="The following commands are available at this time", inline=False)
        embed.add_field(name="Session scheduling", value="add, remove, show, find_meeting, oneshot, stats")
        embed.add_field(name="Miscellaneous", value="delete, pics, poll, meme")
        await ctx.send(embed=embed)

    @help.command()
    async def add(self, ctx):
        em = discord.Embed(title="Add", description="Adds a date available for a session", color=ctx.author.color)
        em.add_field(name="**How to use**", value="Call the command and give up to 9 valid dates as input, one on each shown field")
        em.add_field(name="Valid Date:", value="A valid date consists of a valid day and a valid time period", inline=False)
        em.add_field(name="Day", value=("A day could be given as a date (9/12, 22/7 etc) following the dd/mm format or as a string."
                                        "\n\nAcceptable strings are each day of the week **(Monday, Tuesday etc)** witch refer to the days of the current week and the keywords today, tomorrow."))
        em.add_field(name="Time", value=("A time period should always be given inside parenthesis. The value could be ether a time period (11:30-18:45) following the 24h format or a string."
                                        " \n\nAcceptable strings are the following: **morning, noon, night, day**"
                                            "\nEach string has an assigned start and end time."
                                            "\nday ->\t(9:00-24:00)\nmorning ->\t(11:30-15:30)\nnoon ->\t(17:00-22:00)\nnight ->\t(20:00-24:00)"), inline=False)
        em.add_field(name="Examples", value=("Some correct date examples are:\n"
                                              "\n7/11(9:00-24:00)\n"
                                              "8/11(noon)\n"
                                              "9/11(13:00-18:45)\n"
                                              "tomorrow(noon)\n"
                                              "Sunday(17:00-23:45)\n"
                                              "Each date must be separated with ENTER from the next one."), inline=False)
        em.add_field(name="**Warning**", value="The new dates should not overlap with eachother.")
        await ctx.send(embed=em)

    @help.command()
    async def show(self, ctx):
        em = discord.Embed(title="Show", description="Shows a sorted list of every date the user has entered so far. By default it returns the dates of the user who called the command but if given a username it will return those dates instead.", color=ctx.author.color)
        await ctx.send(embed=em)
    
    @help.command()
    async def meme(self, ctx):
        em = discord.Embed(title="Meme", description="Posts a random image from the top 35 posts on r/dndmemes this week", color=ctx.author.color)
        await ctx.send(embed=em)
    
    @help.command()
    async def poll(self, ctx):
        em = discord.Embed(title="Poll", description="Creates a poll with up to 9 choices.", color=ctx.author.color)
        em.add_field(name="**Syntax**", value="You type the command name followed by the question and the available options as shown by the fields when the command is called.", inline=False)
        em.add_field(name="Example", value="\poll \"Title of the poll\" first_option second_option third_option", inline=False)
        await ctx.send(embed=em)

    @help.command()
    async def oneshot(self, ctx):
        em = discord.Embed(title="Oneshot", description="Prints all the dm's available dates and how many members are available for each one of those dates. The Dm is the user calling the command or a valid server member given as input.", color=ctx.author.color)
        await ctx.send(embed=em)
    
    @help.command()
    async def pics(self, ctx):
        em = discord.Embed(title="Pics", description="Creates and posts into a thread all images sent to the current channel. Alternatively, posts all the images sent in the last X messages.", color=ctx.author.color)        
        em.add_field(name="Example", value="/pics 10\n will show all the images in the last 10 messages", inline=False)
        await ctx.send(embed=em)
    
    @help.command()
    async def files(self, ctx):
        em = discord.Embed(title="Files", description="Creates and posts into a thread all files (pdf, docx, txt and more) sent to the current channel. Alternatively, posts all the files sent in the last X messages.", color=ctx.author.color)        
        em.add_field(name="Example", value="/files 10\n will show all the files in the last 10 messages", inline=False)
        await ctx.send(embed=em)
    
    @help.command()
    async def stats(self, ctx):
        em = discord.Embed(title="Stats", description="Shows more information about the users and all the entered dates", color=ctx.author.color)
        await ctx.send(embed=em)

    @help.command()
    async def remove(self, ctx):
        em = discord.Embed(title="Remove", description="Removes one or more dates", color=ctx.author.color)
        em.add_field(name="How to use", value=("After calling /remove a menu will be shown to the user with each date he has entered."
                                    "Choose the dates you wish to remove and click off the menu. A confirm message should follow."))
        await ctx.send(embed=em)

    @help.command()
    async def find_meeting(self, ctx):
        em = discord.Embed(title="Find Meeting", description="Finds the possible meeting times for all the members in the channel that it's called in.", color=ctx.author.color)
        em.add_field(name="Aliases", value="find", inline=False)
        em.add_field(name="Duration", value="A number indicating how many hours the meeting should last. Default value is 3 hours.")
        #em.add_field(name="Permissions", value="This command is only available to users with the administrator role")
        await ctx.send(embed=em)

    @help.command()
    async def delete(self, ctx):
        em = discord.Embed(title="Delete", description="Deletes a number of messages in the channel that its called in", color=ctx.author.color)
        em.add_field(name="**Syntax**", value="!delete <integer>", inline=False)
        em.add_field(name="<integer>", value="A number indicating how many messages should be deleted")
        em.add_field(name="Permissions", value="This command is only available to users with the administrator role")
        await ctx.send(embed=em)


async def setup(client):
    await client.add_cog(Help(client))