
# bot.py
import os
import discord
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


@client.command(name='set_date')
async def command(ctx):
	global times_used
	await ctx.send(f"enter the available dates")

	def check(msg):
		return msg.author == ctx.author and msg.channel == ctx.channel

	msg = await client.wait_for("message", check=check)
	ctx.send(msg.content.lower())

	times_used = times_used + 1
#client.wati_for() to read user inpput raise timeout error
#context.message to fetch the message of the commands
#context.author to fetch the user that called the commands
#context.send to send a message to the channel


client.run(TOKEN)
