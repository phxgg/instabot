'''
Made by phxgg (https://github.com/phxgg)

TODO: see README.md

Please note that Instagram can limit an account's likes, comments and activity in general.
This script cannot be 100% accurate regarding Instagram limits.
There is a chance that your account might be locked, limited or even banned.
Use this at your own risk.
'''

from classes.config import Config
from classes.updater import Updater
#from classes.driversetup import DriverSetup
from classes.instabot import InstaBot

# Global variables
updater = Updater()
#driversetup = DriverSetup()
config = Config('./config/config.json')

# safe execute
def safe_execute(default, exception, function, *args):
    try:
        return function(*args)
    except exception:
        return default

# close everything before quitting the application
def exitApp(msg = None, openFiles = [], igBot = None):
    if openFiles:
        for f in openFiles:
            #f.close()
            safe_execute('Object probably not a file', Exception, f.close)
    if igBot:
        igBot.quit()
    sys.exit(msg if msg else 0)

my_bot = None

try:
    # initialize bot
    my_bot = InstaBot(config)

    # start bot
    my_bot.startBot()
except KeyboardInterrupt:
    exitApp('Early termination of InstaBot.', [my_bot.counter.countCommentsFile], my_bot)

exitApp('InstaBot exited successfully!', [my_bot.counter.countCommentsFile], my_bot)
