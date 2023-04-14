import discord
from typing import Optional
from discord.ext import commands
from discord import app_commands



class Help(commands.Cog):
    def __init__(self, client) -> None:
        self.client = client

    @app_commands.command(name="help", description="Shows help and information about all the commands")
    async def help(self, interaction: discord.Interaction):
        
        embed ="string"
        
        await interaction.response.send_message(embed=embed)

    async def _help_embed(self, title: str, description: Optional[str] = None, set_author: bool = False):
        embed = discord.Embed(title=title)
        if description:
            embed.description = description
        if set_author:
            #TODO find a way to add the avatar
            #avatar = self.context.bot.user.avatar or self.context.bot.user.default_avatar
            #embed.set_author(name=self.context.bot.user.name, icon_url=avatar.url)
            pass
        