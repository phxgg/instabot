import datetime
import os

class Logger:
    current_time = datetime.datetime.now()
    commentLogs = None

    def __init__(self, debugEnabled: bool, keepCommentLogs: bool):
        self.debugEnabled = debugEnabled
        self.keepCommentLogs = keepCommentLogs

        if self.keepCommentLogs:
            self.commentLogs = open('./comments.log', 'a')

    def info(self, text: str) -> None:
        self.updateTime()
        print('[INFO: ' + str(self.current_time.hour) + ':' + str(self.current_time.minute) + ':' + str(self.current_time.second) + '] ' + text)

    def error(self, text: str) -> None:
        self.updateTime()
        print('[ERROR: ' + str(self.current_time.hour) + ':' + str(self.current_time.minute) + ':' + str(self.current_time.second) + '] ' + text)
    
    def debug(self, text: str) -> None:
        if self.debugEnabled:
            self.updateTime()
            print('[DEBUG: ' + str(self.current_time.hour) + ':' + str(self.current_time.minute) + ':' + str(self.current_time.second) + '] ' + text)

    def writeComment(self, comment: str) -> None:
        if self.keepCommentLogs:
            self.commentLogs.write(comment + '\n')
            # instantly ensure the comment is written to the file
            self.commentLogs.flush()

    def close(self) -> None:
        if self.keepCommentLogs:
            self.commentLogs.close()

    def updateTime(self) -> None:
        self.current_time = datetime.datetime.now()