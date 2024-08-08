import sys
import os
import hashlib
import platform

class Helper:
    @staticmethod
    def safe_execute(default, exception: Exception, function, *args):
        try:
            return function(*args)
        except exception:
            return default

    @staticmethod
    def exit_app(msg: str = None, openFiles: list = [], igBot = None) -> None:
        if openFiles:
            for f in openFiles:
                #f.close()
                Helper.safe_execute('Object probably not a file', Exception, f.close)
        if igBot:
            igBot.quit()
        sys.exit(msg if msg else 0)
    
    @staticmethod
    def get_platform() -> str:
        system = platform.system().lower()

        if system == "windows":
            # Check if it's 32-bit or 64-bit
            arch = platform.architecture()[0]
            if arch == "32bit":
                return "win32"
            elif arch == "64bit":
                return "win64"
        elif system == "linux":
            return "linux"
        elif system == "darwin":
            return "darwin" # macOS is identified as 'darwin'
        
        return "unknown"
        
    @staticmethod
    def get_driver_exe() -> str:
        platform = Helper.get_platform()
        driver_file_name = ''

        if platform == 'linux':
            driver_file_name = 'chromedriver'
        elif platform == 'win32' or platform == 'win64':
            driver_file_name = 'chromedriver.exe'
        elif platform == 'darwin':
            driver_file_name = 'chromedriver'

        return driver_file_name
    
    @staticmethod
    def get_driver_folder_path() -> str:
        platform = Helper.get_platform()
        driver_folder = ''

        if platform == 'linux':
            driver_folder = 'linux64'
        elif platform == 'win32':
            driver_folder = 'win32'
        elif platform == 'win64':
            driver_folder = 'win64'
        elif platform == 'darwin':
            driver_folder = 'mac-x64'
        
        return driver_folder
    
    @staticmethod
    def get_driver_zip_name() -> str:
        platform = Helper.get_platform()
        driver_zip = ''

        if platform == 'linux':
            driver_zip = 'chromedriver-linux64.zip'
        elif platform == 'win32':
            driver_zip = 'chromedriver-win32.zip'
        elif platform == 'win64':
            driver_zip = 'chromedriver-win64.zip'
        elif platform == 'darwin':
            driver_zip = 'chromedriver-mac-x64.zip'
        
        return driver_zip

    @staticmethod
    def get_driver_path() -> str:
        driver_folder_path = Helper.get_driver_folder_path()
        return os.path.join(os.getcwd(), 'bin', 'chromedriver-' + driver_folder_path, Helper.get_driver_exe())
        
    @staticmethod
    def get_user_agent() -> str:
        platform = Helper.get_platform()
        ua = ''

        if platform == 'linux':
            ua = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36'
        elif platform == 'win32' or platform == 'win64':
            ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36'
        elif platform == 'darwin':
            ua = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36'
        
        return ua

    @staticmethod
    def md5sum(filepath) -> str:
        md5_hash = hashlib.md5()

        f = open(filepath, 'rb')
        md5_hash.update(f.read())

        digest = md5_hash.hexdigest()
        f.close()
        
        return digest