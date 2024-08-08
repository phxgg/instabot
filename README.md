# InstaBot

Auto commenting bot for Instagram.

Works great on multi-participation allowed giveaways.

# Requirements
1. Install Python 3.11.4 (or later) & pip from https://www.python.org/
2. Use `pip install -r requirements.txt` inside the `main.py` folder to install the requirements.
3. Google Chrome updated to the latest version.

# How to use
1. Rename `config-sample.json` to `config.json` and `tags-sample.txt` to `tags.txt` inside the `config` folder.
2. In your `tags.txt` file, each line should be an Instagram username for your tag list. <b>Make sure there are NO empty lines.</b>
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
* Creating new accounts will not produce many comments; instead they will get blocked.
Instagram's algorithm is designed to limit accounts that do not seem legit based on
several variables (account creation date, comment/like activity, following activity, interaction with other people, etc.).
It would be best to use a legit account.

# Distribution
## PyInstaller
* Windows
```
pyinstaller --clean main.py && Xcopy /E /I "config-dist" "./dist/main/config" && del main.spec
```

* macOS
```
pyinstaller --clean main.py && cp -r "config-dist" "./dist/main/config" && rm -rf main.spec
```

## PyArmor

> [!WARNING]
> PyArmor has been updated to version 8, and these instructions might not work as expected at the moment. Please refer to the [PyArmor documentation](https://pyarmor.readthedocs.io/en/latest/) for more information.

* Windows
```
pyarmor pack --clean main.py && Xcopy /E /I "config-dist" "./dist/main/config"
```

* macOS
```
pyarmor pack --clean main.py && cp -r "config-dist" "./dist/main/config"
```

ZIP the `dist` folder.

# Bugs
* Windows 8: It seems like the script won't work (cannot find html elements) on `--headless` mode in Windows 8.
This could be because of Instagram auto sending the current region language. *Might* have been fixed already, not tested.

# ToDo

* `chromedriver` links have changed, need to fix this.

* **429 error workaround:** Navigate to post through the Instagram UI instead of directly going to the URL. Also stop refreshing each time we post.

* Restart the script if it crashes.

* Self-updating application.

* Support for Firefox browser.

* Option to get tags from followings/followers instead of using `tags.txt`.

* <s>Display a message when ChromeDriver and Chrome versions don't match.</s>
* <s>Set browser locale to English (`en_US`) with ChromeDriver.</s>
* <s>Auto download ChromeDriver binaries if it does not exist.</s>
* <s>Cross-platform availability.</s>
* <s>Create a `start()` method in the `InstaBot` class and do the work there.</s>
* <s>Create a `Helper` class and keep certain functions there.</s>
* <s>User-Agent selection depending on the platform.</s>
* <s>Random time between each letter in `InstaBot.typePhrase()`</s>
* <s>Allow user to create, inside `config.json`, the format of comment that will be used.<br>
Example: `[tag] [tag] 42 euro size`</s>
