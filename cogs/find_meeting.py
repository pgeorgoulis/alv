import discord
from discord.ext import commands
from discord.ext.commands import MissingPermissions
from discord.ext.commands import MissingRequiredArgument
from requests import get
import json
from datetime import datetime
from date import Date
import csv
import utils

class Find_meeting(commands.Cog):

    def __init__(self, client):
        self.client = client

    #This function gets called every time the find_meeting does.
    #It deletes from the file all the dates that have passed
    def purge_dates(self, channel_users):
        cur_day = datetime.today().day
        cur_month = datetime.today().month

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


    @commands.command(pass_context = True)
    @commands.has_permissions(administrator=True)   #Raises some subclass CommandError
    async def find_meeting(self, ctx, duration):

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
            temp = utils.sort_dates(temp)
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
                date = entry.get_day()+"/"+entry.get_month()
                if date in dictionary:
                    old_times = dictionary[date]
                    new_time = (entry.get_start_time().base60(), entry.get_end_time().base60())
                    old_times.append(new_time)
                else:
                    #Tupple of 2 elements inside a time list for that date with possible multiple entries
                    time_list = [(entry.get_start_time().base60(), entry.get_end_time().base60())]
                    dictionary[date] = time_list
            final_dates.append(dictionary)

        #By now all the users dates are in a dictionary in the final_dates

        common_keys = set(final_dates[0].keys())
        for dic in final_dates[1:]:
            common_keys.intersection_update(set(dic.keys()))
        #Find the true final dates and times for each user by popping the
        #ones that are not in common_keys
        #probably unnecesary
        for d in final_dates:
            for key in list(d.keys()):
                if key not in common_keys:
                    d.pop(key)
        meetings = []
        for key in common_keys:
            users_times = []
            for dic in final_dates:
                #find the busy hours
                time_list = dic[key]
                busy_time = [True] * 1439
                for (s,e) in time_list:
                    for i in range(s,e):
                        #All the remaiing True fieds will be unusable busy time slots
                        busy_time[i] = False

                users_times.append(busy_time)

            free_time = [True]*1439
            #for every users times
            for busy_mins in users_times:
                for i in range(0,1439):
                    if busy_mins[i] is True:
                        free_time[i] = False

            result = list()
            openInterval = False
            beg, end = 0, 0
            for i, slot in enumerate(free_time):
                if not openInterval and slot:
                    openInterval = True
                    beg = i
                elif openInterval and not slot:
                    openInterval = False
                    end = i
                    beg = utils.base60_to_str(beg)
                    end = utils.base60_to_str(end)
                    #Create the meeting date
                    dateObj = Date(key, beg, end)
                    time_diffObj = utils.time_diff(dateObj.get_start_time(), dateObj.get_end_time())
                    if time_diffObj.get_hour() >= int(duration):
                        meetings.append(dateObj)

        if len(meetings) == 0:
            await ctx.send("Looks like there won't be a session this week. Here is a meme to make you feel better")
            content = get("https://meme-api.herokuapp.com/gimme/dndmemes").text
            data = json.loads(content,)
            meme = discord.Embed(title=f"{data['title']}", Color = discord.Color.random()).set_image(url=f"{data['url']}")
            await ctx.send(embed=meme)
        else:
            uild = ctx.guild
            meetings = utils.sort_dates(meetings)
            if len(meetings) == 1:
                await ctx.send("I found the following date:")
            else:
                await ctx.send("I found the following dates:")
            for meeting in meetings:
                #Get all the fiends needed
                year = datetime.today().year
                month = int(meeting.get_month())
                day = int(meeting.get_day())
                start = meeting.get_start_time().time_to_string()
                end = meeting.get_end_time().time_to_string()
                string = datetime(year, month, day).strftime("%A")+" "+str(day)+"/"+str(month)

                embed = discord.Embed(title="Available Date", colour=0x87CEEB)
                embed.add_field(name="Date", value=string, inline=False)
                embed.add_field(name="Start time", value=start, inline=True)
                embed.add_field(name="End time", value=end, inline=True)
                await ctx.send(embed=embed)

    @find_meeting.error
    async def find_meeting_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            await ctx.send("Error: This command is only available to sigma males")
        elif isinstance(error, MissingRequiredArgument):
            await ctx.send("Error: find_meeting needs a time duration argument")
        else:
            raise error

def setup(client):
    client.add_cog(Find_meeting(client))
