'''
Made by phxgg (https://github.com/phxgg)

TODO: see README.md

Please note that Instagram can limit an account's likes, comments and activity in general.
This script cannot be 100% accurate regarding Instagram limits.
There is a chance that your account might be locked, limited or even banned.
Use this at your own risk.
'''

import atexit
import os
# import sys

from classes.helper import Helper
from classes.config import Config
from classes.updater import Updater
from classes.driversetup import DriverSetup
from classes.instabot import InstaBot

#sys.stdout = open('Logs.log', 'w')

# Global variables
updater = Updater()
driversetup = DriverSetup()
config = Config('./config/config.json')
enable = updater.isUpdated()

# Pause app when exiting so it shows the exception error if thrown
def exit_handler():
    # sys.stdout.close()

    if Helper.getPlatform() == 'win32':
        os.system('pause')


def main():
    atexit.register(exit_handler)

    if enable:
        my_bot = None

        try:
            # initialize bot
            my_bot = InstaBot(config)

            # prepare & start bot
            my_bot.prepare()
            my_bot.start()
        except KeyboardInterrupt as e:
            print('[KeyboardInterrupt] Early termination of InstaBot.')
        except Exception as e:
            print('[Exception]')
            print(str(e))
        finally:
            Helper.exitApp('[EXIT InstaBot]', [my_bot.counter.count_comments_file], my_bot)


if __name__ == '__main__':
    main()
