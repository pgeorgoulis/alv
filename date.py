from t import Treno

class Date():
    #Take three strings and initialize a date
    def __init__(self, day, start, end):

        d_list = day.split("/")
        self.day = d_list[0]
        self.month = d_list[1]

        #split the time to hours and minutes
        s_list = start.split(":")
        self.start_time = Treno(int(s_list[0]), int(s_list[1]))
        e_list = end.split(":")
        self.end_time = Treno(int(e_list[0]), int(e_list[1]))


    def get_day(self):
        return self.day
    def get_month(self):
        return self.month
    def get_start_time(self):
        return self.start_time
    def get_end_time(self):
        return self.end_time
    def get_full_date(self):
        return self.day+"/"+self.month+"("+self.start_time.time_to_string()+"-"+self.end_time.time_to_string()+")"
