import discord
from discord.ext import commands
from discord.ext.commands import MissingPermissions
from discord.utils import get
from datetime import date
import csv
import utils

class Find_meeting(commands.Cog):

    def __init__(self, client):
        self.client = client

    #This function gets called every time the find_meeting does.
    #It deletes from the file all the dates that have passed
    def purge_dates(self, channel_users):
        print(f'The users in this channel are: {channel_users}')

        cur_day = date.today().day
        cur_month = date.today().month

        new_file = []
        for user in channel_users:
            users_dates, exit, message = utils.get_users_dates(user)
            temp_list = []
            temp_list.append(user)
            if exit == 0:
                for entry in users_dates:
                    month = int(entry.get_month())
                    day = int(entry.get_day())
                    if month == cur_month:
                        if day > cur_day:
                            temp_list.append(entry.get_full_date())
                    elif month > cur_month:
                        temp_list.append(entry.get_full_date())
            #TODO replace all the writting to the file here and in the show_and_remove
            #with a seperate function. Also, optimize this solution
            new_file.append(temp_list)

        with open(utils.get_filename(), 'w') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(new_file)


    @commands.command()
    @commands.has_permissions(administrator=True)   #Raises some subclass CommandError
    async def find_meeting(self, ctx):

        channel_users = []
        for m in ctx.channel.members:
            channel_users.append(str(m))
        #Remove the bots name from the list
        channel_users.remove("Alv#3487")
        self.purge_dates(channel_users)

        #Fetch the dates for all the users
        final_dates = []
        for user in channel_users:
            date_dictionary = {}
            temp, exit_code, message = utils.get_users_dates(user)
            #if an error occured
            if exit_code !=0:
                await ctx.send(message)
                return
            #Create a dictionary with keys the date and value a time list for that date
            #For each date, if it already exists add its times to the existing date
            #If it does not add it as a new to the Dictionary
            #Finally, add the dictionary of each user in a list representing the csv
            #fine in an itterable format.
            dictionary = {}
            for entry in temp:
                date = entry.get_day()+"-"+entry.get_month()
                if date in dictionary:
                    old_times = dictionary[date]
                    new_time = (entry.get_start_time().base60(), entry.get_end_time().base60())
                    old_times.append(new_time)
                else:
                    #Tupple of 2 elements inside a time list for that date with possible multiple entries
                    time_list = [(entry.get_start_time().base60(), entry.get_end_time().base60())]
                    dictionary[date] = time_list
            print(dictionary)
            final_dates.append(dictionary)

        #By now all the users dates are in a dictionary in the final_dates

        common_keys = set(final_dates[0].keys())
        for dic in final_dates[1:]:
            common_keys.intersection_update(set(dic.keys()))

        print(common_keys)
        #Find the true final dates and times for each user by popping the
        #ones that are not in common_keys
        for d in final_dates:
            for key in list(d.keys()):
                if key not in common_keys:
                    d.pop(key)


    @find_meeting.error
    async def find_meeting_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            await ctx.send("This command is only available to sigma males")
        else:
            raise error

def setup(client):
    client.add_cog(Find_meeting(client))
