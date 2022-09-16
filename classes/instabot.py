from selenium import webdriver
from selenium.webdriver.support import ui
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.keys import Keys

from time import sleep
import random
import os

from .helper import Helper
from .counter import Counter
from .logger import Logger

class InstaBot:
    config = None
    logger = None
    counter = None
    driver = None

    # update these regularly to avoid detection
    min_time_between_letters = 0.03
    max_time_between_letters = 0.09

    def __init__(self, config):
        '''
        The constructor will initialize all the variables and start the driver.
        '''
        
        self.config = config
        self.logger = Logger(self.config.debug, self.config.keep_comment_logs)
        self.counter = Counter()
        
        self.logger.info('Initializing InstaBot...')
        self.logger.debug('Setting up ChromeOptions...')
        #self.logger.debug('Found Monitor Size: ' + self.config.width + 'x' + self.config.height)

        self.chrome_options = webdriver.ChromeOptions()
        #self.chrome_options.add_argument('--window-size=' + self.config.width + ',' + self.config.height)
        self.chrome_options.add_argument('--disable-extensions')
        self.chrome_options.add_argument('--start-maximized') # works on Windows
        # self.chrome_options.add_argument('--start-fullscreen') # works on Mac (maybe not necessary)
        self.chrome_options.add_argument('--headless')
        self.chrome_options.add_argument('--lang=en-US')
        self.chrome_options.add_argument('--disable-gpu')
        self.chrome_options.add_argument('--mute-audio')
        self.chrome_options.add_argument('--log-level=3') # hide console warnings

        # detection issues
        self.chrome_options.add_argument('--user-agent=' + Helper.getUserAgent())
        self.chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        self.chrome_options.add_argument('--disable-dev-shm-usage')
        self.chrome_options.add_argument('--no-sandbox')
        self.chrome_options.add_argument('--ignore-certificate-errors')
        self.chrome_options.add_argument('--allow-running-insecure-content')

        self.chrome_options.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})
        self.chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
        self.chrome_options.add_experimental_option('useAutomationExtension', False)

        self.logger.debug('Loading Chrome driver...')
        self.driver = webdriver.Chrome(Helper.getDriverPath(), options=self.chrome_options)

        # self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        self.driver.execute_cdp_cmd('Network.setUserAgentOverride', {'userAgent': Helper.getUserAgent()})

        self.logger.debug('navigator.userAgent: ' + self.driver.execute_script('return navigator.userAgent'))
        self.logger.debug('navigator.webdriver: ' + str(self.driver.execute_script('return navigator.webdriver')))

    def prepare(self) -> None:
        # check if url is an instagram link
        self.checkIfInstagram()
        
        # get instagram post
        self.logger.debug('Getting the Instagram post URL...')
        try:
            self.driver.get('https://instagram.com')
            # self.driver.get(self.config.ig_post_url)
        except:
            raise Exception('Could not open the link.')

        sleep(2)

        # click accept cookies
        self.logger.debug('Clicking "Accept" button on the cookies message...')
        try:
            ui.WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//button[contains(text(), "Allow essential and optional cookies")]'))).click()
        except:
            raise Exception('Could not find the "Accept" cookies button.')

        sleep(5)
        
        # check if the Post URL is valid
        self.logger.debug('Validating post URL...')
        if not self.validPostURL():
            raise Exception('Post URL is invalid. Please check the URL you provided in the config.')

        # click the button to get into Login page
        # self.logger.debug('Clicking on the "Log In" button...')
        # try:
        #     ui.WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//button[contains(text(), "Log In")]'))).click()
        # except:
        #     raise Exception('Could not find the "Log In" button.')

        # redirect to instagram login url
        self.logger.debug('Redirecting to Login page...')
        try:
            self.driver.get('https://www.instagram.com/accounts/login/')
        except:
            raise Exception('Could not redirect to the Login page.')

        sleep(3)

        # input username & password and click the login button
        self.logger.debug('Looking for the username & password fields')
        try:
            unField = self.driver.find_element_by_xpath('//input[@name="username"]')
            pwField = self.driver.find_element_by_xpath('//input[@name="password"]')
        except:
            raise Exception('Could not find "username" and/or "password" elements.')

        self.logger.debug('Sending keys for username & password...')
        self.typePhrase(self.config.username, unField)
        self.typePhrase(self.config.password, pwField)

        self.logger.debug('Clicking submit...')
        try:
            self.driver.find_element_by_xpath('//button[@type="submit"]').click()
        except:
            raise Exception('Could not find "submit" button to login.')
            
        sleep(5)

        # check if the account has been locked. If so, we have to wait for some time to re-try logging in
        if not self.canLogin():
            self.logger.error('Cannot login! Waiting for 30 minutes. Also make sure your username & password combination is correct')
            sleep(1800)
            self.logger.info('Done waiting. Trying again...')
        else:
            self.logger.debug('Successfully logged in: ' + self.config.username)

        # check for Suspicious Login Attempt
        if self.suspiciousLoginAttempt():
            raise Exception('A Suspicious Login Attempt message was found. Please manually login and verify your account. Then restart the InstaBot.')
            #self.logger.error('A Suspicious Login Attempt message was found. Please manually login and verify your account. Then restart the InstaBot.')
            #Helper.exitApp('Suspicious Login Attempt found', [self.counter.count_comments_file], self)

        # redirect to instagram post url in case "One Tap" box shows up
        self.logger.debug('Redirecting to Instagram post URL...')
        try:
            self.driver.get(self.config.ig_post_url)
        except:
            raise Exception('Could not open the link.')

        # bypass One Tap when logged in
        #self.logger.debug('Bypassing the "One Tap" dialog box by clicking "Not Now"...')
        #self.driver.find_element_by_xpath('//button[contains(text(), "Not Now")]').click()

        sleep(3)

    def start(self) -> None:
        while True:
            # hour break
            if self.counter.hour_break_comments >= self.config.per_hour_comments:
                print('[*] HOUR break')
                self.counter.minute_break_comments = 0
                self.counter.hour_break_comments = 0
                sleep(3600) # 1 hour

            # minute break
            if self.counter.minute_break_comments >= self.config.session_comments:
                print('[*] MINUTE break')
                self.counter.minute_break_comments = 0
                sleep(180) # 3 mins
            
            print('[*] Counter: ' + str(self.counter.comments_counter))

            self.comment()

            # we do not want to include these increments inside the comment() function because we want to go through the breaks to avoid instagram limits
            self.counter.minute_break_comments = self.counter.minute_break_comments + 1
            self.counter.hour_break_comments = self.counter.hour_break_comments + 1

            self.counter.count_comments_file.seek(0) # get to the first index of text
            self.counter.count_comments_file.truncate() # truncate everything after it
            self.counter.count_comments_file.write(str(self.counter.comments_counter)) # write new comments counter

            self.counter.count_comments_file.flush() # these two lines will make sure the file is saved & updated even if an error occurs
            os.fsync(self.counter.count_comments_file.fileno())

    def comment(self) -> None:
        # clone the global tags variable
        tags = list(self.config.tags)

        # fill in comment with comment_format
        tag_count = self.config.comment_format.count('[tag]')
        format_tag = self.config.comment_format.replace('[tag]', '{}')
        comment = format_tag.format(*('@' + self.getRandomTag(tags) for _ in range(tag_count))) #tags[random.randint(0, len(tags)-1)]

        # find instagram post
        self.checkIfInstagram()

        try:
            self.driver.get(self.config.ig_post_url)
        except:
            raise Exception('Could not open the link.')

        sleep(2)

        # get comment textarea and click on the input box.
        # Instagram might load the commentArea more than one times, so we might get an exception at the first try.
        self.logger.debug('Looking for the comment textarea & clicking on it...')
        try:
            commentArea = ui.WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//textarea[contains(@aria-label,"Add a comment…")]')))
            commentArea.click()
        except StaleElementReferenceException as e:
            commentArea = ui.WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//textarea[contains(@aria-label,"Add a comment…")]')))
            commentArea.click()
        except:
            raise Exception('Could not find the comment textarea.')

        sleep(1)

        # input comment
        pressEnterInComment = True
        self.logger.info('Commenting: ' + comment)
        self.typePhrase(comment, commentArea, True, pressEnterInComment)
        
        sleep(1)

        # click post button if we did not already press enter while typing the comment
        if not pressEnterInComment:
          self.logger.debug('Clicking the "Post" button...')
          try:
              ui.WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//button/div[contains(text(), "Post")]'))).click()
              # ui.WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//button[contains(@data-testid, "post-comment-input-button")]'))).click()
          except:
              raise Exception('Could not find the "Post" button.')

        sleep(1.5)

        # check if post was successfully commented. Otherwise wait for 1 hour to kinda refresh the rate
        if not self.commentPosted():
            self.logger.error('Could not post comment! Waiting for 1 hour...')
            self.counter.hour_break_comments = self.config.per_hour_comments # force an hour break
        else:
            self.logger.writeComment(comment)
            self.logger.debug('Posted successfully!')
            self.counter.comments_counter = self.counter.comments_counter + 1

        #self.driver.execute_script("document.evaluate(\"//button[contains(text(), 'Post')]\", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.removeAttribute(\"disabled\");")
        #sleep(2)
    
    def checkIfInstagram(self):
        '''
        Check if the given URL is an Instagram link.
        '''

        if 'instagram.com' not in self.config.ig_post_url:
            raise Exception('Not an Instagram URL.')

    def getRandomTag(self, tags: list) -> str:
        '''
        Return a random username from the tags.txt
        '''

        index = random.randint(0, len(tags)-1)
        tag = tags[index]
        tags.remove(tag) # delete tag from the temporary variable. We do not want to show the same tag more than once
        return tag

    def suspiciousLoginAttempt(self) -> bool:
        '''
        Return true if a "suspicious login attempt" message has been received.
        '''

        flag = False

        # find "Suspicious Login Attempt" text
        try:
            self.driver.find_element_by_xpath('//p[contains(text(), "Suspicious Login Attempt")]')
            flag = True
        except:
            pass

        try:
            self.driver.find_element_by_xpath('//h2[contains(text(), "We Detected An Unusual Login Attempt")]')
            flag = True
        except:
            pass

        return flag

    def canLogin(self) -> bool:
        '''
        Return true if no error has been received during the login attempt.
        '''

        try:
            self.driver.find_element_by_xpath('//p[@id="slfErrorAlert"]')
        except NoSuchElementException:
            return True
        return False

    def validPostURL(self) -> bool:
        '''
        Return true if the Post URL exists.
        '''

        try:
            self.driver.find_element_by_xpath('//h2[contains(text(), "Sorry, this page isn\'t available.")]')
        except NoSuchElementException:
            return True
        return False

    def commentPosted(self) -> bool:
        '''
        Return true if the comment was successfully posted and no errors were received.
        '''

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

    def typePhrase(self, text: str, field, isCommentArea: bool = False, pressEnter: bool = False) -> None:
        '''
        Type something in a field with random time between each letter (0.03 - 0.08 seconds)
        @text: the text to type
        @field: the field to type in
        @isCommentArea: if true, we're grabbing the comment textarea element at the exact time that we want to type on it
        @pressEnter: if true, we'll press the enter key after typing the text -> used for posting the comment
        '''

        try:
            for letter in text:
                # It seems like Instagram will load the commentArea textbox more than one times.
                # To fix this, we're grabbing the element at the exact time that we want to type on it.
                if isCommentArea:
                    field = ui.WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//textarea[contains(@aria-label,"Add a comment")]')))

                field.send_keys(letter)
                sleep(random.uniform(self.min_time_between_letters, self.max_time_between_letters)) # input time of each letter (const one was: 0.048)

            if pressEnter:
                sleep(random.uniform(self.min_time_between_letters, self.max_time_between_letters))
                field.send_keys(Keys.RETURN)
        except StaleElementReferenceException as e:
            raise StaleElementReferenceException('[InstaBot] typePhrase(): bug')
        except:
            raise Exception('[InstaBot] typePhrase(): Something went wrong.')

    def quit(self) -> None:
        '''
        Quit the driver.
        '''

        self.driver.quit()
