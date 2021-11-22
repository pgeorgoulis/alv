
# bot.py
import os
import discord
import asyncio
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = commands.Bot(command_prefix='!')

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

@client.command()
async def set_date(ctx):
    await ctx.send('Enter the available days: ')

    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel

    try:
        msg = await client.wait_for("message", check=check, timeout=30)
        await ctx.send(f'You said {msg.content}')
    except asyncio.TimeoutError:
        await ctx.send("Sorry, you didn't reply in time")

@client.command()
async def embed(ctx):
    embed = discord.Embed(title="Next session:", url="", description="kalispera", color=0x00c7e6)
    await ctx.send(embed=embed)

#client.wati_for() to read user inpput raise timeout error
#context.message to fetch the message of the commands
#context.author to fetch the user that called the commands
#context.send to send a message to the channel


client.run(TOKEN)
