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

            #Check if the dates were added succesfully
            found_list, exit_code = utils.confirm_change(author, dates_list)
            for i in range(found_list):
                if found_list[i]:
                    #TODO maybe send a collective message for the possitives to avoid spam. Maybe with .join
                    #Each date that was not added should be sent on its own.
                    await ctx.send(f'Date {dates_list[i]} was added succesfully')
                else:
                    await ctx.send(f'Error: Date {dates_list[i]} was not added')

        except asyncio.TimeoutError:
            await ctx.send("Sorry, you didn't reply in time")


def setup(client):
    client.add_cog(Add_date(client))
