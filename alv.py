# bot.py
import os
import asyncio
import random
import discord
import discord.ext
from dotenv import load_dotenv
from discord.ext import commands
from datetime import datetime

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('SERVER_ID')

intents = discord.Intents.all()
client = commands.Bot(command_prefix='!', intents=intents)
client.remove_command('help')
#Global variables for the file name and size

async def load_extensions():
    for foldername in os.listdir('./cogs'):
        if foldername == "__pycache__":
            continue
        for filename in os.listdir(f'./cogs/{foldername}'):
            if filename.endswith('.py'):
                await client.load_extension(f"cogs.{foldername}.{filename[:-3]}") #:-3] remove the .py

async def main():
    async with client:
        await load_extensions()
        await client.start(TOKEN)


#Events
#sync the slash command
@client.event
async def on_ready():
    print(f"discord.py {discord.__version__}\n")

    synced = await client.tree.sync()
    current_time = datetime.now().strftime("%H:%M")

    print("Local time is: "+ current_time)
    print("[+] Alv is running...")
    print("[+] Slash Commands synced: "+ str(len(synced))+" commands")

@client.event
async def on_interaction(interaction):
    author = interaction.user
    date_called = datetime.today().strftime("%d/%m/%Y, %H:%M:%S")
    try:
        #If no command name is found
        inter = interaction.command.name
    except Exception as e:
        #TODO log the failed interaction
        pass
    else:
        string = f'\nINTERACTION\t\t {inter:<15} was called at \t\t <{date_called}> \t\t by AUTHOR: \t\t {author}'
        file = open("logs.txt", "a")
        file.write(string)
        file.close()

@client.event
async def on_command(ctx):
    author = ctx.author
    date_called = datetime.today().strftime("%d/%m/%Y, %H:%M:%S")
    comm = ctx.command.name
    string = f"\nCOMMAND \t\t {comm:<15} was called at \t\t <{date_called}> \t\t by AUTHOR: \t\t {author}"
    file = open("logs.txt", "a")
    file.write(string)
    file.close()

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        strings = [
            "how about no",
            "no.",
            "I shall not",
            "Um... yeah, no",
            "I don't think so",
            "Δεν θα μου πεις τι να κάνω",
            "no u",
            "this ain't it, chief",
            "Επειδή θέλω, όχι επειδή μου το είπες"
        ]
        await ctx.send(random.choice(strings))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.mention_everyone:
        return
    if client.user.mentioned_in(message):
        pictures = [
        "metal_jacket.gif",
        "shapiro.gif",
        "shapiro.gif",
        "shapiro.gif",
        "shapiro.gif",
        "spongebob.jpg",
        "spongebob.jpg",
        "spongebob.jpg",
        "hello_there.gif",
        "hello_there.gif",
        "hello_there.gif",
        "hello_there.gif",
        "hello_there.gif",
        "hello_there.gif",
        "hello_there.gif",
        "hello_there.gif" #more chances of the hello there gif.
        ]
        pic_name = random.choice(pictures)
        dir = os.path.dirname(os.path.realpath('__file__'))
        pic_path = "pics/"+pic_name
        full_path = os.path.join(dir, pic_path)
        with open(full_path, 'rb') as f:
            picture = discord.File(f)
            await message.channel.send(file=picture)
    await client.process_commands(message)

@client.tree.command(name="ping", description="Get the bot's current latency!")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(f'{int(client.latency * 1000)} ms.')


asyncio.run(main())