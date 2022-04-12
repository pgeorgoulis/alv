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
            j_plus_month = int(dates[j+1].get_month())
            j_day = int(dates[j].get_day())
            j_plus_day = int(dates[j+1].get_day())
            #If they are on the same month(string comparing them is fine)
            #Check the days

            if j_month == j_plus_month:
                if j_day > j_plus_day:
                    dates[j], dates[j+1]= dates[j+1], dates[j]
            #Else, if the j+1 month is bigger, swap them
            elif j_month > j_plus_month:
                dates[j], dates[j+1]= dates[j+1], dates[j]

    return dates

"""Random Utilities"""

def remove_spaces(string):
    return string.replace(" ", "")

#Get a string and check if it is made out of digits
def is_number(string):
    #one or more numnbers
    digits = '[0-9]+'
    result = re.search(digits, string)
    return result
#Get a string and check if it matches the date format
def is_date(string):
    day = '([1-9]|[0-2][0-9]|30|31)'
    month = '(1[0-2])|(0?[1-9])'
    time = '(0?[0-9]|1[0-9]|[2][0-3]):([0-5][0-9])'
    time2 = 'morning|noon|night|day|'
    pattern = day+'[]\/]'+month+'[(]'+time+'-'+time+'[)]'
    pattern2 = day+'[]\/]'+month+'[(]'+time2+'[)]'
    time_is_word = False
    first_flag = False
    second_flag = False
    first_flag = re.search(pattern, string)
    #Check if the time was entered as a word

    if first_flag is None:
        time_is_word = re.search(pattern2, string)
        if time_is_word:
            result = True
            return result, time_is_word

    #Also check if the end time is bigger than the start time.
    if first_flag and not time_is_word: #If its a valid date
        date, start_time, end_time = split_date(string)
        s_list = start_time.split(":")
        e_list = end_time.split(":")
        s_obj = TimeObj(int(s_list[0]), int(s_list[1]))
        e_obj = TimeObj(int(e_list[0]), int(e_list[1]))

        time_obj = time_diff(s_obj, e_obj)
        if time_obj.get_hour() < 0:
            #Then the start time was bigger that the end time
            second_flag = False
        else:
            second_flag = True

    #AND to make sure that the check passes only if both flags are true
    result = first_flag and second_flag
    return result, time_is_word

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
# returns 1. The date list, 2. Exit code, 3. Exit message
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
                message = "Error: User "+author+" has\'t entered any dates."
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
            message = "Error: User "+author+" was not found in the file"
            exit_code = 2

        return dates_list, exit_code, message


#Get a user and a list of date objects. Find if they exist or not in the file
#Used to confirm add_date and remove_date
#Could return a boolean list with each element refaring to the date list
def confirm_change(author, date_list):
    #Call the get users date command.
    users_dates, exit_code, message = get_users_dates(author)

    found_list = []
    #We need the user to exist. So only exit codes 0, 1
    if exit_code == 0:
        #The user was found and he has entered dates.
        for date in date_list:
            date_found = False
            for u_date in users_dates:
                if date.get_full_date() == u_date.get_full_date():
                    date_found = True
            found_list.append(date_found)

    elif exit_code == 1:
        for date in date_list:
            found_list.append(False)
    else:
        pass #The user was not found in the file so return some error code

    return found_list, exit_code

#write the dates to a csv file
def writeFile(author, dates):
    lines = list()
    found_flag=False
    with open(file_name, 'r', newline="") as csvfile:
        reader = csv.reader(csvfile, delimiter=",")
        #Load the whole file in lines list
        for row in reader:
            name = row[0]
            #rows.append(row)
            if author != name:
                lines.append(row)
            else:
                #if the user entered multiple dates
                if type(dates) is list:
                    #get the line and append it at the end
                    for string in dates:
                        row.append(string)
                    lines.append(row)
                    found_flag = True
                    #TODO might need to remove the break
                    break
                else:
                    #its only one dates
                    row.append(dates)
                    lines.append(row)
                    found_flag = True
                    break

        #If the user does not exist already
        if not found_flag:
            #then add the new user
            new_line = []
            new_line.append(author)
            new_line.append(dates)

            lines.append(new_line)

    #Rewrite the new file
    with open(file_name, 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(lines)
        return
