import discord
from discord.ext import commands
import csv

class Find_meeting(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def common(self, ctx):

        await ctx.send(calc_date())

    def intersection(lst1, lst2):
        lst3 = [value for value in lst1 if value in lst2]
        return lst3

    def count_lines():
        with open(file_name, 'r') as file:
            count =0
            for line in file:
                if line != "\n":
                    count += 1
        return count

    def calc_date():
        common_days = list()
        line_count = count_lines()
        if line_count <= 1:
            print("Error: Not enough entries")
            return

        with open(file_name, 'r', newline="") as csvfile:
            reader = csv.reader(csvfile, delimiter=",")

            #Get the first line
            first_row = next(reader)
            #remove the first element which is the name
            first_row.pop(0)
            #first_days = set(row)

            #Get the second line
            second_row = next(reader)
            second_row.pop(0)
            #Common elements of the first two
            common_days = intersection(first_row, second_row)

            for i in range(line_count-2):
                next_row = next(reader)
                next_row.pop(0)
                common = intersection(common_days, next_row)

        return common


def setup(client):
    client.add_cog(Find_meeting(client))
