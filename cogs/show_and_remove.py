import discord
from discord.ext import commands
from date import Date
import asyncio
import csv
import utils


class Show_and_remove(commands.Cog):

    def __init__(self, client):
        self.client = client


    @commands.command()
    async def show(self, ctx):

        dates_list, exit_code, message = utils.get_users_dates(str(ctx.author))
        #Mention the user, print the message and if the list is not empty, print it.
        await ctx.send(ctx.author.mention)
        await ctx.send(message)

        #Only if the error code is 0 print the dates. Else, there aren't any dates to print
        final_string = ""
        if exit_code == 0:
            dates_list = utils.sort_dates(dates_list)
            #Initialize the counter
            i=1
            for date in dates_list:
                temp = str(i)+". "+ date.get_full_date() +"\n"
                final_string += temp
                i+=1
            await ctx.send(final_string)


    @commands.command()
    async def remove(self, ctx):
        #Show the dates to the user
        #Need to find diffrent aproach instead of copying the show dates code.
        dates_list, exit_code, message = utils.get_users_dates(str(ctx.author))

        #Mention the user, print the message and if the list is not empty, print it.
        await ctx.send(ctx.author.mention)
        await ctx.send(message)

        #Only if the error code is 0 print the dates. Else, there aren't any dates to print
        final_string = ""
        if exit_code == 0:
            #Initialize the counter
            dates_list = utils.sort_dates(dates_list)
            i=1
            for date in dates_list:
                temp = str(i)+". "+ date.get_full_date() +"\n"
                final_string += temp
                i+=1
            await ctx.send(final_string)
        else:
            return

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
                    else:
                        await ctx.send(f'Error: Number {num} does not exist in the list above')
                else:
                    await ctx.send(f'Error: Entry {num} not an integer')

            #Find the dates that need to be removed
            remove_dates = []
            for number in sanitized_list:
                remove_dates.append(dates_list[number-1])

            #And remove them
            for r_date in remove_dates:
                for date in dates_list:
                    #TODO see if comparing objects works
                    if r_date.get_full_date() == date.get_full_date():
                        dates_list.remove(date)
                        #TODO probably needs break here

            #Write to the file
            #TODO needs impovement, make this function one the the utils write file function
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
                        for date in dates_list:
                            new_line.append(date.get_full_date())
                        lines.append(new_line)
            #Rewrite the new file
            with open(utils.get_filename(), 'w') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerows(lines)

            #Check if the dates were added succesfully
            found_list, exit_code = utils.confirm_change(author, remove_dates)
            for i in range(len(found_list)):
                if found_list[i]:
                    await ctx.reply(f'Error: Date {remove_dates[i].get_full_date()} was not removed')
                else:
                    #TODO maybe send a collective message for the possitives to avoid spam. Maybe with .join
                    #Each date that was not added should be sent on its own.
                    await ctx.reply(f'Date {remove_dates[i].get_full_date()} was removed succesfully')


        except asyncio.TimeoutError:
            await ctx.send("Sorry, you didn't reply in time")


def setup(client):
    client.add_cog(Show_and_remove(client))
