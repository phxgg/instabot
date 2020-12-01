from time import sleep
import random
from classes.logger import Logger

from selenium import webdriver
from selenium.webdriver.support import ui
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

class InstaBot:
    def __init__(self, config):
        self.config = config
        self.logger = Logger(self.config.debug, self.config.keepCommentLogs)

        # initialize logger
        self.logger.info('Initializing InstaBot...')

        self.logger.debug('Setting up ChromeOptions...')
        self.logger.debug('Found Monitor Size: ' + config.width + 'x' + config.height)
        
        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_argument('--window-size=' + config.width + ',' + config.height)
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

        self.logger.debug('Loading Chrome driver...')
        self.driver = webdriver.Chrome('chromedriver', options=self.chrome_options)

        # get instagram post
        self.logger.debug('Getting the Instagram post URL...')
        self.driver.get(self.config.igPost_url)
        sleep(2)

        # click accept cookies
        self.logger.debug('Clicking "Accept" button on the cookies message...')
        self.driver.find_element_by_xpath('//button[contains(text(), "Accept")]').click()
        sleep(2)
        
        # click the button to get into Login page
        self.logger.debug('Clicking on the "Log in" button...')
        self.driver.find_element_by_xpath('//a[contains(text(), "Log in")]').click()
        sleep(3)

        # input username & password and click the login button
        self.logger.debug('Looking for the username & password fields')
        unField = self.driver.find_element_by_xpath('//input[@name="username"]')
        pwField = self.driver.find_element_by_xpath('//input[@name="password"]')

        self.logger.debug('Sending keys for username & password...')
        self.typePhrase(self.config.username, unField)
        self.typePhrase(self.config.password, pwField)

        self.logger.debug('Clicking submit...')
        self.driver.find_element_by_xpath('//button[@type="submit"]').click()
        sleep(5)

        # check if the account has been locked. If so, we have to wait for some time to re-try logging in
        if not self.canLogin():
            self.logger.error('Cannot login! Waiting for 30 minutes...')
            sleep(1800)
            self.logger.info('Done waiting. Trying again...')
        else:
            self.logger.debug('Successfully logged in!')

        # bypass One Tap when logged in
        self.logger.debug('Bypassing the "One Tap" dialog box by clicking "Not Now"...')
        self.driver.find_element_by_xpath('//button[contains(text(), "Not Now")]').click()
        sleep(3)

    def comment(self):
        global commentsCounter, hourBreakComments

        # clone the global tags variable
        tags = list(self.config.tags)

        # fill in comment with comment_format
        tag_count = self.config.comment_format.count('[tag]')
        format_tag = self.config.comment_format.replace('[tag]', '{}')
        comment = format_tag.format(*('@' + self.getRandomTag(tags) for _ in range(tag_count))) #tags[random.randint(0, len(tags)-1)]

        """
        for i in range(0, 3):
            index = random.randint(0, len(tags)-1)
            comment = comment + '@' + tags[index] + ' '
            tags.remove(tags[index])
        """

        # find instagram post
        self.logger.debug('Getting Instagram post URL...')
        self.driver.get(self.config.igPost_url)
        sleep(2)

        # get comment textarea and click on the input box. Doing this once, for some reason did not work so i had to do this twice.
        self.logger.debug('Looking for the comment textarea & clicking on it...')
        commentArea = self.driver.find_element_by_xpath('//textarea[contains(@aria-label,"Add a comment")]')
        commentArea.click()
        sleep(5)
        commentArea = self.driver.find_element_by_xpath('//textarea[contains(@aria-label,"Add a comment")]')
        commentArea.click()

        # input comment
        self.logger.info('Commenting: ' + comment)
        self.typePhrase(comment, commentArea)
        sleep(1)

        # click post button (or we could send_keys(Keys.RETURN))
        self.logger.debug('Clicking the "Post" button...')
        self.driver.find_element_by_xpath('//button[contains(text(), "Post")]').click()
        sleep(1.5)

        # check if post was successfully commented. Otherwise wait for 1 hour to kinda refresh the rate
        if not self.commentPosted():
            self.logger.error('Could not post comment! Waiting for 1 hour...')
            hourBreakComments = self.config.perHourComments # force an hour break
        else:
            self.logger.writeComment(comment)
            self.logger.debug('Posted successfully!')
            commentsCounter = commentsCounter + 1
        
        #self.driver.execute_script("document.evaluate(\"//button[contains(text(), 'Post')]\", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.removeAttribute(\"disabled\");")
        #sleep(2)
    
    def getRandomTag(self, tags):
        index = random.randint(0, len(tags)-1)
        tag = tags[index]
        tags.remove(tag) # delete tag from the temporary variable. We do not want to show the same tag more than once
        return tag

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