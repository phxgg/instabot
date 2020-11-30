import datetime

class Logger:
    current_time = datetime.datetime.now()

    def __init__(self, debugEnabled):
        self.debugEnabled = debugEnabled

    def info(self, text):
        self.updateTime()
        print('[INFO: ' + str(self.current_time.hour) + ':' + str(self.current_time.minute) + ':' + str(self.current_time.second) + '] ' + text)

    def error(self, text):
        self.updateTime()
        print('[ERROR: ' + str(self.current_time.hour) + ':' + str(self.current_time.minute) + ':' + str(self.current_time.second) + '] ' + text)
    
    def debug(self, text):
        if self.debugEnabled:
            self.updateTime()
            print('[DEBUG: ' + str(self.current_time.hour) + ':' + str(self.current_time.minute) + ':' + str(self.current_time.second) + '] ' + text)

    def updateTime(self):
        self.current_time = datetime.datetime.now()