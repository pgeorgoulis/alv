class Treno():
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
        string = str(self.hour)+":"+str(self.minutes)
        return string
