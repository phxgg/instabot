# InstaBot

### *This is under construction*

Auto commenting bot for Instagram.

Works great on multi-participation allowed giveaways.

# Installation
1. Install Python 3.8 (or later) & pip from https://www.python.org/
2. Use `pip install -r requirements.txt` to install the requirements.
3. Download the latest stable release of ChromeDriver from https://chromedriver.chromium.org/<br>*[you will have to have Google Chrome installed and updated to latest version]*
4. Include ChromeDriver path to your `PATH` system environment variable.

# How to use
1. Rename `config-sample.json` to `config.json` and `tags-sample.txt` to `tags.txt` inside the `config` folder.
2. In `config.json` fill in your username and password in the corresponding fields. Also fill in the Instagram post URL.<br>
You could also set `debug` to true or `keepCommentLogs` to true, to get debug messages or keep logs of the posted comments.<br>
If you are not aware of other variables in `config.json`, I would suggest not edit anything else.
3. Create a `tags.txt` file inside the `config` folder. Each line in this file will be a new tag in your tags list.

<u><b>Notes:</b></u>
* You need to have 2FA disabled on your Instagram account.
* The more tags you use, the safer your account will be.
This is because Instagram will limit accounts that make the same comment over and over again,
so less tags means you're most likely to make a comment you have already made before.

# ToDo
* Self-updating application.
* Support for Firefox browser.
* Option to get tags from followings/followers instead of using `tags.txt`.
* Enable maximum number of comments per day to prevent Instagram from limiting.
* Auto download ChromeDriver binaries if it does not exist.<br>
<i>(This might not work, because ChromeDriver gave an error that it needs to be in PATH. This means the user has to do that manually.)</i>
* Cross-platform availability <i>(after the above is done)</i>
* <s>Create a `start()` method in the `InstaBot` class and do the work there.</s>
* <s>Create a `Helper` class and keep certain functions there.</s>
* <s>User-Agent selection depending on the platform.</s>
* <s>Random time between each letter in `InstaBot.typePhrase()`</s>
* <s>Allow user to create, inside `config.json`, the format of comment that will be used.<br>
Example: `[tag] [tag] 42 euro size`</s>
