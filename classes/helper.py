import sys
import hashlib

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
        
    @staticmethod
    def getDriverName():
        driver_file_name = ''

        if Helper.getPlatform() == 'linux' or Helper.getPlatform() == 'linux2':
            driver_file_name = 'chromedriver'
        elif Helper.getPlatform() == 'win32':
            driver_file_name = 'chromedriver.exe'
        elif Helper.getPlatform() == 'darwin':
            driver_file_name = 'chromedriver'

        return driver_file_name
        
    @staticmethod
    def getUserAgent():
        ua = ''

        if Helper.getPlatform() == 'linux' or Helper.getPlatform == 'linux2':
            ua = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'
        elif Helper.getPlatform() == 'win32':
            ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'
        elif Helper.getPlatform() == 'darwin':
            ua = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_3_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'
        
        return ua

    @staticmethod
    def md5sum(filepath):
        md5_hash = hashlib.md5()

        f = open(filepath, 'rb')
        md5_hash.update(f.read())

        digest = md5_hash.hexdigest()
        f.close()
        
        return digest