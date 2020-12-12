import sys

class Helper:
    @staticmethod
    def safe_execute(default, exception, function, *args):
        try:
            return function(*args)
        except exception:
            return default

    @staticmethod
    def exitApp(msg = None, openFiles = [], igBot = None):
        if openFiles:
            for f in openFiles:
                #f.close()
                Helper.safe_execute('Object probably not a file', Exception, f.close)
        if igBot:
            igBot.quit()
        sys.exit(msg if msg else 0)

    @staticmethod
    def getPlatform():
        return sys.platform
        