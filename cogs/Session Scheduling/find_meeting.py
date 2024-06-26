import os
import utils
import discord
from discord import Embed
from discord.ext import commands
from discord import app_commands
from datetime import datetime


class Find_meeting(commands.Cog):

    def __init__(self, client):
        self.client = client


    @app_commands.command(name = "find_meeting", description="Finds possible meeting times for all the users in the current chat")
    async def find_meeting(self, interaction=discord.Interaction, duration: int = None):

        #Purge the dates from the channel users
        channel_users = []
        for mem in interaction.channel.members:
            channel_users.append(str(mem))
        channel_users.remove("Alv#3487")
        utils.purge_dates(channel_users)
        try:
            common_keys, formatted_dates = utils.find_common_days(channel_users)
        except Exception as e:
            await interaction.response.send_message(e)
            return

        meetings = utils.find_common_times(common_keys, formatted_dates, duration)
        
        if len(meetings) == 0:
            dir = os.path.dirname(os.path.realpath('__file__'))
            pic_path = "/home/porf/Desktop/alv/alv/pics/no_session_.jpg"
            with open(pic_path, 'rb') as f:
                picture = discord.File(f)
                await interaction.response.send_message(file=picture)
        else:
            guild = interaction.guild
            meetings = utils.sort_dates(meetings)
            if len(meetings) == 1:
                await interaction.response.send_message("I found the following date:")
            else:
                await interaction.response.send_message("I found the following dates:")
            for meeting in meetings:
                #Get all the fiends needed
                year = datetime.today().year
                month = int(meeting.get_month())
                day = int(meeting.get_day())
                start = meeting.get_start_time().time_to_string()
                end = meeting.get_end_time().time_to_string()
                string = datetime(year, month, day).strftime("%A")+" "+str(day)+"/"+str(month)

                embed = Embed(title="Possible Session", colour=0x87CEEB)
                embed.add_field(name="Date", value=string, inline=False)
                embed.add_field(name="From", value=start, inline=True)
                embed.add_field(name="Until", value=end, inline=True)
                await interaction.channel.send(embed=embed)

async def setup(client):
    await client.add_cog(Find_meeting(client))