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
1. Rename `config-sample.json` to `config.json` inside the `config` folder.
2. In `config.json` fill in your username and password in the corresponding fields. Also fill in the Instagram post URL.<br>
You could also set `debug` to true to see what's going on while the program is running (this will give you many messages).<br>
If you are not aware of other variables in `config.json`, I would suggest not edit anything else.
4. Create a `tags.txt` file inside the `config` folder. Each line in this file will be a new tag in your tags list.

# ToDo
1. Auto download ChromeDriver if it does not exist.
2. <s>Random time between each letter in InstaBot.typePhrase()</s>
3. Allow user to create, inside `config.json`, the format of comment that will be used.<br>
Example: `[tag] [tag] 42 euro size`
4. Run worker for 8 hours and have a break of 8 hours each time to prevent limits. Check if this is valid with the HOUR break.
5. Self-updating application.
6. Support for Firefox browser.
