"""
Made by phxgg (https://github.com/phxgg)

TODO: see README.md

[This script on average posts 500-600 comments in 24 hours.]
Please note that Instagram can limit an account's likes, comments and activity in general.
This script cannot be 100% accurate regarding Instagram limits.
There is a chance that your account might be locked, limited or even banned.
Use this at your own risk.
"""

from time import sleep
import random
import os
import sys

from classes.updater import Updater
#from classes.driversetup import DriverSetup
from classes.config import Config
from classes.logger import Logger
from win32api import GetSystemMetrics

from selenium import webdriver
from selenium.webdriver.support import ui
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

# Global variables
updater = Updater()
#driversetup = DriverSetup()
config = Config('./config/config.json')
logger = Logger(config.debug)

width = str(GetSystemMetrics(0))
height = str(GetSystemMetrics(1))

commentsCounter = 0
minuteBreakComments = 0
hourBreakComments = 0

def getRandomTag(match, taglist):
    index = random.randint(0, len(taglist)-1)
    tag = taglist[index]
    taglist.remove(tag)
    return tag

class InstaBot:
    def __init__(self, c):
        self.config = c

        # initialize logger
        logger.info('Initializing InstaBot...')

        logger.debug('Setting up ChromeOptions...')
        logger.debug('Found Monitor Size: ' + width + 'x' + height)
        
        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_argument('--window-size=' + width + ',' + height)
        self.chrome_options.add_argument('--disable-extensions')
        #self.chrome_options.add_argument("--proxy-server='direct://'") # not sure if needed so i commented these two out
        #self.chrome_options.add_argument("--proxy-bypass-list=*")
        self.chrome_options.add_argument('--start-maximized')
        self.chrome_options.add_argument('--headless')
        self.chrome_options.add_argument('--disable-gpu')
        self.chrome_options.add_argument('--disable-dev-shm-usage')
        self.chrome_options.add_argument('--no-sandbox')
        self.chrome_options.add_argument('--ignore-certificate-errors')
        self.chrome_options.add_argument('--allow-running-insecure-content')
        self.chrome_options.add_argument('--log-level=3') # hide console warnings

        logger.debug('Loading Chrome driver...')
        self.driver = webdriver.Chrome('chromedriver', options=self.chrome_options)

        # get instagram post
        logger.debug('Getting the Instagram post URL...')
        self.driver.get(self.config.igPost_url)
        sleep(2)

        # click accept cookies
        logger.debug('Clicking "Accept" button on the cookies message...')
        self.driver.find_element_by_xpath('//button[contains(text(), "Accept")]').click()
        sleep(2)
        
        # click the button to get into Login page
        logger.debug('Clicking on the "Log in" button...')
        self.driver.find_element_by_xpath('//a[contains(text(), "Log in")]').click()
        sleep(3)

        # input username & password and click the login button
        logger.debug('Looking for the username & password fields')
        unField = self.driver.find_element_by_xpath('//input[@name="username"]')
        pwField = self.driver.find_element_by_xpath('//input[@name="password"]')

        logger.debug('Sending keys for username & password...')
        self.typePhrase(self.config.username, unField)
        self.typePhrase(self.config.password, pwField)

        logger.debug('Clicking submit...')
        self.driver.find_element_by_xpath('//button[@type="submit"]').click()
        sleep(5)

        # check if the account has been locked. If so, we have to wait for some time to re-try logging in
        if not self.canLogin():
            logger.error('Cannot login! Waiting for 30 minutes...')
            sleep(1800)
            logger.info('Done waiting. Trying again...')
        else:
            logger.debug('Successfully logged in!')

        # bypass One Tap when logged in
        logger.debug('Bypassing the "One Tap" dialog box by clicking "Not Now"...')
        self.driver.find_element_by_xpath('//button[contains(text(), "Not Now")]').click()
        sleep(3)

    def comment(self):
        global commentsCounter, hourBreakComments

        # clone the global tags variable
        tags = list(self.config.tags)

        # fill in comment with comment_format
        tag_count = self.config.comment_format.count('[tag]')
        format_tag = self.config.comment_format.replace('[tag]', '{}')
        comment = format_tag.format(*('@' + tags[random.randint(0, len(tags)-1)] for _ in range(tag_count)))

        """
        for i in range(0, 3):
            index = random.randint(0, len(tags)-1)
            comment = comment + '@' + tags[index] + ' '
            tags.remove(tags[index])
        """

        # find instagram post
        logger.debug('Getting Instagram post URL...')
        self.driver.get(self.config.igPost_url)
        sleep(2)

        # get comment textarea and click on the input box. Doing this once, for some reason did not work so i had to do this twice.
        logger.debug('Looking for the comment textarea & clicking on it...')
        commentArea = self.driver.find_element_by_xpath('//textarea[contains(@aria-label,"Add a comment")]')
        commentArea.click()
        sleep(5)
        commentArea = self.driver.find_element_by_xpath('//textarea[contains(@aria-label,"Add a comment")]')
        commentArea.click()

        # input comment
        logger.info('Commenting: ' + comment)
        self.typePhrase(comment, commentArea)
        sleep(1)

        # click post button (or we could send_keys(Keys.RETURN))
        logger.debug('Clicking the "Post" button...')
        self.driver.find_element_by_xpath('//button[contains(text(), "Post")]').click()
        sleep(1.5)

        # check if post was successfully commented. Otherwise wait for 1 hour to kinda refresh the rate
        if not self.commentPosted():
            logger.error('Could not post comment! Waiting for 1 hour...')
            hourBreakComments = self.config.perHourComments # force an hour break
        else:
            logger.debug('Posted successfully!')
            commentsCounter = commentsCounter + 1
        
        #self.driver.execute_script("document.evaluate(\"//button[contains(text(), 'Post')]\", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.removeAttribute(\"disabled\");")
        #sleep(2)
    
    def canLogin(self):
        try:
            self.driver.find_element_by_xpath('//p[@id="slfErrorAlert"]')
        except NoSuchElementException:
            return True
        return False

    def commentPosted(self):
        flag = False

        # check if Retry button exists
        try:
            self.driver.find_element_by_xpath('//button[contains(text(), "Retry")]')
            flag = True
        except NoSuchElementException:
            pass

        # or check if Try Again Later dialog is shown
        try:
            self.driver.find_element_by_xpath('//h3[contains(text(), "Try Again Later")]')
            flag = True
        except NoSuchElementException:
            pass
        
        # or check if Report a Problem button exists
        try:
            self.driver.find_element_by_xpath('//button[contains(text(), "Report a Problem")]')
            flag = True
        except NoSuchElementException:
            pass

        if flag:
            return False
        return True

    def typePhrase(self, comment, field):
        for letter in comment:
            field.send_keys(letter)
            sleep(random.uniform(0.03, 0.08)) # input time of each letter (const one was: 0.048)

    def quit(self):
        self.driver.quit()

# load comment counter
try:
    with open('./counter.txt') as countCommentsFile:
        commentsCounter = int(countCommentsFile.read())
except Exception as e:
    print("An error occured when trying to open counter.txt")
    print(e)
    sys.exit()

# initialize bot
my_bot = InstaBot(config)

# open counter file to keep updating the counter
countCommentsFile = open('./counter.txt', 'a')

while True:
    # hour break
    if hourBreakComments >= config.perHourComments:
        print('[*] HOUR break')
        minuteBreakComments = 0
        hourBreakComments = 0
        sleep(3600) # 1 hour

    # minute break
    if minuteBreakComments >= config.sessionComments:
        print('[*] MINUTE break')
        minuteBreakComments = 0
        sleep(180) # 3 mins
    
    print('[*] Counter: ' + str(commentsCounter))

    my_bot.comment()

    # we do not want to include these increments inside the comment() function because we want to go through the breaks to avoid instagram limits
    minuteBreakComments = minuteBreakComments + 1
    hourBreakComments = hourBreakComments + 1

    countCommentsFile.seek(0)
    countCommentsFile.truncate()
    countCommentsFile.write(str(commentsCounter))

my_bot.quit()