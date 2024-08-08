import requests

VERSION = '1.0'
VERSION_URL = 'https://dl.dropbox.com/s/vnwvqchi3cgt3pm/version.txt?dl=0'

class Updater:
    latest_version = None

    def __init__(self):
        print('* Checking for updates...')

        # TODO
        #self.latest_version = self.get_latest_version()
        self.latest_version = '1.0'

        if VERSION != self.latest_version:
            print('** You are using an outdated version. Updating now... **')
            print('[*] Your version: ' + VERSION)
            print('[*] Latest version: ' + self.latest_version)
            self.update()

    def is_updated(self) -> bool:
        latest_version = self.latest_version
        if VERSION != latest_version:
            return False
        return True

    def get_latest_version(self) -> str:
        try:
            r = requests.get(VERSION_URL)
            return r.text
        except:
            return 'error'

    def update(self) -> None:
        print('Self-updating is under construction.')