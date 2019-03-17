import sys

import _configs
import _words
import IgBot

def print_help():
    print("")
    print("Correct usage: " + sys.argv[0] + " number_of_accounts")
    print("  number_of_accounts: Number of accounts to be created")
    print("Use '" + sys.argv[0] + " help' to display this message again")

if __name__ == "__main__":
    if (sys.argv[1] == "help") or (len(sys.argv) != 2):
        print_help()
    else:
        bot = IgBot.IgBot()

        bot.open_browser()
        for i in range(int(sys.argv[1])):
            account = bot.generate_acc_details()
            bot.create_account(account["email"], account["name"], account["username"], account["password"])
            bot.save_to_csv(_configs.new_accounts_file, account["email"], account["name"], account["username"], account["password"])
            
            bot.close_browser()

        print("")
        print("Done!")
        bot.quit()
    
    

        

