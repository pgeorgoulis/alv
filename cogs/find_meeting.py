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
    #Gets a list of users and removes from the dates.csv file any of their dates that have passed
    #When the new dates are rewritten into the file they should be sorted
    def purge_dates(self, channel_users):
        cur_day = datetime.today().day
        cur_month = datetime.today().month

        new_file = []
        for user in channel_users:
            users_dates, exit, message = utils.get_users_dates(user)
            temp_list = []
            temp_list.append(user)
            if exit == 0:
                users_dates = utils.sort_dates(users_dates)
                for entry in users_dates:
                    month = int(entry.get_month())
                    day = int(entry.get_day())
                    if month == cur_month:
                        if day > cur_day:
                            temp_list.append(entry.get_full_date())
                    elif month > cur_month:
                        temp_list.append(entry.get_full_date())
            #TODO replace all the writting to the file here and in the show_and_remove with a seperate function. Also, optimize this solution
            new_file.append(temp_list)

        #Read the file and add all the users that werent in channel_users back into the file. 
        with open(utils.get_filename(), 'r', newline="") as csvfile:
            reader = csv.reader(csvfile, delimiter=",")
            for row in reader:            
                user_name = row[0]
                if user_name not in channel_users:
                    new_file.append(row)


        with open(utils.get_filename(), 'w') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(new_file)


    @commands.command(pass_context = True)
    @commands.has_permissions(administrator=True)   #Raises some subclass CommandError #TODO catch all the admin privilage errors and print the same message (pehaps global exception filter)
    async def find_meeting(self, ctx, duration):

        #Purge the dates from the channel users
        channel_users = []
        for mem in ctx.channel.members:
            channel_users.append(str(mem))
        channel_users.remove("Alv#3487")
        self.purge_dates(channel_users)

        #Get all the dates from the user channels and format them in a specific way
        formated_dates = [] # A list of dictionaries with all the common dates 
        for user in channel_users:
            user_dates, exit_code, message = utils.get_users_dates(user)
            user_dates = utils.sort_dates(user_dates)
            if exit_code !=0:
                await ctx.send(message)
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
                busy_time = [True] * 1440
                for (s,e) in time_list:
                    for i in range(s,e):
                        #All the remaiing True fieds will be unusable busy time slots
                        busy_time[i] = False
            #By now, the busy minutes of one day for one user are found. 
                busy_times_list.append(busy_time)

            
            #for every users times
            free_time = [True]*1440
            for busy_mins in busy_times_list:
                for i in range(0,1440):
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
                    if time_diffObj.get_hour() >= int(duration):
                        meetings.append(dateObj)

        #Print some stats about the dates using formated_dates, the set of dictionaries from above
        length = len(common_keys)
        if length == 0:
            string = "0 common days found"
        elif length == 1:
            string = "1 common day found:\n"
            #TODO find a workaround without the loop to get the only one set element
            for date in common_keys:
                string = string + date
        else:
            string = str(length) + " common days found:\n"
            common_dates_string = ""
            for date in common_keys:
                common_dates_string = common_dates_string + date + "\n"
            string = string + common_dates_string

        #Create the embed with the stats and send it at the end
        em = discord.Embed(title="Statistics", color =0x0CC10C)        
        em.add_field(name="Common Days", value=string, inline=False)


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

                embed = discord.Embed(title="Possible Session", colour=0x87CEEB)
                embed.add_field(name="Date", value=string, inline=False)
                embed.add_field(name="From", value=start, inline=True)
                embed.add_field(name="Until", value=end, inline=True)
                await ctx.send(embed=embed)
        
        #Send the statistics last every time
        await ctx.send(embed=em)

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