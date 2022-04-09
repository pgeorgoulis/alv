
# bot.py
import os
import random
import discord
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

intents = discord.Intents.all()
client = commands.Bot(command_prefix='!', intents=intents)
client.remove_command('help')
#Global variables for the file name and size


#Events
@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

    print("Guild Members:")
    for member in guild.members:
        print(member)

    '''channel = client.get_channel(931601808701395016) #bot commands channel
    await channel.send("Επειδή θέλω, όχι επειδή μου το είπες")
    with open('my_image.jpeg', 'rb') as f:
        picture = discord.File(f)
        await channel.send(file=picture)'''

initial_extensions = []

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        initial_extensions.append("cogs."+filename[:-3]) #:-3] remove the .py

if __name__ == '__main__':
    for extension in initial_extensions:
        client.load_extension(extension)

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        strings = ["how about no", "no.", "I shall not","Um... yeah, no", "Δεν θα μου πεις τι να κάνω", "Επειδή θέλω, όχι επειδή μου το είπες"]
        await ctx.send(random.choice(strings))


client.run(TOKEN)
