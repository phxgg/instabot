'''
Made by phxgg (https://github.com/phxgg)

Please note that Instagram can limit an account's likes, comments and activity in general.
This script cannot be 100% accurate regarding Instagram limits.
There is a chance that your account might be locked, limited or even banned.
Use this at your own risk.
'''

import atexit
import os
import sys
import argparse

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
is_updated = updater.is_updated()

# Pause app when exiting so it shows the exception error if thrown
def exit_handler():
    # sys.stdout.close()

    ''' Restart script on error. Disabled for now because it'll cause too many requests (error code 429) '''
    # os.system('python {}'.format(os.path.abspath(__file__)))

    platform = Helper.get_platform()
    if platform == 'win32' or platform == 'win64':
        os.system('pause')


def main():
    atexit.register(exit_handler)

    # parse arguments
    parser = argparse.ArgumentParser(description='InstaBot - by phxgg')
    parser.add_argument('--no-headless', action='store_true', help='Run the bot in headless mode')
    args = parser.parse_args()

    if is_updated:
        my_bot = None

        try:
            # initialize bot
            my_bot = InstaBot(args, config)

            # prepare & start bot
            my_bot.prepare()
            my_bot.start()
        except KeyboardInterrupt as e:
            print('[KeyboardInterrupt] Early termination of InstaBot.')
        except Exception as e:
            print('[Exception]')

            if 'This version of ChromeDriver only supports Chrome version' in str(e):
                print('[ERROR] UPDATE NEEDED: Please delete the "bin" folder and update your Chrome browser.')
            else:
                print(e)
        finally:
            Helper.exit_app('[EXIT InstaBot]', [my_bot.counter.count_comments_file] if my_bot != None else None, my_bot)


if __name__ == '__main__':
    main()
