import discord
from discord.ext import commands
import utils


class Statistics(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def stats(self, ctx):

        channel_users = []
        for membr in ctx.channel.members:
            channel_users.append(str(membr))

        channel_users.remove("Alv#3487")
        #channel_users.remove("pr#8877")
        #channel_users.remove("katiaa#7311")
        #TODO search for those users  and remove them if they exist
        #Get all the dates from the channel users
        
        last_date_string = ""
        for user in channel_users:
            user_dates, exit_code, message = utils.get_users_dates(user)
            user_dates = utils.sort_dates(user_dates)
            if exit_code !=0: #If the user wasn't found or hasnt entered any dates
                string = user[0:-5] + ": "+" - "+"\n"
            else:
                last_day = user_dates[-1].get_day()
                last_month = user_dates[-1].get_month()
                string = user[0:-5] + ": "+ last_day+"/"+last_month+"\n"
            last_date_string = last_date_string + string

        embed = discord.Embed(title="Statistics", description="Stats about each user's entered dates", color =0x0CC10C)        
        embed.add_field(name="Last Date", value=last_date_string, inline=False)
        await ctx.send(embed=embed)

async def setup(client):
    await client.add_cog(Statistics(client))