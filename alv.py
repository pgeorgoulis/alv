
# bot.py
import os
import csv
import discord
import asyncio
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = commands.Bot(command_prefix='!')
#Global variables for the file name and size
file_name = "dates.csv"


def count_lines():
    with open(file_name, 'r') as file:
        count =0
        for line in file:
            if line != "\n":
                count += 1
    return count


#write the dates to a csv file
def writeFile(author, content):
    lines = list()
    found_flag=False

    with open(file_name, 'r', newline="") as csvfile:
        reader = csv.reader(csvfile, delimiter=",")

        #Load the whole file in lines list
        for row in reader:
            name = row[0]
            print(name)
            #rows.append(row)
            if author != name:
                lines.append(row)
            else:
                #get the line and append it at the end
                for string in content:
                    row.append(string)
                lines.append(row)
                found_flag = True
                print("found", author)

        #If the user does not exist already
        if not found_flag:
            #then add the new user
            print("not found", author)
            content.insert(0, author)
            lines.append(content)

    #Rewrite the new file
    with open(file_name, 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(lines)

    return

def intersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return lst3

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


#Events
@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    print(
    f'{client.user} is connecter to the following guild:\n'
    f'{guild.name}(id: {guild.id})'
    )

    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')


#Use add date to add a available date as a user
@client.command()
async def add_date(ctx):
    await ctx.send('Enter the available days: ')

    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel

    try:
        #Read the user input and split it into seperate days
        msg = await client.wait_for("message", check=check, timeout=30)
        dates_array = msg.content.lower().split(",")
        author = str(msg.author)

        writeFile(author, dates_array)

    except asyncio.TimeoutError:
        await ctx.send("Sorry, you didn't reply in time")


@client.command()
async def common(ctx):

    await ctx.send(calc_date())


@client.command()
async def embed(ctx):
    embed = discord.Embed(title="Next session:", url="", description="kalispera", color=0x00c7e6)
    await ctx.send(embed=embed)
    await ctx.send(f'said {dates_array}')


client.run(TOKEN)





#client.wati_for() to read user inpput raise timeout error
#context.message to fetch the message of the commands
#context.author to fetch the user that called the commands
#context.send to send a message to the channel
