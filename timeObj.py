class TimeObj():
    #Takes an integer as an hour and another one as minutes
    ## TODO: Change the file and the class name to something more appropriate
    def __init__(self, hour, minutes):
        self.hour = hour
        self.minutes = minutes

    def get_hour(self):
        return self.hour
    def get_minutes(self):
        return self.minutes
    #return the time
    def time_to_string(self):
        if self.minutes < 10:
            minutes_str = "0"+str(self.minutes)
        else:
            minutes_str = str(self.minutes)
        string = str(self.hour)+":"+minutes_str
        return string
