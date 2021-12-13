import os
import csv
import re

file_name = "dates.csv"


#Take a pottential date and split it to 3 strings
def split_date(string):
    result = string.split("(")
    day = result[0]
    #remove the last character: )
    times = result[1].replace(")", "")
    times = times.split("-")
    time1 = times[0]
    time2 = times[1]
    return day, time1, time2


def remove_spaces(string):
    return string.replace(" ", "")

#convert a list to a string
def to_string(list):
    return ' '.join(str(elem) for elem in list)

#Get a string and check if it matches the date format
def is_date(string):
    pattern='(([1-9]|[0-3][0-9])([(]([1-9]|[0-1][0-9]|[2][0-3]):[0-5][0-9]-([1-9]|[0-1][0-9]|[2][0-3]):[0-5][0-9][)]),?)+'
    result = re.match(pattern, string)
    return result

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
