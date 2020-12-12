import sys

class Counter:
    commentsCounter = 0
    minuteBreakComments = 0
    hourBreakComments = 0

    countCommentsFile = None

    def __init__(self):
        # load comment counter
        try:
            with open('./counter.txt') as countCommentsFile:
                self.commentsCounter = int(countCommentsFile.read())
        except Exception as e:
            print(e)
            sys.exit('An error occured when trying to open counter.txt')    

        # open counter file to keep updating the counter
        self.countCommentsFile = open('./counter.txt', 'a')

