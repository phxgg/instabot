import os
import requests

VERSION = '1.0'
VERSION_URL = 'https://dl.dropbox.com/s/vnwvqchi3cgt3pm/version.txt?dl=0'

class Updater:
    def __init__(self):
        latest_version = self.getLatestVersion()

        if VERSION != latest_version:
            print("** You are using an outdated version. Updating now... **")
            print('[*] Your version ' + VERSION)
            print('[*] Latest version ' + latest_version)
            self.update()

    def getLatestVersion(self):
        r = requests.get(VERSION_URL)
        return r.text

    def update(self):
        print("Self-updating is under construction. The script will continue.")