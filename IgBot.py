from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import selenium.common.exceptions
from math import floor
import time
import random
import sys
import csv
import os
import string
import autoit
import re

import _configs
import _words

class IgBot:
    #Initializes the bot and sets browser options
    def __init__(self):
        print("Initializing...")

        if(_configs.browser == "chrome"):
            self.browser_options = webdriver.ChromeOptions()
        
        #Uses a random proxy from the list in _configs
        proxy_server = random.choice(_configs.proxy_server_list)
        if(_configs.browser == "chrome"):
            self.browser_options.add_argument("--proxy-server=%s" % proxy_server)
        
        #Removes warning/error messages in console
        if(_configs.browser == "chrome"):
            self.browser_options.add_argument("log-level=3")
            
        #Sets localization to US english 
        if(_configs.browser == "chrome"):
            self.browser_options.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})

    #Loads accounts from a CSV file and returns a list with all account information
    def load_from_csv(self, file_path):
        print("Loading accounts...")
        
        with open(file_path, mode='r') as accounts_file:
            account_reader = csv.reader(accounts_file, delimiter=',', quotechar='"')
            next(account_reader)  #Skips header
            
            #Saves every account as a dictionary in a list
            accounts = []
            for row in account_reader:
                accounts.append({
                    "email" : row[0],
                    "name" : row [1],
                    "username" : row [2],
                    "password" : row [3]
                })

        print("Accounts loaded")
        return accounts
 
    #Saves account to a CSV file
    def save_to_csv(self, file_path, email, name, username, password): 
        print("Saving account...")

        with open(file_path, mode='a', newline='') as accounts_file:
            account_writer = csv.writer(accounts_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            
            #Writes header if the file is new or empty
            if (not os.path.isfile(file_path)) or (os.path.getsize(file_path) == 0):
                print("  New file, writing header...")
                account_writer.writerow(["email", "name", "username", "password"])
            
            account_writer.writerow([email, name, username, password])
        
        print("Account saved")

    #Moves an account from one file to the other
    def move_account(self, account, origin_file, destination_file):
        print("Moving " + account["username"] + " from '" + re.sub("(.*/)*", "", origin_file) + "' to '" + re.sub("(.*/)*", "", destination_file) + "' ...")
        modified_origin = [] #Accounts to be kept in the origin file
        file_found = False #Flag to determine if the file was found or not

        #Searches for the account in origin file
        with open(origin_file, mode='r') as origin: 
            origin_reader = csv.reader(origin, delimiter=',', quotechar='"')
            next(origin_reader) #Skips header

            for row in origin_reader:
                #Check if account is in the origin file
                if (row[0] == account["email"] and
                row[1] == account["name"] and
                row[2] == account["username"] and
                row[3] == account["password"]):
                    file_found = True
                else:
                    modified_origin.append({
                        "email" : row[0],
                        "name" : row[1],
                        "username" : row[2],
                        "password" : row[3]
                    })

        if(file_found):
            #Adds account to the destination file
            with open(destination_file, mode='a', newline='') as destination:
                destination_writer = csv.writer(destination, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                destination_writer.writerow([account["email"], account["name"], account["username"], account["password"]])

            #Rewrites the origin file to remove the account
            with open(origin_file, mode='w', newline='') as origin:
                origin_writer = csv.writer(origin, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                origin_writer.writerow(["email", "name", "username", "password"])
                for account in modified_origin:
                    origin_writer.writerow([account["email"], account["name"], account["username"], account["password"]])
            
            print("Account moved")
        else:
            print("  Account not found in origin!")
                    
    #Opens the browser using the options set in __init__
    def open_browser(self):
        print("Opening browser...")
        
        if(_configs.browser == "chrome"):
            self.driver = webdriver.Chrome(options=self.browser_options)
        elif(_configs.browser == "firefox"):
            self.driver = webdriver.Firefox(options=self.browser_options)

    #Closes current browser window
    def close_browser(self):
        print("Closing browser...")

        self.driver.close()

    #Opens a new browser tab
    def open_tab(self):
        print("Opening new tab...")

        if(_configs.os == "mac"):
            self.driver.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 't')
        else:
            self.driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 't')

    #Closes current browser tab
    def close_tab(self):
        print("Closing current tab")

        if(_configs.os == "mac"):
            self.driver.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 'w')
        else:
            self.driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 'w')

    #Ends session, killing the driver
    def quit(self):
        print("Killing driver...")
        
        self.driver.quit()

    #Navigates to the login page and logs in with the specified account
    def log_in(self, username, password):
        print("Logging in as " + username + "...")
        
        self.driver.get('https://www.instagram.com/accounts/login/')
        time.sleep(1)

        field_username = self.driver.find_element_by_name('username')
        field_username.send_keys(username)

        field_password = self.driver.find_element_by_name('password')
        field_password.send_keys(password)

        time.sleep(1.5)

        login_button = self.driver.find_element_by_xpath("//div[text() = 'Log In']/..")
        login_button.click()
        time.sleep(5)

    #Follows all the targets with the current account
    def follow(self, targets):
        print("Following targets...")
        
        if len(targets) == 0:
            print("  Targets list is empty!")
            return
        
        for target in targets:
            print("  Following " + target + "...")

            self.driver.get("https://www.instagram.com/" + target)
            time.sleep(2)

            try:
                follow_button = self.driver.find_element_by_xpath("//button[text() = 'Follow']")
                follow_button.click()

                time.sleep(0.5)
            except:
                print("    Already following " + target + "!")
    
    #Unfollows all the targets with the current account
    def unfollow(self, targets):
        print("Unfollowing targets...")
        
        if len(targets) == 0:
            print("  Targets list is empty!")
            return
        
        for target in targets:
            print("  Unfollowing " + target + "...")

            self.driver.get("https://www.instagram.com/" + target)
            time.sleep(1)

            try:
                unfollow_button = self.driver.find_element_by_xpath("//button[text() = 'Following']")
                unfollow_button.click()

                time.sleep(0.5)

                confirm_button = self.driver.find_element_by_xpath("//button[text() = 'Unfollow']")
                confirm_button.click()

                time.sleep(0.5)
            except:
                print("    Not following " + target + "!")
    
    #Opens the current account's profile page
    def open_profile(self):
        print("Opening profile...")
        
        self.driver.get('https://www.instagram.com/accounts/edit/')

    #Sets a profile picture from the profile_images folder if the account doesn't have one yet
    def set_profile_picture(self):
        print("Setting profile picture...")

        try:
            picture_icon = self.driver.find_element_by_xpath("//button[@title='Add a profile photo']")
            picture_icon.click()            

            #Selects a random picture from the "profile_images" folder
            image_path = os.path.dirname(os.path.realpath(__file__)) + "\profile_images\\128_%03d.jpg\\" % random.randint(1,73)

            #Handles the native file upload window interaction
            handle = "[CLASS:#32770; TITLE:Open]"
            autoit.win_wait(handle, 60)
            autoit.control_set_text(handle, "Edit1", image_path)
            autoit.control_click(handle, "Button1") 
        except:
            print("  Account already has a profile picture")

    #Sets a random gender if it doesn't have one yet
    def set_gender(self):
        print("Setting gender...")

        gender = self.driver.find_element_by_xpath("//select[@id='pepGender']")
        if(gender.get_attribute("value") != 3):
            print("  Already has a gender!")
        else:
            gender_option = self.driver.find_element_by_xpath("//select[@id='pepGender']/option[@value='%i']" % random.randint(1,2))
            gender_option.click()  

    #Generates and returns bio from sentences and hashtags
    def generate_bio(self, language=_words.BIO_EN):
        bio = ""
        
        #Adds random sentences to the bio
        for i in range(random.randint(2, 6)):
            bio += random.choice(_words.bio_sentences[language]) + ' '    
        
        bio += "\n"

        #Adds random hashtags to the bio
        for i in range(random.randint(0,5)):
            bio += random.choice(_words.hashtags) + ' '
        
        return bio

    #Writes the generated bio in the bio text box if the account doesn't have one yet
    def set_bio(self):
        print("Writing bio...")

        bio_text_box = self.driver.find_element_by_xpath("//textarea[@id='pepBio']")

        if(bio_text_box.text != ""):
            print("  Already has a bio!")
        else:
            bio_text_box.send_keys("    ")  #For some reason the first sentence gets cut off without this

            bio = self.generate_bio()
            print("  \"" + bio + "\"")
            bio_text_box.send_keys(bio)
            time.sleep(1)

    #Saves profile after editing
    def save_profile(self):
        submit_button = self.driver.find_element_by_xpath("//button[contains(text(), 'Submit')]")
        submit_button.click()

    #Generates name from random first name and last name
    def generate_name_from_names(self):
        name = random.choice(_words.first_names) + " " + random.choice(_words.last_names)

        return name

    #Generates and returns username from random adjective, color, thing and 4 digit number
    def generate_username_from_things(self):
        username = random.choice(_words.adjectives) + random.choice(_words.colors) + random.choice(_words.things) + str(random.randint(0, 9999))
        
        #Generates another username if the previous is too long
        while len(username) > 26:
            username = random.choice(_words.adjectives) + random.choice(_words.colors) + random.choice(_words.things) + str(random.randint(0, 9999))
        
        return username

    #Generates username from first name, last name and 4 digit number
    def generate_username_from_name(self, name):
        username = re.sub(' ', '', name.lower()) + str(random.randint(0,9999))

        return username
    
    #Generates e-mail from e-mails list and random alias
    def generate_email(self):
        #Generates a random number of random alphanumeric characters to use for the e-mail alias
        alias = ""
        for i in range(random.randint(1, 10)):
            random_char = random.choice(string.ascii_letters + string.digits)
            alias = alias + random_char
        
        #Adds alias to random e-mail from list
        email = re.sub('@', '+' + alias + '@', random.choice(_configs.email_list))
        return email

    #Returns a random password from the passwords list
    def generate_password(self):
        password = random.choice(_configs.password_list)
        return password

    #Generates and returns a dictionary with all account details (e-mail, name, username and password)
    def generate_acc_details(self):
        print("Generating account details...")

        email = self.generate_email()
        name = self.generate_name_from_names()

        #Generates username based on _configs.py settings
        if(_configs.generate_username_from == "name"):
            username = self.generate_username_from_name(name)
        else:
            username = self.generate_username_from_things()

        password = self.generate_password()

        account = {
            "email" : email,
            "name" : name,
            "username" : username,
            "password" : password
        }

        print("  E-mail: " + account["email"])
        print("  Name: " + account["name"])
        print("  Username: " + account["username"])
        print("  Password: " + account["password"])

        return account

    #Returns username for the currently logged in account
    def get_own_username(self):
        #Gets link to profile
        own_profile = self.driver.find_element_by_xpath("//span[contains(@class, 'glyphsSpriteUser__outline')]").find_element_by_xpath("..")
        #Extracts username from link
        own_username = own_profile.get_attribute("href").replace("https://www.instagram.com/", "").replace("/", "")
        
        return own_username

    #Fills the sign up form and creates an account
    def create_account(self, email, name, username, password):
        print("Creating account...")
        self.driver.get('https://www.instagram.com/')
        time.sleep(1)
        
        field_email = self.driver.find_element_by_name('emailOrPhone')
        field_email.send_keys(email)

        field_name = self.driver.find_element_by_name('fullName')
        field_name.send_keys(name)

        field_username = self.driver.find_element_by_name("username")
        field_username.send_keys(username)

        field_password = self.driver.find_element_by_name('password')
        field_password.send_keys(password)

        signup_button = self.driver.find_element_by_xpath("//button[text() = 'Sign up']")
        signup_button.click() 

        time.sleep(5)

    #Checks if the account is banned. Returns "banned" or "ok"
    def check_account(self, username, password):
        print("Checking account " + username + "...")
        self.log_in(username, password)
        try:
            banned_text = self.driver.find_element_by_xpath("//*[@id='slfErrorAlert']")
            print("  " + username + " is BANNED!")
            return "banned"
        except:
            print("  " + username + " is ok")
            return "ok"

    #Loads and returns a list of links to 'num_posts' posts starting from post number 'start'. 'target' can be a user or a hashtag (use the # symbol).
    def get_posts(self, target, num_posts=12, start=0):
        print("Loading " + str(num_posts) + " pictures...")

        if(target[0] == '#'):	#Target is a hashtag
        	self.driver.get("https://www.instagram.com/explore/tags/" + target[1:])
        else:	#Target is a profile
        	self.driver.get('https://www.instagram.com/' + target)
        time.sleep(1)

        num_scrolls = floor((start+num_posts-1) / 12)  #Number of times to scroll the page to load all pictures. Pictures are loded in batches of 12.

        #Loads the required amount of pictures
        for i in range(num_scrolls):
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)

        #Finds all pictures on the page and grabs the links
        pictures = self.driver.find_elements_by_xpath("//a[contains(@href, '/p/')]")
        links = [element.get_attribute("href") for element in pictures]
        
        #Returns the correct section of the list
        return links[start:(start+num_posts)]

    #Likes 'percentage'% of 'target''s posts starting from 'start' until 'num_posts' is reached
    def like_posts(self, target, num_posts=10, percentage=100, start=0):
        print("Liking " + target + "'s posts...")

        self.driver.get('https://www.instagram.com/' + target)
        time.sleep(1)

        first_post = self.driver.find_element_by_xpath("//a[contains(@href, '/p/')]")
        first_post.click()
        time.sleep(1)

        posts_liked = 0
        posts_skipped = 0

        #Skips to starting point
        for i in range(start):
            try:
                right_arrow = self.driver.find_element_by_xpath("//a[contains(@class, 'coreSpriteRightPaginationArrow')]")
                right_arrow.click()
                time.sleep(1)
            except:
                print("Couldn't get to starting point! Not enough posts!")
                return

        while (posts_liked < num_posts):
            try:
                #Checks if post is not yet liked
                self.driver.find_element_by_xpath("//button/span[contains(@class, 'glyphsSpriteHeart__outline')]")
                
                #Randomly skips posts
                if(random.randint(0,100) <= percentage):
                    like_button = self.driver.find_element_by_xpath("//button[contains(@class, 'coreSpriteHeartOpen')]")
                    like_button.click()

                    posts_liked += 1
                    print("  Post liked")
                else:
                    posts_skipped += 1
                    print("  Post skipped")
            except:
                print("  Post already liked!")

            #Checks if done
            if(posts_liked == num_posts):
                print("Liked " + str(posts_liked) + " posts and skipped " + str(posts_skipped) + " possible posts.")
                return
            
            #Moves on to the next post
            try:
                right_arrow = self.driver.find_element_by_xpath("//a[contains(@class, 'coreSpriteRightPaginationArrow')]")
                right_arrow.click()
                time.sleep(1)
            except:
                print("Reached last post!")
                print("Liked " + str(posts_liked) + " posts and skipped " + str(posts_skipped) + " possible posts.")
                return

    #Unlikes 'percentage'% of 'target''s posts starting from 'start' until 'num_posts' is reached
    def unlike_posts(self, target, num_posts=10, percentage=100, start=0):
        print("Unliking " + target + "'s posts...")

        self.driver.get('https://www.instagram.com/' + target)
        time.sleep(1)

        first_post = self.driver.find_element_by_xpath("//a[contains(@href, '/p/')]")
        first_post.click()
        time.sleep(1)

        posts_unliked = 0
        posts_skipped = 0
        while (posts_unliked < num_posts):
            try:
                #Checks if post is liked
                self.driver.find_element_by_xpath("//button/span[contains(@class, 'glyphsSpriteHeart__filled')]")
                
                #Randomly skips posts
                if(random.randint(0,100) <= percentage):
                    like_button = self.driver.find_element_by_xpath("//button[contains(@class, 'coreSpriteHeartOpen')]")
                    like_button.click()

                    posts_unliked += 1
                    print("  Post unliked")
                else:
                    posts_skipped += 1
                    print("  Post skipped")
            except:
                print("  Post not liked!")

            #Checks if done
            if(posts_unliked == num_posts):
                print("Unliked " + str(posts_unliked) + " posts and skipped " + str(posts_skipped) + " possible posts.")
                return
            
            #Moves on to the next post
            try:
                right_arrow = self.driver.find_element_by_xpath("//a[contains(@class, 'coreSpriteRightPaginationArrow')]")
                right_arrow.click()
                time.sleep(1)
            except:
                print("Reached last post!")
                print("Unliked " + str(posts_unliked) + " posts and skipped " + str(posts_skipped) + " possible posts.")
                return

    #Loads comments up to page 'page'. Set 'page' to 0 to load all comments (might take a while)
    def load_comment_pages(self, page):
        if (page == 0):
            try:
                while True:
                    load_more_comments = self.driver.find_element_by_xpath("//button[text() = 'Load more comments']")
                    load_more_comments.click()
                    time.sleep(1)
            except:
                pass
        else:
            for i in range(page-1):
                load_more_comments = self.driver.find_element_by_xpath("//button[text() = 'Load more comments']")
                load_more_comments.click()
                time.sleep(1)

    #Returns a list with number of comments from 'targets' in 'post' up to page 'pages'. Set 'pages' to 0 to check all pages. Set 'post' to empty to use current page.
    def count_comments(self, post, targets, pages=3):
        print("Finding comments by " + str(targets) + "...")
        
        if(post != ""):
            self.driver.get(post)
            time.sleep(1)

        self.load_comment_pages(pages)

        #Gets all comments
        comments = self.driver.find_elements_by_xpath("//h3/a[contains(@class, 'notranslate') and not(contains(text(), '@'))]")
        print("  " + str(len(comments)) + " comments loaded")

        #Gets all usernames from comments
        num_comments = []
        for target in targets:
            num_comments.append(len([username.text for username in comments if username.text == target]))

        print("  " + str(num_comments) + " comments found")
        return num_comments

    #Generates a comment from a random comment and random hashtags
    def generate_comment(self):
        comment = random.choice(_words.comments[_words.COMMENTS_EN])
        
        for i in range(random.randint(0,4)):
            comment += " " + random.choice(_words.hashtags)

        return comment

    #Comments on 'percentage'% of 'target''s posts starting from 'start' until 'num_posts' is reached. Skips posts that have 'max_comments' from you.
    def comment_posts(self, target, num_posts=10, percentage=100, start=0, max_comments=1):
        print("Commenting on " + target + "'s posts...")

        self.driver.get('https://www.instagram.com/' + target)
        time.sleep(1)

        first_post = self.driver.find_element_by_xpath("//a[contains(@href, '/p/')]")
        first_post.click()
        time.sleep(1)

        posts_commented = 0
        posts_skipped = 0

        #Skips to starting point
        for i in range(start):
            try:
                right_arrow = self.driver.find_element_by_xpath("//a[contains(@class, 'coreSpriteRightPaginationArrow')]")
                right_arrow.click()
                time.sleep(1)
            except:
                print("Couldn't get to starting point! Not enough posts!")
                return

        while (posts_commented < num_posts):
            #Checks if post is not yet commented
            num_comments = self.count_comments("", [self.get_own_username()], 0)
            #Skips posts already commented
            if (num_comments[0] != 0):
                print("  Post already commented!")
            else:
                #Randomly skips posts
                if(random.randint(0,100) <= percentage):
                    comment_text_box = self.driver.find_element_by_xpath("//textarea[@placeholder='Add a comment…']")
                    comment_text_box.click()
                    comment_text_box = self.driver.find_element_by_xpath("//textarea[@placeholder='Add a comment…']")
                    comment_text_box.send_keys(self.generate_comment())
                    comment_text_box.submit()
                    time.sleep(1)

                    posts_commented += 1
                    print("  Post commented")
                else:
                    posts_skipped += 1
                    print("  Post skipped")

            #Checks if done
            if(posts_commented == num_posts):
                print("Commented " + str(posts_commented) + " posts and skipped " + str(posts_skipped) + " possible posts.")
                return
            
            #Moves on to the next post
            try:
                right_arrow = self.driver.find_element_by_xpath("//a[contains(@class, 'coreSpriteRightPaginationArrow')]")
                right_arrow.click()
                time.sleep(2)
            except:
                print("Reached last post!")
                print("Commented " + str(posts_commented) + " posts and skipped " + str(posts_skipped) + " possible posts.")
                return

    #If target is a post, deletes all but 'comments_to_leave' comments. If target is a profile, deletes all but 'comments_to_leave' comments from 'percentage'% of 'target''s posts starting from 'start' until 'num_posts' is reached. 
    def delete_comments(self, target, num_posts=1, percentage=100, start=0, comments_to_leave=0):
        print("Deleting comments from " + target + "...")
        if("/" not in target):
            target = "https://www.instagram.com/" + target + "/"

        if (target != ""):
            self.driver.get(target)
            time.sleep(1)
        else:
            target = self.driver.current_url

        posts_deleted = 0
        posts_skipped = 0
        comments_deleted = 0

        if(target[25:28] == "/p/"):  #Target is a post
            more_options = self.driver.find_element_by_xpath("//span[@aria-label='More options']")
            more_options.click()
            time.sleep(1)

            try:
                remove_comments = self.driver.find_element_by_xpath("//button[text()='Remove comments']")
                remove_comments.click()
                time.sleep(1)

                delete_buttons = self.driver.find_elements_by_xpath("//button[@title='Delete Comment']")
                #Leaves out 'comments_to_leave' comments
                for i in range(comments_to_leave):
                    delete_buttons.remove(random.choice(delete_buttons))
                
                #Deletes comments
                for delete_button in delete_buttons:
                    delete_button.click()
                    time.sleep(1)
                    confirm_delete = self.driver.find_element_by_xpath("//button[text()='Delete Comment' and @tabindex='0']")
                    confirm_delete.click()
                    time.sleep(1)
                    comments_deleted += 1                        
            except:
                print("  No comments to delete!")
                cancel = self.driver.find_element_by_xpath("//button[text()='Cancel']")
                cancel.click()
                time.sleep(1)
            
            #Done
            print("Deleted " + str(comments_deleted) + " comments on " + str(posts_deleted) + " posts and skipped " + str(posts_skipped) + " possible posts.")
        else:  #Target is a profile
            first_post = self.driver.find_element_by_xpath("//a[contains(@href, '/p/')]")
            first_post.click()
            time.sleep(1)

            #Skips to starting point
            for i in range(start):
                try:
                    right_arrow = self.driver.find_element_by_xpath("//a[contains(@class, 'coreSpriteRightPaginationArrow')]")
                    right_arrow.click()
                    time.sleep(1)
                except:
                    print("Couldn't get to starting point! Not enough posts!")
                    return

            while (posts_deleted < num_posts):
                more_options = self.driver.find_element_by_xpath("//span[@aria-label='More options']")
                more_options.click()
                time.sleep(1)
                
                #Checks if post has comments to delete
                try:
                    remove_comments = self.driver.find_element_by_xpath("//button[text()='Remove comments']")
                    remove_comments.click()
                    time.sleep(1)

                    delete_buttons = self.driver.find_elements_by_xpath("//button[@title='Delete Comment']")

                    #Randomly skips posts
                    if(random.randint(0,100) <= percentage):
                        #Leaves out 'comments_to_leave' comments
                        for i in range(comments_to_leave):
                            delete_buttons.remove(random.choice(delete_buttons))

                        #Deletes comments
                        for delete_button in delete_buttons:
                            delete_button.click()
                            time.sleep(1)
                            confirm_delete = self.driver.find_element_by_xpath("//button[text()='Delete Comment' and @tabindex='0']")
                            confirm_delete.click()
                            time.sleep(1)
                            comments_deleted += 1 

                        posts_deleted += 1
                        print("  Comments deleted")
                    else:
                        posts_skipped += 1
                        print("  Post skipped")
                        
                        cancel = self.driver.find_element_by_xpath("//button[text()='Cancel']")
                        cancel.click()
                        time.sleep(1)

                    more_options.click()
                    time.sleep(1)

                    finish_deleting = self.driver.find_element_by_xpath("//button[text()='Finish removing comments']")
                    finish_deleting.click()
                    time.sleep(1)

                except:
                    print("  No comments to delete!")
                    cancel = self.driver.find_element_by_xpath("//button[text()='Cancel']")
                    cancel.click()
                    time.sleep(1)
                
                #Checks if done
                if(posts_deleted == num_posts):
                    print("Deleted " + str(comments_deleted) + " comments on " + str(posts_deleted) + " posts and skipped " + str(posts_skipped) + " possible posts.")
                    return
                
                #Moves on to the next post
                try:
                    right_arrow = self.driver.find_element_by_xpath("//a[contains(@class, 'coreSpriteRightPaginationArrow')]")
                    right_arrow.click()
                    time.sleep(2)
                except:
                    print("Reached last post!")
                    print("Deleted " + str(comments_deleted) + " comments on " + str(posts_deleted) + " posts and skipped " + str(posts_skipped) + " possible posts.")
                    return   

    #Likes 'percentage'% of comments from 'targets' within 'pages' pages in 'post' until 'num_comments' is reached. Leave 'post' empty to use current page.
    def like_comments(self, targets, post="", num_comments=3, percentage=100, pages=1):
        print("Liking comments from " + str(targets) + " in " + post + "...")

        if (post != ""):
            self.driver.get(post)
            time.sleep(1)
        else:
            post = self.driver.current_url

        self.load_comment_pages(pages)

        #Gets usernames and buttons for all comments
        usernames = self.driver.find_elements_by_xpath("//h3/a[contains(@class, 'notranslate') and not(contains(text(), '@'))]")
        like_buttons = self.driver.find_elements_by_xpath("//span[contains(@class, 'glyphsSpriteComment_like')]")
        print("  " + str(len(usernames)) + " comments loaded")

        comments_liked = 0
        comments_skipped = 0
        for index, username in enumerate(usernames):
            if (username.text in targets):  #Potential comment to like
                if("glyphsSpriteComment_like_active" in like_buttons[index].get_attribute("class")):  #Checks if comment is already liked
                    print("  Comment already liked!")
                else:
                    #Randomly skips posts
                    if(random.randint(0,100) <= percentage):
                        like_buttons[index].find_element_by_xpath("..").click()  #Clicks parent element (the actual button)
                        time.sleep(1)

                        comments_liked += 1
                        print("  Comment liked")
                    else:
                        comments_skipped += 1
                        print("  Comment skipped")
            
            #Checks if done
            if(comments_liked == num_comments):
                print("Liked " + str(comments_liked) + " comments and skipped " + str(comments_skipped) + " possible comments.")
                return

    #Unlikes 'percentage'% of comments from 'targets' within 'pages' pages in 'post' until 'num_comments' is reached. Leave 'post' empty to use current page.
    def unlike_comments(self, targets, post="", num_comments=3, percentage=100, pages=1):
        print("Unliking comments from " + str(targets) + " in " + post + "...")

        if (post != ""):
            self.driver.get(post)
            time.sleep(1)
        else:
            post = self.driver.current_url

        self.load_comment_pages(pages)

        #Gets usernames and buttons for all comments
        usernames = self.driver.find_elements_by_xpath("//h3/a[contains(@class, 'notranslate') and not(contains(text(), '@'))]")
        like_buttons = self.driver.find_elements_by_xpath("//span[contains(@class, 'glyphsSpriteComment_like')]")
        print("  " + str(len(usernames)) + " comments loaded")

        comments_unliked = 0
        comments_skipped = 0
        for index, username in enumerate(usernames):
            if (username.text in targets):  #Potential comment to unlike
                if("glyphsSpriteComment_like_active" in like_buttons[index].get_attribute("class")):  #Checks if comment is liked
                    #Randomly skips posts
                    if(random.randint(0,100) <= percentage):
                        like_buttons[index].find_element_by_xpath("..").click()  #Clicks parent element (the actual button)
                        time.sleep(1)

                        comments_unliked += 1
                        print("  Comment unliked")
                    else:
                        comments_skipped += 1
                        print("  Comment skipped")
                else:
                    print("  Comment not liked!")
            
            #Checks if done
            if(comments_unliked == num_comments):
                print("Liked " + str(comments_unliked) + " comments and skipped " + str(comments_skipped) + " possible comments.")
                return

    #Follows 'num_follows' accounts from the suggested accounts page
    def follow_suggested(self, num_follows=10):
        followed = 0
        while(followed < num_follows):
            self.driver.get("https://www.instagram.com/explore/people/suggested/")
            time.sleep(1)

            #Load all suggested accounts
            for i in range(3):
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(1)

            self.driver.execute_script("window.scrollTo(0, 0);")

            follow_buttons = self.driver.find_elements_by_xpath("//button[text() = 'Follow']")
            for button in follow_buttons:
                button.click()
                time.sleep(0.5)
                followed += 1

                #Stops if num_follows has been reached
                if(followed == num_follows):
                    break

        print("  " + str(followed) + " accounts followed")

    #Follows the author of 'post'. Leave empty to use current page.
    def follow_author(self, post=""):
    	if (post != ""):
    		if('/' in post):	#Post is a link
    			self.driver.get(post)
    		else:	#Post is an ID
    			self.driver.get("https://www.instagram.com/p/" + post)
    	time.sleep(1)

    	author = self.driver.find_element_by_xpath("//a[contains(@class, 'notranslate')]")
    	self.follow([author.text])









if __name__ == "__main__":
    print("This file has no main! Import this module into your script to use it!")