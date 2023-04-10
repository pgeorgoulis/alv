import os
import discord
from discord import app_commands
from discord.ext.commands import Cog
from discord.ext.commands import MissingPermissions
from discord.ext.commands import command



class Cogs(Cog):
    """Loads, Unloads or Reloads one or more cog files"""

    COG_EMOJI=":gear:"

    def __init__(self, client):
        self.client = client

    def check_if_it_is_me(interaction: discord.Interaction) -> bool:
        return str(interaction.user.id) == os.getenv('MY_ID')

    @app_commands.check(check_if_it_is_me)
    @app_commands.command(name="cog", description="Load, Unload or Reload a cog file.")
    async def cog(self, interaction: discord.Interaction, action: str, path: str=None):
        
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
                    await self.client.unload_extension(cog_file)
                    await self.client.load_extension(cog_file)
                    await interaction.response.send_message(f'RELOADED: cogs.{path}')
                elif action == "load":
                    await self.client.load_extension(cog_file)
                    await interaction.response.send_message(f'LOADED: cogs.{path}')
                elif action == "unload":
                    await self.client.unload_extension(cog_file)
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
                        await self.client.unload_extension(file)
                        await self.client.load_extension(file)
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


async def setup(client):
    await client.add_cog(Cogs(client))