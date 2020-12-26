import sys

class Counter:
    comments_counter = 0
    minute_break_comments = 0
    hour_break_comments = 0

    count_comments_file = None

    def __init__(self):
        # load comment counter
        try:
            with open('./counter.txt') as countCommentsFile:
                self.comments_counter = int(countCommentsFile.read())
        except Exception as e:
            print(e)
            sys.exit('An error occured when trying to open counter.txt')    

        # open counter file to keep updating the counter
        self.count_comments_file = open('./counter.txt', 'a')

