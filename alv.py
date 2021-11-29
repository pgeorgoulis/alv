
# bot.py
import os
import csv
import discord
import asyncio
import re
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = commands.Bot(command_prefix='!')
#Global variables for the file name and size
file_name = "dates.csv"


#Events
@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    print(
    f'{client.user} is connecter to the following guild:\n'
    f'{guild.name}(id: {guild.id})' #print the rest of the members
    )

    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')

initial_extensions = []

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        initial_extensions.append("cogs."+filename[:-3]) #:-3] remove the .py

if __name__ == '__main__':
    for extension in initial_extensions:
        client.load_extension(extension)

client.run(TOKEN)
