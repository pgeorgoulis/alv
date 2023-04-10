from discord import Embed
import discord
from discord.ext import commands
from discord import app_commands
from discord.ext.commands import MissingPermissions
from discord.ext.commands import MissingRequiredArgument
import json
from datetime import datetime
from date import Date
import utils

class Find_meeting(commands.Cog):

    def __init__(self, client):
        self.client = client


    @app_commands.command(name = "find_meeting", description="Finds possible meeting times for all the users in the current chat")
    async def find_meeting(self, interaction=discord.Interaction, duration: int = None):

        #Purge the dates from the channel users
        channel_users = []
        for mem in interaction.channel.members:
            channel_users.append(str(mem))
        channel_users.remove("Alv#3487")
        utils.purge_dates(channel_users)

        #Get all the dates from the user channels and format them in a specific way
        formated_dates = [] # A list of dictionaries with all the common dates 
        for user in channel_users:
            user_dates, exit_code, message = utils.get_users_dates(user)
            user_dates = utils.sort_dates(user_dates)
            if exit_code !=0:
                await interaction.channel.send(message)
                return    

            dictionary = {}
            for entry in user_dates:
                date = entry.get_day()+"/"+entry.get_month()
                #if the date already excists, append the new times to the excisting ones
                if date in dictionary:
                    excisting_times = dictionary[date]
                    new_time = (entry.get_start_time().base60(), entry.get_end_time().base60())
                    excisting_times.append(new_time)
                    dictionary[date] = excisting_times
                    #TODO write it in a more "pythonic" way
                else:
                    #Tupple of 2 elements inside a time list for that date with possible multiple entries
                    time_list = [(entry.get_start_time().base60(), entry.get_end_time().base60())]
                    dictionary[date] = time_list
            formated_dates.append(dictionary)

        common_keys = set(formated_dates[0].keys())
        for dic in formated_dates[1:]:
            common_keys.intersection_update(set(dic.keys()))

        for d in formated_dates:
            for key in list(d.keys()):
                if key not in common_keys:
                    d.pop(key)

        meetings = []
        for key in common_keys:
            busy_times_list = []
            for dic in formated_dates:
                #find the busy hours
                time_list = dic.get(key)
                busy_time = [True] * 1441
                for (s,e) in time_list:
                    for i in range(s,e):
                        #All the remaiing True fieds will be unusable busy time slots
                        busy_time[i] = False
            #By now, the busy minutes of one day for one user are found. 
                busy_times_list.append(busy_time)

            
            #for every users times
            free_time = [True]*1441
            for busy_mins in busy_times_list:
                for i in range(0,1441):
                    if busy_mins[i] is True:
                        free_time[i] = False
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
                    if duration == None:
                        meetings.append(dateObj)
                    elif duration != None:
                        if time_diffObj.get_hour() >= duration:
                            meetings.append(dateObj)
                    else:
                        await interaction.channel.send("Warning: Given meeting duration is not valid.The command will proceed without a duration value")
                        meetings.append(dateObj)


        if len(meetings) == 0:
            await interaction.channel.send("Looks like there won't be a session this week. Here is a meme to make you feel better")
            await interaction.invoke(self.client.get_command('meme') )
            await interaction.response.send_message("You could try using the `!oneshot` command to find the date with the most available party members")
        else:
            guild = interaction.guild
            meetings = utils.sort_dates(meetings)
            if len(meetings) == 1:
                await interaction.response.send_message("I found the following date:")
            else:
                await interaction.response.send_message("I found the following dates:")
            for meeting in meetings:
                #Get all the fiends needed
                year = datetime.today().year
                month = int(meeting.get_month())
                day = int(meeting.get_day())
                start = meeting.get_start_time().time_to_string()
                end = meeting.get_end_time().time_to_string()
                string = datetime(year, month, day).strftime("%A")+" "+str(day)+"/"+str(month)

                embed = Embed(title="Possible Session", colour=0x87CEEB)
                embed.add_field(name="Date", value=string, inline=False)
                embed.add_field(name="From", value=start, inline=True)
                embed.add_field(name="Until", value=end, inline=True)
                await interaction.channel.send(embed=embed)

async def setup(client):
    await client.add_cog(Find_meeting(client))