import os
import requests
import zipfile

from .helper import Helper

class DriverSetup:
    LATEST_RELEASE_STABLE_URL = 'https://googlechromelabs.github.io/chrome-for-testing/LATEST_RELEASE_STABLE'
    STORAGE_URL = 'https://storage.googleapis.com/chrome-for-testing-public'

    def __init__(self):
        # check if bin directory exists, otherwise create it
        if not os.path.exists('bin'):
            os.mkdir('bin')

        if not self.driver_exists():
            self.download_driver()

    def driver_exists(self) -> bool:

        # do md5sum check here

        if not os.path.exists(Helper.get_driver_path()):
            return False
        return True

    def get_latest_version(self) -> str:
        try:
            r = requests.get(self.LATEST_RELEASE_STABLE_URL)
            return r.text
        except:
            raise Exception('[DriverSetup] getLatestVersion() error')

    def download_driver(self) -> None:
        driver_folder_path = Helper.get_driver_folder_path()
        driver_zip_name = Helper.get_driver_zip_name()

        # download the zip file
        extra_path = driver_folder_path + '/' + driver_zip_name
        try:
            url = self.STORAGE_URL + '/' + self.get_latest_version() + '/' + extra_path
            r = requests.get(url, allow_redirects=True)
        except:
            raise Exception('[DriverSetup] downloadDriver() error')

        zip_path = os.getcwd() + '\\chromedriver.zip'

        # write content to disk
        open(zip_path, 'wb').write(r.content)

        # unzip
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall('bin')

        # delete zip
        os.remove(zip_path)