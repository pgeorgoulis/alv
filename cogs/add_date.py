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

            #Get the users dates to avoid duplicates in dates.csv
            users_dates, ex_code, message = utils.get_users_dates(author)
            
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
                    else:
                        attributes = utils.split_date(date)
                        obj = Date(attributes[0], attributes[1], attributes[2])

                    #Now that obj is created check if obj.time overlaps with another one in the file.
                    #exit code 0 -> Dates were found. exit code 1 -> User was found but he hasn't entered any dates
                    overlap_flag = False
                    if ex_code !=0 and ex_code != 1:
                        await ctx.send("Warning: Date and time overlap check was skipped")
                    else:
                        for written_date in users_dates:
                            same_day = bool(int(written_date.get_day()) == int(obj.get_day()))
                            if same_day:
                                #Check if it's the same month but also save time in comparisons
                                same_month = bool(int(written_date.get_month()) == int(obj.get_month()))
                                if same_month:
                                    wr_start = written_date.get_start_time().get_hour()
                                    wr_end = written_date.get_end_time().get_hour()
                                    obj_start = obj.get_start_time().get_hour()
                                    obj_end = obj.get_end_time().get_hour()
                                    #Conditions to check if there is overlap between the time periods
                                    overlap_one = bool(obj_start < wr_start and obj_end > wr_end)
                                    overlap_two = bool(obj_start < wr_end and obj_start > wr_start)
                                    overlap_three = bool(obj_start == wr_start or obj_end == wr_end)
                                    if overlap_one or overlap_two or overlap_three:
                                        overlap_flag = True
                                        break
 
                    if overlap_flag: 
                        string = f'Error: Date {obj.get_full_date()} overlaps with existing date {written_date.get_full_date()}'
                        message_list.append(string)
                    else:       
                        #Test. If its valid, add it to the file
                        list_to_write.append(obj.get_full_date())
                        list_to_confirm.append(obj)

                else:
                    string = f'Error: {entry} is not a valid date. Use `!help add` to find the correct format'
                    message_list.append(string)

            #Write the dates, check to confirm changes, print the apropriate messages
            utils.writeFile(author, list_to_write)
            found_list, exit_code = utils.confirm_change(author, list_to_confirm)

            if exit_code == 0:
                i=0
                for date in list_to_confirm:
                    if found_list[i]:
                        string = f'Date {date.get_full_date()} was added succesfully'
                    else:
                        string = f'Error: Date {date.get_full_date()} was not added. Please try again'
                    message_list.append(string)
                    i+=1
            else:
                await ctx.reply(f'Error: Error in confirm message')
            
            await ctx.reply("\n".join(message_list))

        except asyncio.TimeoutError:
            await ctx.send("Sorry, you didn't reply in time")


async def setup(client):
    await client.add_cog(Add_date(client))
