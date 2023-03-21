from datetime import datetime, timedelta

from discord import AllowedMentions, Embed
from discord.ext.commands import Cog
from discord import app_commands
import discord


numbers = ("1️⃣", "2⃣", "3⃣", "4⃣", "5⃣",
		   "6⃣", "7⃣", "8⃣", "9⃣")


class Poll(Cog):
    def __init__(self, client):
        self.client = client

    @app_commands.checks.has_permissions(manage_messages=True)
    @app_commands.command(name="poll", description="Creates a poll")
    async def poll(self, interaction: discord.Interaction, question: str, option1: str, option2: str, option3: str = None, option4: str = None, option5: str = None, option6: str = None, option7: str = None, option8: str = None, option9: str = None):

        entry_list = [option1, option2, option3, option4, option5, option6, option7, option8, option9]
        options = []
        for entry in entry_list:
            if entry:
                options.append(entry)


        allowed_mentions = AllowedMentions(everyone=True)
        await interaction.response.send_message("@everyone new poll", allowed_mentions=allowed_mentions)
        embed = Embed(title="Poll",
                        description=question,
                        colour=0xEB459E,
                        timestamp=datetime.now())
        
        fields = [("Options", "\n".join([f"{numbers[idx]} {option}" for idx, option in enumerate(options)]), False), 
        ("Instructions", "React to cast a vote!", False)]

        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)

        message = await interaction.channel.send(embed=embed)

        print(type(message))

        for emoji in numbers[:len(options)]:
            await message.add_reaction(emoji)
            
        

            

async def setup(client):
    await client.add_cog(Poll(client))