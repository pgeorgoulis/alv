import discord
from discord.ext import commands
import csv
import utils

class Find_meeting(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(administrator=True)   #Raises some subclass CommandError
    async def find_meeting(self, ctx):
        common_days = set()
        line_count = utils.file_lines()
        if line_count <= 1:
            await ctx.send("Error: Not enough entries")
            return

        with open(utils.get_filename(), 'r', newline="") as csvfile:
            reader = csv.reader(csvfile, delimiter=",")
            date_dictionary1 = {}
            date_dictionary2 = {}
            #Get the first line
            first_row = next(reader)
            #remove the first element which is the name
            first_row.pop(0)
            #first_days = set(row)
            date_dictionary1 = utils.date_parser(first_row)

            #Get the second line
            second_row = next(reader)
            second_row.pop(0)
            date_dictionary2 = utils.date_parser(second_row)
            #Common elements of the first two
            common_days = date_dictionary1.keys() & date_dictionary2.keys()
            #for each row
            for i in range(line_count-2):
                next_row = next(reader)
                next_row.pop(0)
                #convert the list of dates into a date_dictionary
                #FIX this is too complicated, Find simpler solutino
                dic = utils.date_parser(next_row)
                dates = dic.keys()
                row_set = set(dates)
                #find the intersection between the intersection_keys and the new rows
                common_days = common_days.intersection(row_set)


        #read the whole file and store it to a list. Each user/line is a dictionary of dates
        lines = []
        with open(utils.get_filename(), 'r', newline="") as csvfile:
            reader = csv.reader(csvfile, delimiter=",")

            for i in range(line_count):
                row = next(reader)
                row.pop(0)
                dictionary = utils.date_parser(row)
                lines.append(dictionary)

        meetings = {}
        for date in common_days:
            start_times = []
            end_times = []
            for i in range(line_count):
                time = lines[i].get(date)
                start_times.append(time[0])
                end_times.append(time[1])

            #now we have all the start and end times from all the users for that date
            #The real starting time will be the maximum value of the start_times list
            #The real ending time will be the minimum value of the end_times list
            start = utils.max_time(start_times)

            end = utils.min_time(end_times)
            #If the time differtence is acceptable add the date add the time to the meetings list
            time_difference = utils.time_diff(start, end)
            if time_difference.get_hour() > 4:
                meetings[date] = [start, end]

        #By now all the acceptable meetings should be added to the meetings dictionary
        if len(meetings) == 0:
            await ctx.send("There are no common dates or times in the given dates")
        else:
            for date, time in meetings.items():
                await ctx.send("Meeing found:\nDate: "+ date +"\nStart time: "+ time[0].time_to_string() +"\nEnd time: "+time[1].time_to_string() )



def setup(client):
    client.add_cog(Find_meeting(client))
