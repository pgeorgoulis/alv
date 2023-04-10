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


@client.tree.command(name="cog", description="Load, Unload or Reload a cog file.")
@commands.guild_only()
@commands.is_owner()
async def cog(interaction: discord.Interaction, action: str, path: str=None):
    
    if path:
        if path.endswith(".py"):
            path = path[:-3]

        cog_names = []
        for filename in os.listdir(f'./cogs'):
            if filename.endswith(".py"):
                cog_names.append(filename[:-3])
        
        if path in cog_names:
            cog_file = f'cogs.{path}'
            if action == "reload":
                await client.unload_extension(cog_file)
                await client.load_extension(cog_file)
                await interaction.response.send_message(f'RELOADED: cogs.{path}')
            elif action == "load":
                await client.load_extension(cog_file)
                await interaction.response.send_message(f'LOADED: cogs.{path}')
            elif action == "unload":
                await client.unload_extension(cog_file)
                await interaction.response.send_message(f'UNLOADED: cogs.{path}')
            else:
                await interaction.response.send_message("Incorrect argument received: [action]") 
        else: 
            await interaction.response.send_message(f'There is no cog named: ```{path}``` ')                    

    else:
        if action == "reload":
            counter = 0
            for filename in os.listdir(f'./cogs'):
                if filename.endswith(".py"):
                    counter += 1
                    file = f'cogs.{filename[:-3]}'
                    await client.unload_extension(file)
                    await client.load_extension(file)
            await interaction.response.send_message(f'RELOADED: {counter} Cogs')
        elif action == "load" or action == "unload":
            await interaction.response.send_message("You must provide a valid path in order to use ```load``` or ```unload``` actions")
        else:
            await interaction.response.send_message("Incorrect argument received: [action]")


@cog.error
async def cog_error(self, ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.send("This command is only available to sigma males")
    else:
        raise error

asyncio.run(main())