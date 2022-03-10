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
    async def show_dates(self, ctx):

        message, list = utils.show_date(str(ctx.author))
        #Mention the user, print the message and if the list is not empty, print it.
        await ctx.send(ctx.author.mention)
        await ctx.send(message)

        if len(list) != 0:
            dates_string = "".join(list)
            await ctx.send(dates_string)


    @commands.command()
    async def remove_date(self, ctx):
        #Show the dates the user has entered
        dates_list = []
        message, dates_list = utils.show_date(str(ctx.author))
        #Mention the user, print the message and if the list is not empty, print it.
        await ctx.send(ctx.author.mention)
        await ctx.send(message)
        if len(dates_list) != 0:
            dates_string = "".join(dates_list)
            await ctx.send(dates_string)

        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel

        try:
            await ctx.send('Enter the number or numbers of the dates you wish to delete: ')
            #Read the user input and split it into seperate days
            msg = await self.client.wait_for("message", check=check, timeout=60)
            input_list = msg.content.split(",")
            author = str(msg.author)
            #Sanitize the input
            sanitized_list = []
            for entry in input_list:
                entry = utils.remove_spaces(entry)
                #If its a number and it exists in the file, add it to the list
                if utils.is_number(entry):
                    num = int(entry)
                    if num <= len(dates_list):
                        sanitized_list.append(num)
            #First remove the necessary dates
            for number in sanitized_list:
                #FIX: Only the first pop will be correct. The ones that follow will pop the
                #wrong index
                dates_list.pop(number-1)
            #Then normalize the rest of the entries (remove the digit and the \n)
            #TODO find a more optimized way
            final_dates = []
            for date in dates_list:
                temp = list(date)
                #The format is for example 1. 22/1(9:00-23:59)\n
                temp.pop(0)
                temp.pop(0)
                temp.pop(0)
                temp.pop(-1)
                string = "".join(temp)
                final_dates.append(string)


            #Write to the file
            #TODO needs impovement
            lines = list()
            with open(utils.get_filename(), 'r', newline="") as csvfile:
                reader = csv.reader(csvfile, delimiter=",")
                #Load the whole file in lines list
                for row in reader:
                    name = row[0]
                    #rows.append(row)
                    if author != name:
                        lines.append(row)
                    else:
                        new_line = []
                        new_line.append(author)
                        for string in final_dates:
                            new_line.append(string)
                        lines.append(new_line)
                        print(lines)
            #Rewrite the new file
            with open(utils.get_filename(), 'w') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerows(lines)

        except asyncio.TimeoutError:
            await ctx.send("Sorry, you didn't reply in time")



def setup(client):
    client.add_cog(Add_date(client))
