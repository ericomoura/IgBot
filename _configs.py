#####   ACCOUNTS   #####
#Path to CSV file for storing created accounts
new_accounts_file = "C:/IgBot/accounts/new_accounts.csv"
#Path to CSV file for storing working accounts
working_accounts_file = "C:/IgBot/accounts/working_accounts.csv"
#Path to CSV file for storing banned accounts
banned_accounts_file = "C:/IgBot/accounts/banned_accounts.csv"

#Path to test CSV file for storing created accounts
test_new_accounts_file = "C:/IgBot/accounts/test_new_accounts.csv"
#Path to test CSV file for working accounts
test_working_accounts_file = "C:/IgBot/accounts/test_working_accounts.csv"
#Path to test CSV file for working accounts
test_banned_accounts_file = "C:/IgBot/accounts/test_banned_accounts.csv"

#####   PROXY   #####
#List of proxy server IPs (leave empty for no proxy)
proxy_server_list = [""]

#####   ACCOUNT INFO   #####
#List of e-mails to use in account creation. Must support aliases (e.g. mymail+kdW5@mail.com).
email_list = ["myemail1@mail.com", "myemail2@mail.com"]
#Passwords to be used in account creation
password_list = ["password123"]

#Method used to generate username
#"things"   : generates from random adjective, color, thing and number
#"name"     : generates from first name, last name and random number
generate_username_from = "name"

#####   ENVIRONMENT   ###
#Operational system script is running in. Options are "windows", "linux", "mac".
os = "windows"
#Browser to be used. Options are "chrome", "firefox".
browser = "chrome"





if __name__ == "__main__":
    print("This file has no code! Open it with a text editor to edit the configs.")