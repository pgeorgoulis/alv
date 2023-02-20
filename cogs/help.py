import discord
from discord.ext import commands

class Help(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.group(invoke_without_command=True)
    async def help(self, ctx):
        embed = discord.Embed(title="Help", description="Use !help <command> for extended information on a command", color = ctx.author.color)
        embed.add_field(name="<command>", value="The following commands are available at this time", inline=False)
        embed.add_field(name="Session scheduling", value="add, remove, show, find_meeting, stats")
        embed.add_field(name="Miscellaneous", value="delete, pics, poll, meme")
        await ctx.send(embed=embed)

    @help.command()
    async def add(self, ctx):
        em = discord.Embed(title="Add", description="Adds a date available for a session", color=ctx.author.color)
        em.add_field(name="**How to use**", value=("1. Use !add to call the command\n"
                                                    "2. After you see the apropriate reply from alv, enter your dates using the following format:\n" 
                                                    "   <date> (<time> - <time>)\n  OR\n    <date> (<string>)\n" 
                                                    "3. Wait for alv to reply to your message confirming the sucessfull addition of the dates\n\n"
                                                    "If you are unsure or you made a mistake you can use the commands !show and !delete to see or change your entries"), inline=False)
        em.add_field(name="<date>", value="This field represents a day and a month.They must follow the format of *dd/mm i.e 25/2*\n Alternatively, strings such as today, tomorrow, monday, saturday etc can be used", inline=False)
        em.add_field(name="<time>", value="This field represents a set of hours and minutes. Each <time> must follow the format of *hh:mm i.e 12:56 (24h format)*", inline=False)
        em.add_field(name="<string>", value=("This field represents a pre-set time frame. The available values for <string> are: *day*, *morning*, *noon*, *night*. "
                                            "\nEach string has an assigned start and end time."
                                            "\nday ->\t(9:00-24:00)\nmorning ->\t(11:30-15:30)\nnoon ->\t(15:30-20:30)\nnight ->\t(20:30-24:00)"), inline=False)
        em.add_field(name="Examples", value=("Some correct date examples are:\n"
                                              "\n7/11(9:00-24:00)\n"
                                              "8/11(noon)\n"
                                              "9/11(13:00-18:45)\n"
                                              "tomorrow(noon)\n"
                                              "Sunday(17:00-23:45)\n"
                                              "Each date must be separated with ENTER from the next one."), inline=False)
        await ctx.send(embed=em)

    @help.command()
    async def show(self, ctx):
        em = discord.Embed(title="Show", description="Shows a sorted list of every date the user has entered so far", color=ctx.author.color)
        em.add_field(name="**Syntax**", value="!show", inline=False)
        await ctx.send(embed=em)
    
    @help.command()
    async def meme(self, ctx):
        em = discord.Embed(title="Meme", description="Posts a random image from the top 35 posts on r/dndmemes this week", color=ctx.author.color)
        em.add_field(name="**Syntax**", value="!show", inline=False)
        await ctx.send(embed=em)
    
    @help.command()
    async def poll(self, ctx):
        em = discord.Embed(title="Poll", description="Creates a poll with up to 9 choices.", color=ctx.author.color)
        em.add_field(name="**Syntax**", value="You type the command name followed by the question or the title of the poll in quotes (\") and each of the available options separated by space", inline=False)
        em.add_field(name="Example", value="!poll \"Title of the poll\" first_option second_option third_option", inline=False)
        await ctx.send(embed=em)

    @help.command()
    async def pics(self, ctx):
        em = discord.Embed(title="Pics", description="Creates a thread and posts there all the chanel images. Alternatively, posts all the images sent on the last <x> messages", color=ctx.author.color)
        em.add_field(title="Aliases", value="pic, pictures, get_pics, get_pictures", inline=False)
        em.add_field(name="**Syntax**", value="!pics or !pics <integer>", inline=False)
        em.add_field(name="Example", value="`!pics 10` \nwill show all the images in the last 10 messages")
        await ctx.send(embed=em)

    @help.command()
    async def stats(self, ctx):
        em = discord.Embed(title="Stats", description="Shows more information about the users and all the entered dates", color=ctx.author.color)
        em.add_field(name="**Syntax**", value="!stats", inline=False)
        await ctx.send(embed=em)

    @help.command()
    async def remove(self, ctx):
        em = discord.Embed(title="Remove", description="Removes one or more dates", color=ctx.author.color)
        em.add_field(name="**Syntax**", value="!remove", inline=False)
        em.add_field(name="How to use", value=("After calling !remove the user will be shown every date he has entered "
                                    "and will be asked to write the index number of each one he wishes to remove\n"
                                 "\n*Syntax* <integer> OR <integer>,<integer>,...,<integer>"))
        await ctx.send(embed=em)

    @help.command()
    async def find_meeting(self, ctx):
        em = discord.Embed(title="Find Meeting", description="Finds the common dates and hours of all the members in the current chanel", color=ctx.author.color)
        em.add_field(name="Aliases", value="find", inline=False)
        em.add_field(name="**Syntax**", value="!find_meeting OR !find_meeting <integer>", inline=False)
        em.add_field(name="<integer>", value="A number indicating how many hours the meeting should last")
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
