import discord
from discord.ext import commands
import csv
import utils

class Find_meeting(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def find_meeting(self, ctx):
        common_days = set()
        line_count = utils.file_lines()
        if line_count <= 1:
            print("Error: Not enough entries")
            return

        with open(utils.get_filename(), 'r', newline="") as csvfile:
            reader = csv.reader(csvfile, delimiter=",")

            #Get the first line
            first_row = next(reader)
            #remove the first element which is the name
            first_row.pop(0)
            #first_days = set(row)
            date_dictionary1 = {}
            date_dictionary1 = utils.date_parser(first_row)

            #Get the second line
            second_row = next(reader)
            second_row.pop(0)
            date_dictionary2 = {}
            date_dictionary2 = utils.date_parser(second_row)
            #Common elements of the first two
            common_days = date_dictionary1.keys() & date_dictionary2.keys()
            print("\n\n")
            print("######")
            print(common_days)
            print("######")
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

                print("$$$$$$")
                print(common_days)


        #read the whole file and store it to a list. Each user/line is a dictionary of dates
        lines = []
        with open(utils.get_filename(), 'r', newline="") as csvfile:
            reader = csv.reader(csvfile, delimiter=",")

            for i in range(line_count):
                row = next(reader)
                row.pop(0)
                dictionary = utils.date_parser(row)
                lines.append(dictionary)

        print(lines)

        for date in common_days:
            start_times = []
            end_times = []
            for i in range(line_count):
                print(lines[i].get(date))
                time = lines[i].get(date)
                start_time, end_time = utils.split_time(time)
                start_times.append(start_time)
                end_times.append(end_time)
            #now we have all the start and end times from all the users for that date
            #The real starting time will be the maximum value of the start_times list
            #The real ending time will be the minimum value of the end_times list
            start = utils.max(start_times)
            ## TODO: this sucks. Find a better way to compare times. Search if a date object exists
            s_hour = start.split(":")
            s_h = int(s_hour)
            end = utils.min(end_times)
            e_hour = end.split(":")
            e_h = int(e_hour)
            timeframe = e_h - s_h
            if end-timeframe > 4 :
                await ctx.send(f'Possible session at {date} {start} : {end}')


def setup(client):
    client.add_cog(Find_meeting(client))
