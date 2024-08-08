import os

class Counter:
    comments_counter = 0
    minute_break_comments = 0
    hour_break_comments = 0

    count_comments_file = None

    def __init__(self):
        # load comment counter
        try:
            with open('./counter.txt', 'r') as countCommentsFile:
                self.comments_counter = int(countCommentsFile.read())
        except Exception:
            with open('./counter.txt', 'a') as countCommentsFile:
                self.comments_counter = 0

        # open counter file to keep updating the counter
        self.count_comments_file = open('./counter.txt', 'a')
    
    def write_counter(self):
        if self.count_comments_file:
            self.count_comments_file.seek(0) # get to the first index of text
            self.count_comments_file.truncate() # truncate everything after it
            self.count_comments_file.write(str(self.counter.comments_counter)) # write new comments counter

            self.count_comments_file.flush() # these two lines will make sure the file is saved & updated even if an error occurs
            os.fsync(self.count_comments_file.fileno())

