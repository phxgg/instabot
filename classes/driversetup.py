import os
import requests
import zipfile

from .helper import Helper

class DriverSetup:
    def __init__(self):
        # check if bin directory exists, otherwise create it
        if not os.path.exists('bin'):
            os.mkdir('bin')

        if not self.driverExists():
            self.downloadDriver()

    def driverExists(self) -> bool:

        # do md5sum check here

        if not os.path.exists(Helper.getDriverPath()):
            return False
        return True

    def getLatestVersion(self) -> str:
        try:
            url = 'https://chromedriver.storage.googleapis.com/LATEST_RELEASE'
            r = requests.get(url)
            return r.text
        except:
            raise Exception('[DriverSetup] getLatestVersion() error')

    def downloadDriver(self) -> None:
        zipFile = ''
        if Helper.getPlatform() == 'linux' or Helper.getPlatform() == 'linux2':
            zipFile = 'chromedriver_linux64.zip'
        elif Helper.getPlatform() == 'win32':
            zipFile = 'chromedriver_win32.zip'
        elif Helper.getPlatform() == 'darwin':
            zipFile = 'chromedriver_mac64.zip'

        try:
            url = 'https://chromedriver.storage.googleapis.com/' + self.getLatestVersion() + '/' + zipFile
            r = requests.get(url, allow_redirects=True)
        except:
            raise Exception('[DriverSetup] downloadDriver() error')
            
        zipPath = os.getcwd() + '\\chromedriver.zip'

        # write content to disk
        open(zipPath, 'wb').write(r.content)

        # unzip
        with zipfile.ZipFile(zipPath, 'r') as zip_ref:
            zip_ref.extractall('bin')

        # delete zip
        os.remove(zipPath)