from timeObj import TimeObj

class Date():
    #Take three strings and initialize a date
    def __init__(self, day, start, end):

        d_list = day.split("/")
        self.day = d_list[0]
        self.month = d_list[1]

        #split the time to hours and minutes
        s_list = start.split(":")
        self.start_time = TimeObj(int(s_list[0]), int(s_list[1]))
        e_list = end.split(":")
        self.end_time = TimeObj(int(e_list[0]), int(e_list[1]))


    def get_day(self) -> str:
        return self.day
    def get_month(self) -> str:
        return self.month
    def get_start_time(self) -> TimeObj:
        return self.start_time
    def get_end_time(self) -> TimeObj:
        return self.end_time
    def get_full_date(self) -> str:
        return self.day+"/"+self.month+"("+self.start_time.time_to_string()+"-"+self.end_time.time_to_string()+")"
