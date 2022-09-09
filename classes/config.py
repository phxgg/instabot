import sys
import json

class Config:
    def __init__(self, configJson: str):
        try:
            with open(configJson) as f_config:
                data = json.load(f_config)
                self.debug = data['debug']
                self.keep_comment_logs = data['keep_comment_logs']
                self.username = data['username']
                self.password = data['password']
                self.ig_post_url = data['ig_post_url']
                self.comment_format = data['comment_format']
                self.session_comments = data['session_comments']
                self.per_hour_comments = data['per_hour_comments']

            self.tags = []

            with open('./config/tags.txt') as f_tags:
                for tag in f_tags:
                    tag = tag.strip() # use .strip() to remove the new line character
                    if not tag.isspace():
                        self.tags.append(tag)
        except Exception as e:
            print(e)
            sys.exit('An error occured while initializing Config.')