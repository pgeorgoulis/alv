import discord
from date import Date
import asyncio
import csv
import utils


from discord.ext import commands

class Add_date(commands.Cog):

    def __init__(self, client):
        self.client = client


    #Use add date to add a available date as a user
    @commands.command()
    async def add_date(self, ctx):
        await ctx.send('Enter the available days: ')

        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel

        try:
            #Read the user input and split it into seperate days
            msg = await self.client.wait_for("message", check=check, timeout=120)
            input_list = msg.content.lower().split(",")
            author = str(msg.author)
            dates_list = list()
            #Create a date object for every date in the input string
            for entry in input_list:
                date = utils.remove_spaces(entry)
                if utils.is_date(date):
                    attributes = utils.split_date(date)
                    #Create the object and append it to the dates_list
                    obj = Date(attributes[0], attributes[1], attributes[2])
                    dates_list.append(obj)
                else:
                    await ctx.send("Wrong format of data. Use !help to find the correct one")

            #write the valid dates_list to a file
            for date in dates_list:
                utils.writeFile(author, date.get_full_date())


        except asyncio.TimeoutError:
            await ctx.send("Sorry, you didn't reply in time")


    @commands.command()
    async def remove_date(self, ctx):

        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel

        try:
            await ctx.send('Enter the number or numbers of the dates you wish to delete: ')
            #Read the user input and split it into seperate days
            msg = await self.client.wait_for("message", check=check, timeout=120)
            input_list = msg.content.lower().split(",")
            author = str(msg.author)



        except asyncio.TimeoutError:
            await ctx.send("Sorry, you didn't reply in time")

    @commands.command()
    async def show_date(self, ctx):
        #Find the dates the user has entered
        with open(utils.get_filename(), 'r', newline="") as csvfile:
            reader = csv.reader(csvfile, delimiter=",")

            line_count = utils.file_lines()
            user_found = False
            for i in range(line_count):
                #First, find the user
                row = next(reader)
                print(row[0])
                if row[0] != str(ctx.author):
                    continue
                else:
                    users_line = row
                    #Exit the loop after the user is found
                    user_found = True
                    break

            if user_found is True:
                list = []
                if len(users_line) == 1:
                    await ctx.send('You haven\'t entered any dates.')
                    return
                #pop the users name and add numbers to the printed list
                users_line.pop(0)
                #For each date the user has entered
                for i in range(len(users_line)):
                    line = str(i+1)+". "+users_line[i]+"\n"
                    list.append(line)
            else:
                await ctx.send(f'Error: user {ctx.author} was not found in the file')
                return
        await ctx.send(ctx.author.mention)
        string_to_print = "".join(list)
        await ctx.send('Here are the dates you have entered:\n'+string_to_print)

def setup(client):
    client.add_cog(Add_date(client))
