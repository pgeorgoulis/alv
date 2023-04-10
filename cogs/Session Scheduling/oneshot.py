
from discord import Embed
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Cog
import discord
import utils


class Oneshot(Cog):
    def __init__(self, client):
        self.client = client

    @app_commands.command(name="oneshot", description="Shows how many members are available on each one of the Dm's entered dates.")
    async def oneshot(self, interaction:discord.Interaction, member:discord.Member = None):
        #TODO for some reason if member is swiched with Dm, the bot breaks
        Dm = member
        default_dm = str(interaction.user)

        if(Dm == None):
            oneshot_dm = default_dm   
        else:
            oneshot_dm = str(Dm)   
        
        
        dm_dates, exit_code, exit_message = utils.get_users_dates(oneshot_dm)
        if exit_code != 0:
            #TODO change this to be printed at the top of the final string on the embed. Same goes for the other commands with this logic
            await interaction.channel
            return

        users = []
        #TODO need to add a away for non members to participate and add dates. 
        for m in interaction.guild.members:
            users.append(str(m))

        common_days = []
        for date_obj in dm_dates:
            dm_date = date_obj.get_day()+"/"+date_obj.get_month()
            date_counter = 0
            for user in users:
                #find in users dates the current date and see if they have it in common. 
                user_dates, e_code, e_message = utils.get_users_dates(user)
                if e_code == 0:
                    for u_date_obj in user_dates:
                        u_date = u_date_obj.get_day()+"/"+u_date_obj.get_month()
                        if u_date == dm_date:
                            date_counter = date_counter + 1
                            break
            common_days.append((date_obj, date_counter))
       
                #If they do add a counter next to the date

                #repeat for all the users and all the dates.

        string = ""
        for d, count in common_days:
            string = string + d.get_full_date() + ":"+ "\t\t"+str(count) +"\n"
        
        embed = Embed(title="One shot availability",description="Number of available party members per DM's entered date", colour=0x87CEEB)
        embed.add_field(name="Dm", value=oneshot_dm, inline=False)
        embed.add_field(name="Results", value=string, inline=False)

        await interaction.response.send_message(embed=embed)




async def setup(client):
    await client.add_cog(Oneshot(client))