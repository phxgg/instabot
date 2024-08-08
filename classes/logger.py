import datetime

class Logger:
    current_time = datetime.datetime.now()
    comment_logs_file = None

    def __init__(self, debug_enabled: bool, keep_comment_logs: bool):
        self.debug_enabled = debug_enabled
        self.keep_comment_logs = keep_comment_logs

        if self.keep_comment_logs:
            self.comment_logs_file = open('./comments.log', 'a')

    def info(self, text: str) -> None:
        self.updateTime()
        print('[INFO: ' + str(self.current_time.hour) + ':' + str(self.current_time.minute) + ':' + str(self.current_time.second) + '] ' + text)

    def error(self, text: str) -> None:
        self.updateTime()
        print('[ERROR: ' + str(self.current_time.hour) + ':' + str(self.current_time.minute) + ':' + str(self.current_time.second) + '] ' + text)
    
    def debug(self, text: str) -> None:
        if self.debug_enabled:
            self.updateTime()
            print('[DEBUG: ' + str(self.current_time.hour) + ':' + str(self.current_time.minute) + ':' + str(self.current_time.second) + '] ' + text)

    def log_comment(self, comment: str) -> None:
        if self.keep_comment_logs:
            self.comment_logs_file.write(comment + '\n')
            # instantly ensure the comment is written to the file
            self.comment_logs_file.flush()

    def close(self) -> None:
        if self.keep_comment_logs:
            self.comment_logs_file.close()

    def updateTime(self) -> None:
        self.current_time = datetime.datetime.now()