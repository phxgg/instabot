import subprocess
import sys
import requests
import zipfile
import shutil
import tempfile
from pathlib import Path

VERSION = '1.0.1'
VERSION_URL = 'https://dl.dropbox.com/scl/fi/mbnqfefdcxjj8l131lswf/version.json?rlkey=wm4rkenk13uagygmfy3iaf097&dl=0'
APP_DIR = Path(sys.executable).parent # Directory where your app is installed
UPDATE_DIR = APP_DIR / "update" # Temporary update directory

class Updater:
    latest_version = None

    def __init__(self):
        print('* Checking for updates...')

        x = self.get_latest_version()
        self.latest_version = x[0]
        self.url = x[1]

        if VERSION != self.latest_version:
            print('** You are using an outdated version. Updating now... **')
            print('[*] Your version: ' + VERSION)
            print('[*] Latest version: ' + self.latest_version)

            if self.url:
                zip_path = self.download_update()
                if zip_path:
                    extracted_dir = self.extract_update(zip_path)
                    if extracted_dir:
                        bat_path = self.create_update_script()
                        if bat_path:
                            self.execute_update_script(bat_path)
                else:
                    # exit application if download failed
                    sys.exit(1)
            else:
                # exit application if no url is provided
                sys.exit(1)

    def is_updated(self) -> bool:
        latest_version = self.latest_version
        if VERSION != latest_version:
            return False
        return True

    def get_latest_version(self) -> tuple:
        try:
            r = requests.get(VERSION_URL)
            # parse json
            json = r.json()
            return json['version'], json['url']
        except Exception as e:
            print('[ERROR] Failed to check for updates.')
            print(e)
            return VERSION, None

    def download_update(self):
        '''
        Download the update from the provided URL.
        '''
        try:
            print('Downloading update...')
            response = requests.get(self.url, stream=True)
            response.raise_for_status()

            # Create a temporary file to save the download
            temp_zip_path = Path(tempfile.gettempdir()) / 'update.zip'
            with open(temp_zip_path, 'wb') as temp_zip_file:
                for chunk in response.iter_content(chunk_size=8192):
                    temp_zip_file.write(chunk)
            
            print('Download complete.')
            return temp_zip_path
        except Exception as e:
            print(f'Error downloading update: {e}')
            return None
        
    def extract_update(self, zip_path):
        '''
        Extract the update into the `update` folder.
        '''
        try:
            print('Extracting update...')
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                # Remove the old update directory if it exists
                if UPDATE_DIR.exists():
                    shutil.rmtree(UPDATE_DIR)
                UPDATE_DIR.mkdir(parents=True, exist_ok=True)
                zip_ref.extractall(UPDATE_DIR)
            print('Update extracted.')
            return UPDATE_DIR
        except Exception as e:
            print(f'Error extracting update: {e}')
            return None

    def create_update_script(self):
        '''
        Create a batch script to replace files and delete the `update` folder.
        '''
        try:
            print('Creating update script...')

            # Path for the batch file
            bat_path = APP_DIR / 'update.bat'

            with open(bat_path, "w") as bat_file:
                bat_file.write(f"@echo off\n")
                bat_file.write(f"timeout /t 2 /nobreak\n")  # Wait for 2 seconds

                # Replace old files with new ones
                bat_file.write(f"xcopy \"{UPDATE_DIR}\\*\" \"{APP_DIR}\" /E /H /C /I /Y\n")
                bat_file.write(f"rmdir /S /Q \"{UPDATE_DIR}\"\n")  # Delete the 'update' directory
                # bat_file.write(f"start \"\" \"{APP_DIR / 'main.exe'}\"\n")  # Restart the application
                bat_file.write(f"del \"%~f0\"\n")  # Delete the batch script itself

            print("Update script created.")
            return bat_path
        except Exception as e:
            print(f'Error creating update script: {e}')
            return None

    def install_update(self, zip_path):
        '''
        Unzip the update and prepare for replacement.
        '''
        try:
            print('Installing update...')
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                temp_dir = Path(tempfile.mkdtemp())
                zip_ref.extractall(temp_dir)

                return temp_dir
        except Exception as e:
            print(f'Error installing update: {e}')
            return None
    
    def execute_update_script(self, bat_path):
        '''
        Execute the batch script to perform the update.
        '''
        print('Executing update script...')
        subprocess.Popen([str(bat_path)], shell=True)
        sys.exit()  # Exit the current application