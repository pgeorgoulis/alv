from discord import Embed
from discord.ext.commands import Cog
from discord import app_commands
import discord
from date import Date
import utils


class Statistics(Cog):

    def __init__(self, client):
        self.client = client

    @app_commands.command(name="stats", description="Shows information about the users and all their entered dates")
    async def stats(self, interaction: discord.Interaction):
        channel_users = []
        for membr in interaction.channel.members:
            channel_users.append(str(membr))

        channel_users.remove("Alv#3487")

        #purge the dates
        utils.purge_dates(channel_users)

        #channel_users.remove("pr#8877")
        #channel_users.remove("katiaa#7311")
        #TODO search for those users  and remove them if they exist
        #Get all the dates from the channel users
     
        last_date = ""
        first_date = ""
        date_count = ""
        all_sets=[]
        for user in channel_users:
            user_dates, exit_code, message = utils.get_users_dates(user)
            user_dates = utils.sort_dates(user_dates)

            #Mporei na einai adeio
            #TODO find out what happens then
            
            dates_set = set() #The set will ingore duplicate dates
            for entry in user_dates:
                date = entry.get_day() + "/" + entry.get_month()

                dates_set.add(date)
            count = str(len(dates_set))
            all_sets.append(dates_set)

            
            #Find the last date for each user and add them into a string. 
            if exit_code !=0: #If the user wasn't found or hasnt entered any dates
                ld_string = user[0:-5] + ": "+" - "+"\n"
                fd_string = user[0:-5] + ": "+" - "+"\n"
                count_string = user[0:-5] + ": "+" - "+"\n" 
            else:
                last_day = user_dates[-1].get_day()
                last_month = user_dates[-1].get_month()
                ld_string = user[0:-5] + ": "+ last_day+"/"+last_month+"\n"
                fd_string = user[0:-5] + ": "+user_dates[0].get_day()+"/"+user_dates[0].get_month()+"\n"
                count_string = user[0:-5] + ": "+ count +"\n" 
            
            first_date = first_date + fd_string
            last_date = last_date + ld_string
            date_count = date_count + count_string #TODO this is a bad way to do this.



        common_days = set.intersection(*all_sets)
        #Print some stats about the dates using formated_dates, the set of dictionaries from above
        if len(common_days) == 0:
            common_string = "0 common days found"
        elif len(common_days) == 1:
            common_string = "1 common day found:\n"
            #TODO find a workaround without the loop to get the only one set element
            for date in common_days:
                common_string = common_string + date
        else:
            common_string = str(len(common_days)) + " common days found:\n"
            common_dates_string = ""
            for date in common_days:
                common_dates_string = common_dates_string + date + "\n"
            common_string = common_string + common_dates_string

        #Create the embed with the stats and send it at the end       
        embed = Embed(title="Statistics", 
                                description="Stats about each user's entered dates", 
                                color =0x0CC10C)        
        embed.add_field(name="First Date", value=first_date, inline=True)
        embed.add_field(name="Last Date", value=last_date, inline=True)
        embed.add_field(name="Number of entered Dates", value=date_count, inline=False)
        embed.add_field(name="Common Days", value=common_string, inline=False)

        await interaction.response.send_message(embed=embed)

async def setup(client):
    await client.add_cog(Statistics(client))