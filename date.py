class Date():
    def __init__(self, day, start_time, end_time):
        self.day = day
        self.start_time = start_time
        self.end_time = end_time

    def unite(self, day, time1, time2):
        string = day+"("+time1+"-"+time2+")"
        return string

    def get_date(self):
        string = self.unite(self.day, self.start_time, self.end_time)
        return string
