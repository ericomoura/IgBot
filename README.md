# IgBot
IgBot is a Python module that allows you to create your own Instagram automation scripts. It uses Selenium to handle the browser automation and PyAutoIt to handle the native window automation.

## Installation
1\) Install Python from the official website (https://www.python.org/)

2\) Install Selenium (for more details, refer to the [official website](https://selenium-python.readthedocs.io/installation.html#))
```sh
$ pip install selenium
```
3\) Install PyAutoIt (for more details, refer to the [official website](https://pypi.org/project/PyAutoIt/))
```sh
$ pip install PyAutoIt
```
NOTE: As noted in [this Github issue](https://github.com/jacexh/pyautoit/issues/24), x64 users will run into an error when trying to install PyAutoIt normally. The workaround, as [explained in a comment](https://github.com/jacexh/pyautoit/issues/24#issuecomment-431776853) requires you to download the zip file from the official website and modify the `autoit.py` file before running `setup.py`. In `autoit.py`, change line 15 from `dll = "AutoItX3.dll"` to `dll = "AutoItX3_x64.dll"`. Make sure you save the changes and run `setup.py` normally.

4\) Download the web drivers for the browsers you want to use

|Browser|Download link|
|-|-|
|Chrome|https://sites.google.com/a/chromium.org/chromedriver/downloads|
|Firefox|https://github.com/mozilla/geckodriver/releases|
|Edge|https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/#downloads|

5\) Make sure the web drivers are in your PATH (either add them to your PATH or move them to the Python intallation folder (e.g. `C:/Program Files/Python/Python37`)

## Setup
1\) Open the `_configs.py` file with a text editor
* Change the file locations for `new_accounts_file`, `working_accounts_file` and `banned_accounts_file` to a suitable location in your computer. It is recommended to use the `accounts` folder in your IgBot folder.
* Change the file locations for `test_new_accounts_file`, `test_working_accounts_file` and `test_banned_accounts_file` to a suitable location in your computer. These files are not used during normal use of the module, but can be useful when testing a new script. It is recommended to use the `accounts` folder in your IgBot folder. 
* If you have any proxies you want to use, add them to the `proxy_server_list`. One will be randomly selected for each session.
* If you plan on using IgBot to create Instagram accounts, add at least one valid e-mail to `email_list` (e-mail service NEEDS to support aliases such as johnsmith+somealias@mail.com) and one password to `password_list` (passwords need to follow Instagram's password requirements).
* Change `os` and `browser` according to your system and preference.

2\) Open the `accounts` folder and add any existing accounts to their respective files, as well as remove the example accounts from each file.

## How to use
IgBot is meant to give you the tools needed to create automated Instagram scripts to suit your own needs. 

Import `IgBot.py` to your Python script
```python
import IgBot
```
Create an instance of the IgBot class
```python
bot = IgBot.IgBot()
```

Use the functions provided to you in `IgBot.py` to create your own logic and desired behaviour.
```python
bot.open_browser()
bot.log_in("username", "password")
bot.follow("instagram")
bot.quit()
```

## Examples
A handful of example scripts have been provided along with the module in the root directory of the project. You can run any of the scripts with the "help" argument to check the correct usage of each one.

#### account_checker
Checks if the new accounts are banned or not and moves them to the appropriate file.

#### account_creator
Creates accounts using the emails and passwords from _configs.

#### comment_deleter
Deletes comments you've made in the target's posts.

#### comment_liker_unliker
Likes/unlikes target's posts.

#### commenter
Posts random comments in target's posts.

#### follower_unfollower
Follows/unfollows the targets with all the accounts in `working_accounts_file`.

#### hashtag_follower
Follows authors from posts in the target hashtag page.

#### liker_unliker
Likes/unlikes target's posts.

#### profile_filler
Fills the profile of a given account using randomly generated information.

## Final words
I wrote this module after seing a few other Instagram bots out there and wondering how they worked. Following my curiosity, I learned how Selenium worked and figured I'd give this a shot. To be completely honest, I don't even use Instagram, I was just bored.

Do whatever you want with this software. If you get banned, that's on you. I take no responsibility for what is done using IgBot. I'm providing this code for anyone that might be as bored and curious as I was to learn from. Feel free to poke around in the code and change things, if you feel like it. 

I tried to comment and organize the code so that anyone reading it could understand what everything does, but in case the way any function works isn't clear, you can refer to the documentation below.

There are a few features I'd still like to add, but I have no plans of supporting and updating this project in the future.

## Documentation
### \_\_init__(self)
Runs once when the IgBot instance is created. Browser options are set here.

### load_from_csv(self, file_path)
Loads all accounts from a CSV file and returns a list with all the accounts.
* PARAMETERS:

**file_path**: Path to the CSV file containing the accounts.
* RETURNS: A list of dictionaries, each containing the following keys: *email*, *name*, *username*, *password*. Each account is an item in the list.

### save_to_csv(self, file_path, email, name, username, password)
Saves the account information to a CSV file.
* PARAMETERS:

**file_path**: Path to the CSV file where the account will be saved.

**email**: Account's e-mail.

**name**: Account's full name.

**username**: Account's username.

**password**: Account's password.

### move_account(self, account, origin_file, destination_file)
Moves the account from one CSV file to another.
* PARAMETERS:

**account**: Dictionary containing the account information, with the following keys: *email*, *name*, *username*, *password*.

**origin_file**: File the account will be taken from.

**destination_file**: File the account will be moved to.

### open_browser(self)
Opens a new browser window.

### close_browser(self)
Closes the current browser window.

### open_tab(self)
*WARNING: This function is either not fully implemented or not currently working properly!*

Opens a new tab in the current browser window.

### close_tab(self)
*WARNING: This function is either not fully implemented or not currently working properly!*

Closes the current tab.

### quit(self)
Ends the session, killing the web driver and closing any browser windows or tabs left open.

### log_in(self, username, password)
Logs in to the specified account.
* PARAMETERS:

**username**: Account's username.

**password**: Account's password.

### follow(self, targets)
Follows a set of targets with the currently active account.
* PARAMETERS:

**targets**: List of usernames to follow. 

### unfollow(self, targets)
Unfollows a set of targets with the currently active account.
* PARAMETERS:

**targets**: List of usernames to unfollow.

### open_profile(self)
Opens the active account's profile.

### set_profile_picture(self)
Sets the active account's profile picture to a random image from the `profile_images` folder if the account doesn't have one set yet. Expects the current page to be the active account's profile.

### set_gender(self)
Sets the active account's gender to a random gender if the account doesn't have one set yet. Expects the current page to be the active account's profile.

### generate_bio(self, language)
Generates a bio text using sentences and hashtags from the `_words.py` file.
* PARAMETERS:

**language**: Language to be used in the bio. Values can be found in `_words.py` and follow the format *BIO_XX* where *XX* is the abbreviation for the language (e.g. *BIO_EN*, *BIO_ES*, *BIO_DE*, etc). Defaults to *_words.BIO_EN*.

* RETURNS: A string with the generated bio text.

### set_bio(self)
Sets the active account's bio if it doesn't have one yet. Uses the `generate_bio` function to create the bio text. Expects the current page to be the active account's profile.

### save_profile(self)
Saves changes to the active account's profile after editing it. Expects the current page to be the active account's profile.

### generate_name_from_names(self)
Generates a full name using the first and last names in `_words.py` (e.g. "John Smith").
* RETURNS: A string with the generated name.

### generate_username_from_things(self)
Generates a username using a random combination of adjective, color, thing and 4 digit number (e.g. "chunkycyantoucan2465"). The set of adjectives, colors and things can be found in `_words.py`.
* RETURNS: A string with the generated username.

### generate_username_from_name(self, name)
Generates a username using the provided full name and a random 4 digit number (e.g. "johnsmith4653").
* PARAMETERS:

**name**: The full name to be used.

* RETURNS: A string with the generated username.
 
### generate_email(self)
Generates an e-mail address from the e-mails in `_configs.py` and a randomly generated alias (e.g. johnsmith+sF4fsW2@mail.com).
* RETURNS: A string with the generated e-mail.

### generate_password(self)
Returns a random password from the passwords list in `_configs.py`.
* RETURNS: A string with the password.

### generate_acc_details(self)
Generates all account information using the functions listed above and returns a dictionary with everything.
* RETURNS: A dictionary containing the generated account information with the following keys: *email*, *name*, *username*, *password*.

### get_own_username(self)
Returns the active account's username.
* RETURNS: A string with the active account's username.

### create_account(self, email, name, username, password)
Creates an account with the provided account information. Note that using a bot to make new accounts will probably get your IP and/or e-mail banned from making any accounts at all.
* PARAMETERS:

**email**: Account's e-mail.

**name**: Account's full name.

**username**: Account's username.

**password**: Account's password.

### check_account(self, username, password)
Checks if the account is banned.
* PARAMETERS:

**username**: Account's username.

**password**: Account's password.

* RETURNS: A string with the account's status (*"ok"* or *"banned"*).

### get_posts(self, target, num_posts, start)
Returns a list of links to target's posts.
* PARAMETERS:

**target**: Username of the target or target hashtag with the # symbol.

**num_posts**: Number of posts to get. Defaults to 12.

**start**: Starting point (e.g. start from the 10th post). Defaults to 0.

* RETURNS: A list of strings with the links. Each link is an item in the list.

### like_posts(self, target, num_posts, percentage, start)
Likes posts from the target.
* PARAMETERS:

**target**: Username of the target.

**num_posts**: Number of posts to like in total. Defaults to 10.

**percentage**: Percentage of the target's posts to like (e.g. setting this to 90 will make it so every post has a 10% chance of being skipped). Skipped posts do not count towards the number of posts liked. Defaults to 100.

**start**: Starting point (e.g. start from the 10th post). Defaults to 0.

### unlike_posts(self, target, num_posts, percentage, start)
Unlikes posts from the target.
* PARAMETERS:

**target**: Username of the target.

**num_posts**: Number of posts to unlike in total. Defaults to 10.

**percentage**: Percentage of the target's posts to unlike (e.g. setting this to 90 will make it so every post has a 10% chance of being skipped). Skipped posts do not count towards the number of posts unliked. Defaults to 100.

**start**: Starting point (e.g. start from the 10th post). Defaults to 0.

### load_comment_pages(self, page)
Loads a certain number of comment pages in a post. Expects the current page to be a post.
* PARAMETERS: 

**page**: Page to load up to (e.g. setting this to 3 will load all pages up to and including the third page). Setting this to 0 will load all pages (this may take a while).

### count_comments(self, post, targets, pages)
Counts the number of comments made by the targets in a post.
* PARAMETERS:

**post**: Post to count comments in. Leave blank to use the current page.

**targets**: List of strings with the usernames to count comments from.

**pages**: Number of pages to search for comments in. Setting this to 0 will search all pages (this may take a while). Defaults to 3.

* RETURNS: A list of numbers with the comment count for every target in the same order as provided to the function (e.g. the number for targets[2] will be in the index 2 of the returned list).

### generate_comment(self)
Generates a random comment from the comments and hashtags in `_words.py`.
* RETURNS: A string with the generated comment.

### comment_posts(self, target, num_posts, percentage, start, max_comments)
Comments randomly generated comments in the target's posts. Comments are generated using the `generate_comment()` function.
* PARAMETERS:

**target**: Username of the target.

**num_posts**: Number of posts to comment in. Defaults to 10.

**percentage**: Percentage of posts to comment in (e.g. setting this to 90 will make it so every post has a 10% chance of being skipped). Skipped posts do not count towards the number of posts commented in. Defaults to 100.

**start**: Starting point (e.g. start from the 10th post). Defaults to 0.

**max_comments**: Maximum number of comments from you in a post (e.g. setting this to 2 will make it so every post with at least 2 comments from you is skipped). Defaults to 1.

### delete_comments(self, target, num_posts, percentage, start, comments_to_leave)
Deletes your comments from the target's posts or form a specific post.
* PARAMETERS:

**target**: Username of the target or link to a specific post.

**num_posts**: Number of posts to delete comments from. Defaults to 10.

**percentage**: Percentage of posts to delete comments from (e.g. setting this to 90 will make it so every post has a 10% chance of being skipped). Skipped posts do not count towards the number of posts deleted from. Defaults to 100.

**start**: Starting point (e.g. start from the 10th post). Defaults to 0.

**comments_to_leave**: Minimum number of comments to leave in a post (e.g. setting this to 2 will stop deleting comments if there are 2 or less comments from you in the post). Defaults to 0.

### like_comments(self, targets, post, num_comment, percentage, pages)
Likes comments made by the targets in a post.
* PARAMETERS:

**targets**: List of strings with the usernames to like comments from.

**post**: Post to like comments in. Pass empty string to use current page. Defaults to "".

**num_comment**: Number of comments to like. Defaults to 3.

**percentage**: Percentage of comments to like (e.g. setting this to 90 will make it so every comment has a 10% chance of being skipped). Skipped comments do not count towards the number of comments liked. Defaults to 100.

**pages**: Number of pages to search for comments in. Setting this to 0 will search all pages (this may take a while). Defaults to 1.

### unlike_comments(self, targets, post, num_comment, percentage, pages)
Unlikes comments made by the targets in a post.
* PARAMETERS:

**targets**: List of strings with the usernames to unlike comments from.

**post**: Post to unlike comments in. Pass empty string to use current page. Defaults to "".

**num_comment**: Number of comments to unlike. Defaults to 3.

**percentage**: Percentage of comments to unlike (e.g. setting this to 90 will make it so every comment has a 10% chance of being skipped). Skipped comments do not count towards the number of comments unliked. Defaults to 100.

**pages**: Number of pages to search for comments in. Setting this to 0 will search all pages (this may take a while). Defaults to 1.

### follow_suggested(self, num_follows)
Follows profiles from the suggested profiles page.
* PARAMETERS:

**num_follows**: Number of profiles to follow. Defaults to 10.

### get_author(self, post)
Gets the post's author.
* PARAMETERS:

**post**: Post to get the author from. Leave empty to use the current page.

* RETURNS: A string with the username of the post's author.

### follow_from_hashtag(self, hashtag, num_follows, percentage, start)
Follows authors of posts in the specified hashtag.
* PARAMETERS:

**hashtag**: Hashtag to follow authors in.

**num_follows**: Number of authors to follow in total.

**percentage**: Percentage of authors to follow (e.g. setting this to 90 will make it so every author has a 10% chance of being skipped). Skipped posts do not count towards the number of posts deleted from. Defaults to 100.

**start**: Starting point (e.g. start from the 10th post). Defaults to 0.

