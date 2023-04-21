import utils
import os
import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import MissingPermissions

class Admin(commands.Cog):

    def __init__(self, client):
        self.client = client

    def check_if_it_is_me(interaction: discord.Interaction) -> bool:
        return str(interaction.user.id) == os.getenv('MY_ID')

    @app_commands.check(check_if_it_is_me)
    @app_commands.command(name="string")
    async def say(self, interaction:discord.Interaction, string:str):
        
        await interaction.channel.send(string)
        await interaction.response.send_message("Done", ephemeral=True)
    
    @app_commands.check(check_if_it_is_me)
    @app_commands.command(name="get_logs", description="Get the last \'limit\'logs from the file. Default limit value is 50")
    async def get_logs(self, interaction: discord.Interaction, limit: int = 20):
        lines = []
        with open("logs.txt", 'r') as file:
            lines = file.readlines()
        if len(lines) < limit:
            string = f"Warning: There are only {len(lines)} entries in the log file\n\n"
        else:
            string = f"Here are the last {limit} entries in the file\n\n"    
        file_content = "".join(lines[:limit])
        final_str = string + file_content
        await interaction.response.send_message(final_str, ephemeral=True)

    #Alternatively @commands.has_role('RoleName')
    @commands.command(pass_context = True)
    @commands.has_permissions(administrator=True)   #Raises some subclass CommandError
    async def delete(self, ctx, number):
        num = int(number)
        await ctx.channel.purge(limit=num+1)
        await ctx.send("Messages deleted", delete_after = 5)

    @delete.error
    async def delete_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            await ctx.send("This command is only available to sigma males")
        else:
            raise error

async def setup(client):
    await client.add_cog(Admin(client))
