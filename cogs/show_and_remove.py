import discord
from discord.ext import commands
from discord import app_commands
from date import Date
import asyncio
import csv
import utils
from discord.ui import Select
from discord.ui import View

class RemoveDatesDropdown(Select):
    def __init__(self, options:list[discord.SelectOption], date_count:int):
        super().__init__(placeholder="Choose one or more dates to be removed", min_values=1, max_values=date_count, options=options)

    async def callback(self, interaction: discord.Interaction):
        dates_list = [f"{option.label}" for option in self.options]

        #Remove the dates from the list
        for date in self.values:
            dates_list.remove(date)

        #Rewrite the file with the new dates
        #TODO I may need to rewrite this. It should't be here

        lines = []
        author = str(interaction.user)
        dates_list.insert(0, author)
        with open(utils.get_filename(), 'r', newline="") as csvfile:
            reader = csv.reader(csvfile, delimiter=",")
            #Load the whole file in lines list
            for row in reader:
                name = row[0]
                #rows.append(row)
                if author != name:
                    lines.append(row)
                else:
                    lines.append(dates_list)
        #Rewrite the new file
        with open(utils.get_filename(), 'w') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(lines) 

        await interaction.response.edit_message(view=None)
        message = utils.confirm_twice(author, self.values)
        await interaction.followup.send(message)
        if self.view:
            self._view.stop()

class RemoveDatesView(View):
    def __init__(self, options: list[discord.SelectOption], date_count:int):
        super().__init__()
        self.add_item(RemoveDatesDropdown(options=options, date_count=date_count))

    async def on_timeout(self):
        return await super().on_timeout()
    

class Show_and_remove(commands.Cog):

    def __init__(self, client):
        self.client = client


    @app_commands.command(name="show", description="Shows the dates from any user")
    async def show(self, interaction:discord.Interaction, member:discord.Member = None):

        default_user = str(interaction.user)

        if(member == None):
            user = default_user
        else:
            user = str(member)

        dates_list, exit_code, message = utils.get_users_dates(user)
        #Only if the error code is 0 print the dates. Else, there aren't any dates to print
        final_string = ""
        if exit_code == 0:
            dates_list = utils.sort_dates(dates_list)
            #Initialize the counter
            i=1
            for date in dates_list:
                temp = str(i)+". "+ date.get_full_date() +"\n"
                final_string += temp
                i+=1
            await interaction.response.send_message(message+"\n"+final_string)
        else:
            await interaction.response.send_message(message)


    @app_commands.command(name="remove", description="Choose and remove one or more dates")
    async def remove(self, interaction:discord.Interaction):
        #Show the dates to the user
        author = str(interaction.user)
        dates_list, exit_code, message = utils.get_users_dates(author)

        #Only if the error code is 0 print the dates.
        if exit_code == 0:
            #Initialize the counter
            dates_list = utils.sort_dates(dates_list)
            options = []
            date_count = 1
            for date in dates_list:
                options.append(discord.SelectOption(label=date.get_full_date()))
            date_count = len(options)
            await interaction.response.send_message("Select the dates you wish to remove", view=RemoveDatesView(options=options, date_count=date_count), ephemeral=True)
        else:
            await interaction.response.send_message(message)
            return




async def setup(client):
    await client.add_cog(Show_and_remove(client))
