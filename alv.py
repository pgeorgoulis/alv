# bot.py
import os
import asyncio
import random
import discord
import discord.ext
from dotenv import load_dotenv
from discord.ext import commands
from discord.ext.commands import MissingPermissions


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('SERVER_ID')

intents = discord.Intents.all()
client = commands.Bot(command_prefix='!', intents=intents)
client.remove_command('help')
#Global variables for the file name and size

async def load_extensions():
    for filename in os.listdir('./cogs'):
        if filename.startswith('help_command.py'):
            continue
        #remove the help_command class
        if filename.endswith('.py'):
            await client.load_extension(f"cogs.{filename[:-3]}") #:-3] remove the .py

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

    print("[+] Alv is running...")
    print("[+] Slash Commands synced: "+ str(len(synced))+" commands")


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