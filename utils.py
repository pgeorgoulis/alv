import os
import csv
import re
from date import Date
from t import Treno

file_name = "dates.csv"


"""Date manipulation"""
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

#takes a list of dates and parses it to day and time. Then, it adds the
#day to a dictionary as the key and a list of two time objects as the value
def date_parser(list_dates):
    dictionary = {}
    for date in list_dates:
        #parse the date and asign it to the dictionary
        date, start_time, end_time = split_date(date)
        date_obj = Date(date, start_time, end_time)
        times_list = [date_obj.get_start_time(), date_obj.get_end_time()]
        dictionary[date_obj.get_day()] = times_list
    return dictionary

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
    time_obj = Treno(new_hour, new_minutes)
    return time_obj

"""Random Utilities"""

def remove_spaces(string):
    return string.replace(" ", "")

#Get a string and check if it matches the date format
def is_date(string):
    day = '([1-9]|[0-2][0-9]|30|31)'
    month = '(1[0-2])|(0?[1-9])'
    time = '(0?[0-9]|1[0-9]|[2][0-3]):([0-5][0-9])'
    pattern = day+'[]\/]'+month+'[(]'+time+'-'+time+'[)]'
    result = re.search(pattern, string)
    return result

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
                    break
                else:
                    #its only one dates
                    row.append(dates)
                    lines.append(row)
                    found_flag = True
                    break

        #If the user does not exist already
        ## TODO: FIX This. It does not work when the user does not exist.
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
