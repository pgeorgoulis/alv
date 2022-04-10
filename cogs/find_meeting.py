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
    def purge(self, channel_users):
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
        self.purge(channel_users)

        #Fetch the dates for all the users

    @find_meeting.error
    async def find_meeting_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            await ctx.send("This command is only available to sigma males")
        else:
            raise error

def setup(client):
    client.add_cog(Find_meeting(client))
