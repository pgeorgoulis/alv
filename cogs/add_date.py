from discord.ext import commands
from date import Date
import asyncio
import utils
from discord.ext import commands


class Add_date(commands.Cog):

    def __init__(self, client):
        self.client = client


    #Use add date to add a available date as a user
    @commands.command()
    async def add(self, ctx):
        await ctx.send('Enter your desired dates, you must')

        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel

        try:
            #Read the user input and split it into seperate days
            msg = await self.client.wait_for("message", check=check, timeout=180)
            input_list = msg.content.lower().split("\n")
            author = str(msg.author)

            list_to_write = []
            list_to_confirm = []
            message_list = []

            #Create a date object for every date in the input string
            for entry in input_list:
                date = utils.remove_spaces(entry)
                valid_date, time_is_word = utils.is_date(date)
                if valid_date:
                    if time_is_word:
                        result = date.split("(")
                        day = result[0]
                        #remove the last character: )
                        time = result[1].replace(")", "")
                        if time == "morning":
                            start_time = "11:30"
                            end_time = "15:30"
                        elif time == "noon":
                            start_time = "15:30"
                            end_time = "20:30"
                        elif time == "night":
                            start_time = "20:30"
                            end_time = "24:00"
                        elif time =="day":
                            start_time = "9:00"
                            end_time = "24:00"

                        obj = Date(day, start_time, end_time)
                        #dates_list.append(obj)
                    else:
                        attributes = utils.split_date(date)
                        #Create the object and append it to the dates_list
                        obj = Date(attributes[0], attributes[1], attributes[2])
                        #dates_list.append(obj)

                    #Test. If its valid, add it to the file
                    list_to_write.append(obj.get_full_date())
                    list_to_confirm.append(obj)
                else:
                    string = f'Error: {entry} is not a valid date. Use !help add to find the correct format'
                    message_list.append(string)

            #Write the dates, check to confirm changes, print the apropriate messages
            utils.writeFile(author, list_to_write)
            found_list, exit_code = utils.confirm_change(author, list_to_confirm)

            if exit_code == 0:
                i=0
                for date in list_to_confirm:
                    if found_list[i]:
                        string = f'Date {obj.get_full_date()} was added succesfully'
                    else:
                        string = f'Error: Date {obj.get_full_date()} was not added. Please try again'
                    message_list.append(string)
                    i+=1
            else:
                await ctx.reply(f'Error: Error in confirm message')
            
            await ctx.reply("\n".join(message_list))

        except asyncio.TimeoutError:
            await ctx.send("Sorry, you didn't reply in time")


async def setup(client):
    await client.add_cog(Add_date(client))
