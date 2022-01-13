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
                #FIX this is too complicated, Find possible simple solution
                dic = utils.date_parser(next_row)
                dates = dic.keys()
                row_set = set(dates)
                #find the intersection between the intersection_keys and the new rows
                common_days = common_days.intersection(row_set)

                print("$$$$$$")
                print(common_days)
            await ctx.send(common_days)


def setup(client):
    client.add_cog(Find_meeting(client))
