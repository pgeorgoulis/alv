from datetime import datetime
import os
import csv
import re
from date import Date
from timeObj import TimeObj

file_name = "dates.csv"


"""Date manipulation"""
def base60_to_str(minutes):
    base100_mins =  minutes+minutes//60*40
    return f"{base100_mins//100:02}:{base100_mins%100:02}"
#Take a time frame string (12:15-4:00) and split it to two seperate times
def split_time(string):
    result = string.split("-")
    start_time = result[0]
    end_time = result[1]
    return start_time, end_time

#Take a pottential date and split it to 3 strings
def split_date(string):
    result = string.split("(")
    day = result[0]
    #remove the last character: )
    times = result[1].replace(")", "")
    start_time, end_time = split_time(times)
    return day, start_time, end_time

#Gets a list of Time objects and returns the smallest time
def min_time(time_list):
    min_obj = time_list[0]
    min_hour = min_obj.get_hour()
    min_minutes = min_obj.get_minutes()

    for object in time_list:
        if object.get_hour() < min_hour:
            min_obj = object
            min_hour = object.get_hour()
            min_minutes = object.get_minutes()
        if object.get_hour() == min_hour:
            if object.get_minutes() < min_minutes:
                min_obj = object
                min_hour = object.get_hour()
                min_minutes = object.get_minutes()
    return min_obj

#Gets a list of Time objects and returns the bigest time
def max_time(time_list):
    max_obj = time_list[0]
    max_hour = max_obj.get_hour()
    max_minutes = max_obj.get_minutes()

    for object in time_list:
        if object.get_hour() > max_hour:
            max_obj = object
            max_hour = object.get_hour()
            max_minutes = object.get_minutes()
        if object.get_hour() == max_hour:
            if object.get_minutes() > max_minutes:
                max_obj = object
                max_hour = object.get_hour()
                max_minutes = object.get_minutes()
    return max_obj

def time_diff(time1, time2):
    if time2.get_minutes() >= time1.get_minutes():
        new_minutes = time2.get_minutes() - time1.get_minutes()
        new_hour = time2.get_hour() - time1.get_hour()
    else:
        new_minutes = 60 + time2.get_minutes() - time1.get_minutes()
        new_hour = time2.get_hour() - 1 - time1.get_hour()
    #create the time object and return it
    time_obj = TimeObj(new_hour, new_minutes)
    return time_obj

#Get a list of date objects and sort them
#Usses bubble sort
def sort_dates(dates):
    length = len(dates)

    for i in range(length-1):
        for j in range(0, length-i-1):
            j_month = int(dates[j].get_month())
            j_day = int(dates[j].get_day())
            j_hour = dates[j].get_start_time().get_hour()
            j_minutes = dates[j].get_start_time().get_minutes()
            j_plus_month = int(dates[j+1].get_month())
            j_plus_day = int(dates[j+1].get_day())
            j_plus_hour = dates[j+1].get_start_time().get_hour()
            j_plus_minutes = dates[j+1].get_start_time().get_minutes()
            #If they are on the same month(string comparing them is fine)
            #Check the days

            if j_month == j_plus_month:
                if j_day > j_plus_day:
                    dates[j], dates[j+1] = swap(dates[j], dates[j+1])
                elif j_day == j_plus_day:
                    if j_hour > j_plus_hour:
                        dates[j], dates[j+1] = swap(dates[j], dates[j+1])
                    elif j_hour == j_plus_hour:
                        if j_minutes > j_plus_minutes:
                            dates[j], dates[j+1] = swap(dates[j], dates[j+1]) 
            #Else, if the j+1 month is bigger, swap them
            elif j_month > j_plus_month:
                dates[j], dates[j+1] = swap(dates[j], dates[j+1])

    return dates

"""Random Utilities"""

def swap(object_one, object_two):
    return object_two, object_one

def remove_spaces(string):
    return string.replace(" ", "")

#Get a string and check if it matches the date format
def is_date(string):
    #day = '([1-9]|[0-2][0-9]|30|31|)'
    #month = '(1[012]|0?[1-9])'
    #hour_min = '((0?[0-9]|1[0-9]|[2][0-3]|[24])[:]([0-5][0-9]))'
    #time_str = '((morning)|(noon)|(night)|(day))'
    #time = hour_min+'[-]'+hour_min
    #date = '^('+day+'[\/]'+month+'[(]'+time+'[)])'
    #date_v2 = '^('+day+'[\/]'+month+'[(]'+time_str+'[)])'
    valid_date = False
    time_is_word = False
    day_is_word = False

    #Search for the first pattern
    match = re.search(r"^(([1-9]|[0-2][0-9]|30|31|)[\/](1[012]|0?[1-9])[(]((0?[0-9]|1[0-9]|[2][0-3])[:]([0-5][0-9]))[-]((?:24\:00)|((0?[0-9]|1[0-9]|[2][0-3])[:]([0-5][0-9])))[)])", string)
    match_2 = re.search("^(([1-9]|[0-2][0-9]|30|31|)[\/](1[012]|0?[1-9])[(]((morning)|(noon)|(night)|(day))[)])", string)
    match_3 = re.search("^((today)|(tomorrow)|(monday)|(tuesday)|(wednesday)|(thursday)|(friday)|(saturday)|(sunday))[(]((morning)|(noon)|(night)|(day))[)]", string)
    match_4 = re.search("^((today)|(tomorrow)|(monday)|(tuesday)|(wednesday)|(thursday)|(friday)|(saturday)|(sunday))[(]((0?[0-9]|1[0-9]|[2][0-3])[:]([0-5][0-9]))[-]((?:24\:00)|((0?[0-9]|1[0-9]|[2][0-3])[:]([0-5][0-9])))[)]", string)

    if match is not None:
        valid_date = True #Transpose it to bool flag
    elif match_2:
        valid_date = True
        time_is_word = True
    elif match_3:
        valid_date = True
        time_is_word = True
        day_is_word = True
    elif match_4:
        valid_date = True
        day_is_word = True

    #Also check if the end time is bigger than the start time.
    if valid_date and not time_is_word:
        date, start_time, end_time = split_date(string)
        s_list = start_time.split(":")
        e_list = end_time.split(":")
        s_obj = TimeObj(int(s_list[0]), int(s_list[1]))
        e_obj = TimeObj(int(e_list[0]), int(e_list[1]))
        time_obj = time_diff(s_obj, e_obj)

        if time_obj.get_hour() < 0:
            #Then the start time was bigger that the end time
            valid_date = False

    return valid_date, time_is_word, day_is_word

"""Tools for files"""
#Counts the lines of a file
def file_lines():
    with open(file_name, 'r') as file:
        count =0
        for line in file:
            if line != "\n":
                count += 1
        return count

#Returns the name of the file
def get_filename():
    return file_name

#Returns the content of the file in a Dictionary format with the dates as intersection_keys
#and the times as values
#TODO implement it


#Get a name as input and return a list with the date objects the user has entered
# returns 3 elements: 1. The date list, 2. Exit code, 3. Exit message
#Exit codes:
# -1 initial code. Meands no message was assigned
#  0 User found and he has entered dates
#  1 User found but he has not entered dates
#  2 User was not found
def get_users_dates(author):
    with open(file_name, 'r', newline="") as csvfile:
        reader = csv.reader(csvfile, delimiter=",")
        line_count = file_lines()
        user_found = False

        dates_list = []
        message = ""
        exit_code = -1  #shows which instance occured with a number. Used in remove date
        for i in range(line_count):
            #First, find the user
            row = next(reader)
            if row[0] != str(author):
                continue
            else:
                users_line = row
                #Exit the loop after the user is found
                user_found = True
                break

        if user_found is True:
            if len(users_line) == 1:
                message = "User "+author+" has\'t entered any dates."
                exit_code = 1
                return dates_list, exit_code, message
            #If the user is found
            message = "I found the following dates by "+author
            exit_code = 0
            #pop the users name
            users_line.pop(0)

            for date in users_line:
                splitted = split_date(date)
                object = Date(splitted[0], splitted[1], splitted[2])
                dates_list.append(object)
        else:
            message = "User "+author+" was not found in the file"
            exit_code = 2

        return dates_list, exit_code, message

#Get an author and a list of dates to write into the file. 
def write_dates(author:str, dates_list:list, add_flg: bool = False):
    lines = []
    dates_list.insert(0, author)

    with open(get_filename(), 'r', newline="") as csvfile:
        reader = csv.reader(csvfile, delimiter=",")
        #Load the whole file in lines list
        user_found = False
        for row in reader:
            name = row[0]
            if author != name:
                lines.append(row)
            else:
                lines.append(dates_list)
                user_found = True
        #If the user does not exist and the function is called from the
        #add command, add the user and the dates anyway
        if not user_found and add_flg:
            lines.append(dates_list)


    #Rewrite the new file
    with open(get_filename(), 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(lines) 

def get_users_from_file()->list:
    users = []
    with open(get_filename(), 'r', newline="") as csvfile:
        reader = csv.reader(csvfile, delimiter=",")
        for row in reader:
            name = row[0]
            users.append(name)

    return users
#Get a user and a list of date objects. Find if they exist or not in the file
#Used to confirm add_date and remove_date
#Could return a boolean list with each element refaring to the date list
def confirm_add(author, date_list):
    #Call the get users date command.
    users_dates, exit_code, message = get_users_dates(author)
    print_list = []
    #We need the user to exist. So only exit codes 0, 1
    if exit_code == 0:
        #The user was found and he has entered dates.
        for date in date_list:
            date_exists_flag = False
            for u_date in users_dates:
                if date.get_full_date() == u_date.get_full_date():
                    date_exists_flag = True
                    break
            if date_exists_flag:
                print_list.append(f'Date {date.get_full_date()} was added sucessfully')
            else:
                print_list.append(f'Error: Date {date.get_full_date()} was not added')
    elif exit_code == 1:
        for date in date_list:
            print_list.append(f'Error: Date {date.get_full_date()} was not added')
    else:
        return message

    final_string = "\n".join(print_list)
    return final_string

#Takes a list of date strings and an author and checks if the dates still exist in the file
#Returns a string with the get_user_dates exit message if an error occur
#or
#a string message containing all the dates and if they were found or not. 

def confirm_remove(author:str, deleted_dates) -> str:
    print_list = []

    users_dates, exit_code, message = get_users_dates(author)
    if exit_code == 0:
        for date in deleted_dates:
            date_exists_flag = False
            for u_date in users_dates:
                if date == u_date.get_full_date():
                    date_exists_flag = True
                    break
            if date_exists_flag:
                print_list.append(f'Error: Date {date} was not deleted')
            else:
                print_list.append(f'Date {date} was deleted succesfully')
        
        final_str = "\n".join(print_list)
    else:
        final_str = message

    return final_str


"""Utils for finding dates"""


#Gets as input a list of user objects
#Returns a list of date objects that are common in the entered users
#If the first comparison fails it could end without scanning throughout all the users
def find_common_days(users_list: list):
    formatted_data = []
    #Format all the user dates in a specific way
    for user in users_list:
        user_dates, exit_code, message = get_users_dates(user)
        user_dates = sort_dates(user_dates)
        if exit_code !=0:
            print("Exit code was not 0 inside find_common_days") 
            return     
        date_dictionary = {}
        for entry in user_dates:
            date = entry.get_day()+"/"+entry.get_month()
            time = tuple()
            time = (entry.get_start_time().base60(), entry.get_end_time().base60())

            if date in date_dictionary:
                date_dictionary[date].append(time)
            else:
                #Typple of 2 elements inside a time list for that date with possible multiple entries
                time_list = [time]
                date_dictionary[date] = time_list
        formatted_data.append(date_dictionary)

    #Now that the dates are formatted, it's easy to find the common ones.
    common_keys = set(formatted_data[0].keys())
    for dic in formatted_data[1:]:
        common_keys.intersection_update(set(dic.keys()))
    for d in formatted_data:
        for key in list(d.keys()):
            if key not in common_keys:
                d.pop(key)

    return common_keys, formatted_data

#Gets as input a list of date objects
#(Obviously the common_dates function is called first)
#Returns a list of date objects
#All the final common date and time objects. Basically what find meeting print

def find_common_times(common_keys: set, formated_dates: list, duration: int = None) -> list:
    meetings = []
    for key in common_keys:
        print(key)
        busy_times_list = []
        for dic in formated_dates:
            #find the busy hours
            time_list = dic.get(key)
            busy_time = [True] * 1441
            for (s,e) in time_list:
                for i in range(s,e):
                    #All the remaiing True fieds will be unusable busy time slots
                    busy_time[i] = False
        #By now, the busy minutes of one day for one user are found. 
            busy_times_list.append(busy_time)
        
        #for every users times
        free_time = [True]*1441
        for busy_mins in busy_times_list:
            for i in range(0,1441):
                if busy_mins[i] is True:
                    free_time[i] = False
        openInterval = False
        beg, end = 0, 0
        for i, slot in enumerate(free_time):
            if not openInterval and slot:
                openInterval = True
                beg = i
            elif openInterval and not slot:
                openInterval = False
                end = i
                beg = base60_to_str(beg)
                end = base60_to_str(end)
                #Create the meeting date
                dateObj = Date(key, beg, end)
                print(f'The date obj is {dateObj.get_full_date()}')
                time_diffObj = time_diff(dateObj.get_start_time(), dateObj.get_end_time())
                if duration == None:
                    meetings.append(dateObj)
                else:
                    if time_diffObj.get_hour() >= duration:
                        meetings.append(dateObj)
    return meetings

#This function gets called every time the find_meeting does.
#Gets a list of users and removes from the dates.csv file any of their dates that have passed
#When the new dates are rewritten into the file they should be sorted
def purge_dates(channel_users):
    cur_day = datetime.today().day
    cur_month = datetime.today().month

    new_file = []
    for user in channel_users:
        users_dates, exit, message = get_users_dates(user)
        temp_list = []
        temp_list.append(user)
        if exit == 0:
            users_dates = sort_dates(users_dates)
            for entry in users_dates:
                month = int(entry.get_month())
                day = int(entry.get_day())
                if month == cur_month:
                    if day >= cur_day:
                        temp_list.append(entry.get_full_date())
                elif month > cur_month:
                    temp_list.append(entry.get_full_date())
        #TODO replace all the writting to the file here and in the show_and_remove with a seperate function. Also, optimize this solution
        new_file.append(temp_list)

    #Read the file and add all the users that werent in channel_users back into the file. 
    with open(get_filename(), 'r', newline="") as csvfile:
        reader = csv.reader(csvfile, delimiter=",")
        for row in reader:            
            user_name = row[0]
            if user_name not in channel_users:
                new_file.append(row)


    with open(get_filename(), 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(new_file)