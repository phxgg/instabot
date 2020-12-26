'''
Made by phxgg (https://github.com/phxgg)

TODO: see README.md

Please note that Instagram can limit an account's likes, comments and activity in general.
This script cannot be 100% accurate regarding Instagram limits.
There is a chance that your account might be locked, limited or even banned.
Use this at your own risk.
'''

from classes.helper import Helper
from classes.config import Config
from classes.updater import Updater
#from classes.driversetup import DriverSetup
from classes.instabot import InstaBot

# Global variables
updater = Updater()
#driversetup = DriverSetup()
config = Config('./config/config.json')
enable = updater.isUpdated()

if enable:
    my_bot = None
    
    try:
        # initialize bot
        my_bot = InstaBot(config)

        # start bot
        my_bot.startBot()
    except KeyboardInterrupt:
        Helper.exitApp('Early termination of InstaBot.', [my_bot.counter.count_comments_file], my_bot)

    Helper.exitApp('InstaBot exited successfully!', [my_bot.counter.count_comments_file], my_bot)
