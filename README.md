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
    * `session_comments` How many comments to make before a 3 minute break happens (<b>recommended:</b> `5`)
    * `per_hour_comments` Maximum number of comments before a 1 hour break happens. (<b>recommended:</b> `50`)
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
