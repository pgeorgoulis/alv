
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

#write the dates to a csv file
def writeFile(author, content):
    lines = list()
    file_name = "dates.csv"
    file_size = os.path.getsize(file_name)
    found_flag=False
    with open(file_name, 'r', newline="") as csvfile:
        reader = csv.reader(csvfile, delimiter=",")
        #The first char of the file

        """if file_size == 0:
            print("empty")
            content.insert(0, author)
            lines.append(content)"""
        #Load the whole file in memory
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

    with open(file_name, 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(lines)

    return


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
async def embed(ctx):
    embed = discord.Embed(title="Next session:", url="", description="kalispera", color=0x00c7e6)
    await ctx.send(embed=embed)
    await ctx.send(f'said {dates_array}')


client.run(TOKEN)





#client.wati_for() to read user inpput raise timeout error
#context.message to fetch the message of the commands
#context.author to fetch the user that called the commands
#context.send to send a message to the channel
