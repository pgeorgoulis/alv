from discord.ext import commands
from discord import app_commands
from date import Date
from datetime import datetime, timedelta
import asyncio
import utils
from discord.ext import commands


class Add_date(commands.Cog):

    def __init__(self, client):
        self.client = client


    #Use add date to add a available date as a user
    @app_commands.command(name="add", description="Adds up to 9 dates")
    async def add(self, interaction, date1:str, date2:str=None, date3:str=None, date4:str=None, date5:str=None, date6:str=None, date7:str=None, date8:str=None, date9:str=None):
        
        temp_list = [date1, date2, date3, date4, date5, date6, date7, date8, date9]
        input_list =[]
        for entry in temp_list:
            if entry:
                input_list.append(entry)

        author = str(interaction.user)

        #Get the users dates to avoid duplicates in dates.csv
        users_dates, ex_code, message = utils.get_users_dates(author)
        
        list_to_write = []
        list_to_confirm = []
        message_list = []

        #Create a date object for every date in the input string
        for entry in input_list:
            entry = utils.remove_spaces(entry.lower())
            valid_date, time_is_word, day_is_word = utils.is_date(entry)
            if valid_date:
                result = entry.split("(")
                day = result[0]
                if day_is_word:
                    if day == "today":
                        date = datetime.today()
                        m = str(date.month)
                        d = str(date.day)
                        day = d+"/"+m
                    elif day == "tomorrow":
                        date = datetime.today() + timedelta(days=1)
                        m = str(date.month)
                        d = str(date.day)
                        day = d+"/"+m
                    else:
                        for i in range(1,7):
                            date = datetime.today() + timedelta(days=i)
                            day_name = date.strftime("%A").lower()
                            if day_name == day:
                                m = str(date.month)
                                d = str(date.day)
                                day = d+"/"+m
                                break
                else:
                    #Remove possible zeroes in front of the dates. For example 02/09(noon) -> 2/9(noon)
                    date_l = day.split("/")
                    d = date_l[0]
                    m = date_l[1]
                    if d[0] == '0':
                        d = d[1:]
                    if m[0] == '0':
                        m = m[1:]
                    day = d + "/" + m
                if time_is_word:
                    #remove the last character: )
                    time = result[1].replace(")", "")
                    if time == "morning":
                        start_time = "11:30"
                        end_time = "15:30"
                    elif time == "noon":
                        start_time = "17:00"
                        end_time = "22:00"
                    elif time == "night":
                        start_time = "20:00"
                        end_time = "24:00"
                    elif time =="day":
                        start_time = "9:00"
                        end_time = "24:00"
                else:
                    attributes = utils.split_date(entry)
                    start_time = attributes[1]
                    end_time = attributes[2]
                
                obj = Date(day, start_time, end_time)

                #Now that obj is created check if obj.time overlaps with another one in the file.
                #exit code 0 -> Dates were found. exit code 1 -> User was found but he hasn't entered any dates
                overlap_flag = False
                if ex_code !=0 and ex_code != 1:
                    await interaction.channel.send("Warning: Date and time overlap check was skipped")
                else:
                    for written_date in users_dates:
                        same_day = bool(int(written_date.get_day()) == int(obj.get_day()))
                        if same_day:
                            #Check if it's the same month but also save time in comparisons
                            same_month = bool(int(written_date.get_month()) == int(obj.get_month()))
                            if same_month:
                                #existing start and end times
                                existing_start = written_date.get_start_time().get_hour()
                                existing_end = written_date.get_end_time().get_hour()
                                #current object waiting to be written
                                new_start = obj.get_start_time().get_hour()
                                new_end = obj.get_end_time().get_hour()
                                #Conditions to check if there is overlap between the time periods
                                overlap_one = bool(new_start < existing_start and new_end > existing_end)
                                overlap_two = bool(new_start < existing_end and new_start > existing_start)
                                overlap_three = bool(new_start == existing_start or new_end == existing_end)
                                if overlap_one or overlap_two or overlap_three:
                                    overlap_flag = True
                                    break
                                if new_start == existing_end:
                                    if obj.get_start_time().get_minutes() <= written_date.get_start_time().get_minutes():
                                        overlap_flag = True
                                        break
                                if new_end == existing_start:
                                    if obj.get_end_time().get_minutes() >= written_date.get_start_time().get_minutes():
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
        for date in users_dates:
            list_to_write.append(date.get_full_date())
        utils.write_dates(author, list_to_write, add_flg=True)
        message= utils.confirm_add(author, list_to_confirm)

        error_msg = "\n".join(message_list)
        final_str = message + "\n" +error_msg
        await interaction.response.send_message(final_str)



async def setup(client):
    await client.add_cog(Add_date(client))
