import os
import csv
import re

file_name = "dates.csv"

def get_filename():
    return file_name

#Take a pottential date and split it to 3 strings
def split_date(string):
    result = string.split("(")
    day = result[0]
    #remove the last character: )
    times = result[1].replace(")", "")
    start_time, end_time = split_time(times)
    return day, start_time, end_time

def split_time(string):
    result = string.split("-")
    start_time = result[0]
    end_time = result[1]
    return start_time, end_time

#takes a list of dates and parses it to day and time. Then, it adds the
#day to a dictionary as the key and the time as the value
def date_parser(list_dates):
    dictionary = {}
    for date in list_dates:
        #parse the date and assing it to the dictionary
        date, start_time, end_time = split_date(date)
        dictionary[date] = start_time + "-" + end_time
    return dictionary

#returns a list of common values
def intersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return lst3

def remove_spaces(string):
    return string.replace(" ", "")

#convert a list to a string
def to_string(list):
    return ' '.join(str(elem) for elem in list)

#Get a string and check if it matches the date format
def is_date(string):
    #TODO split the pattern to subpatterns day, time
    pattern='(([1-9]|[0-3][0-9])([(]([1-9]|[0-1][0-9]|[2][0-3]):[0-5][0-9]-([1-9]|[0-1][0-9]|[2][0-3]):[0-5][0-9][)]),?)+'
    result = re.match(pattern, string)
    return result

def file_lines():
    with open(file_name, 'r') as file:
        count =0
        for line in file:
            if line != "\n":
                count += 1
        return count

#Find the max element of a list
## TODO: convert the list to integers
def max(list):
    max = list[0]
    for number in list:
        if number > max:
            max = number
    return max
#find the min element of a list
def min(list):
    min = list[0]
    for number in list:
        if number < min:
            min = number
    return min

#write the dates to a csv file
def writeFile(author, dates):
    lines = list()
    found_flag=False
    with open(file_name, 'r', newline="") as csvfile:
        reader = csv.reader(csvfile, delimiter=",")
        #Load the whole file in lines list
        for row in reader:
            name = row[0]
            print(name)
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
                    print("found", author)
                else:
                    #its only one dates
                    row.append(dates)
                    lines.append(row)
                    found_flag = True
                    print("found", author)

        #If the user does not exist already
        if not found_flag:
            #then add the new user
            print("not found", author)
            dates.insert(0, author)
            lines.append(dates)

    #Rewrite the new file
    with open(file_name, 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(lines)
        return
