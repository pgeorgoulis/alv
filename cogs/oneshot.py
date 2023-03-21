from discord.ext.commands import command
from discord.ext.commands import Cog
from discord import Embed
import utils

class Oneshot(Cog):
    def __init__(self, client):
        self.client = client

    @command(name = "oneshot")
    async def oneshot(self, ctx, dm = None):
        
        if dm == None:
            dm = str(ctx.author)
        else:
            dm_found = False 
            for member in ctx.guild.members:
                if dm in str(member).lower():
                    dm = str(member)
                    dm_found = True
                    break
            if not dm_found:
                print("in")
                dm = str(ctx.author)
                await ctx.send(f'Warning: The dm was not found. Proceeding with user {str(ctx.author)} as a DM instead')
        
        
        dm_dates, exit_code, exit_message = utils.get_users_dates(dm)
        if exit_code != 0:
            await ctx.send(exit_message)
            return

        users = []
        #TODO need to add a away for non members to participate and add dates. 
        for m in ctx.guild.members:
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
        embed.add_field(name="Dm", value=str(dm), inline=False)
        embed.add_field(name="Results", value=string, inline=False)

        await ctx.send(embed=embed)




async def setup(client):
    await client.add_cog(Oneshot(client))