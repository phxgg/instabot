# InstaBot

### *This is under construction*

Auto commenting bot for Instagram.

Works great on multi-participation allowed giveaways.

# Installation
1. Install Python 3.8 (or later) & pip from https://www.python.org/
2. Use `pip install -r requirements.txt` to install the requirements.
3. Download the latest stable release of ChromeDriver from https://chromedriver.chromium.org/<br>*[you will have to have Google Chrome installed and updated to latest version]*
4. Include ChromeDriver executable path to your `PATH` system environment variable.<br>*[newer versions of InstaBot will auto download ChromeDriver, and `PATH` won't be necessary to edit]*

# How to use
1. Rename `config-sample.json` to `config.json` and `tags-sample.txt` to `tags.txt` inside the `config` folder.
2. In your `tags.txt` file, each line should be an Instagram username for your tag list.
3. In `config.json` complete the following fields:<br>
    * `username` Your instagram username.
    * `password` Your instagram password.
    * `ig_post_url` The instagram link of the post.
    * `comment_format` What you want to comment. Each `[tag]` field will be a different tag from your tags list.
    * `session_comments` How many comments to make before a 3 minute break happens (<b>recommended:</b> `3`)
    * `per_hour_comments` Maximum number of comments before a 1 hour break happens. (<b>recommended:</b> `35`)
    * `debug` Show debug logs in the console (true/false) (<b>recommended:</b> `true`).
    * `keep_comment_logs` Create a `comments.log` file that keeps logs of all your comments (<b>recommended:</b> `true`). 

<u><b>Notes:</b></u>
* You need to have 2FA disabled on your Instagram account.
* The more tags you use, the safer your account will be.
This is because Instagram will limit accounts that make the same comment over and over again,
so less tags means you're most likely to make a comment you have already made before.

*More documentation coming soon.*

# Distribution
### PyInstaller for Windows
```
pyinstaller main.py && Xcopy /E /I "config-dist" "./dist/main/config" && rm main.spec
```

### PyArmor
**Windows**
```
pyarmor pack --clean main.py && Xcopy /E /I "config-dist" "./dist/main/config"
```

**macOS**
```
pyarmor pack --clean main.py && cp -r "config-dist" "./dist/main/config"
```

ZIP the `dist` folder.

# Bugs
* Windows 8: It seems like the script won't work (cannot find html elements) on `--headless` mode in Windows 8.
This could be because of Instagram auto sending the current region language. *Might* have been fixed already, not tested.

# ToDo
* Self-updating application.
* Support for Firefox browser.
* Option to get tags from followings/followers instead of using `tags.txt`.
* Enable maximum number of comments per day to prevent Instagram from limiting.
* <s>Auto download ChromeDriver binaries if it does not exist.</s>
* <s>Cross-platform availability.</s>
* <s>Create a `start()` method in the `InstaBot` class and do the work there.</s>
* <s>Create a `Helper` class and keep certain functions there.</s>
* <s>User-Agent selection depending on the platform.</s>
* <s>Random time between each letter in `InstaBot.typePhrase()`</s>
* <s>Allow user to create, inside `config.json`, the format of comment that will be used.<br>
Example: `[tag] [tag] 42 euro size`</s>
