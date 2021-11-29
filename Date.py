class Date:
    def __init__(day, start_time, end_time):
        self.day = days
        self.start_time = start_time
        self.end_time = end_time

    def unite(day, time1, time2):
        string = day+"("+time1+"-"+time2+")"
        return string

    def split_string(string):
        result = string.split("(")
        day = result[0]
        #remove the last character: )
        times = result[1][-1]
        times = times.split("-")
        time1 = times[0]
        time2 = times[1]
        return day, time1, time2

    #Get a list convert to string, rewrite it to a specific format to filter out user retardedness
    def format_input(list):
        print(f'The temp list is:{list}')
        temp_string = to_string(list)
        print(f'The temp string is:{temp_string}')

        formated_input = temp_string.lower().replace(" ", "")
        print(formated_input)

        pattern='(([1-9]|[0-3][0-9])([(]([1-9]|[0-1][0-9]|[2][0-3]):[0-5][0-9]-([1-9]|[0-1][0-9]|[2][0-3]):[0-5][0-9][)]),?)+'
        result = re.match(pattern, formated_input)
        list=formated_input.split(",")
        return result, list

    #convert a list to a string
    def to_string(list):
        return ' '.join(str(elem) for elem in list)
