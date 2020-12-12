from win32api import GetSystemMetrics
import json

class Config:
    def __init__(self, configJson):
        try:
            with open(configJson) as f_config:
                data = json.load(f_config)
                self.debug = data['debug']
                self.keepCommentLogs = data['keepCommentLogs']
                self.username = data['username']
                self.password = data['password']
                self.igPost_url = data['ig_post_url']
                self.comment_format = data['comment_format']
                self.sessionComments = data['sessionComments']
                self.perHourComments = data['perHourComments']

            self.tags = []

            with open('./config/tags.txt') as f_tags:
                for tag in f_tags:
                    self.tags.append(tag.strip()) # use .strip() to remove the new line character
        except Exception as e:
            print("An error occured while initializing Config.")
            print(e)
            sys.exit()

        self.width = str(GetSystemMetrics(0))
        self.height = str(GetSystemMetrics(1))