import sys

import _configs
import _words
import IgBot
   
def print_help():
    print("")
    print("Correct usage: " + sys.argv[0] + " mode targets")
    print("  mode: 'follow' or 'unfollow'. 'follow' will follow all targets. 'unfollow' will unfollow all targets.")
    print("  targets: List of users to be followed/unfollowed. Comma separated (e.g. user1,user2,user3,user4).")
    print("Use '" + sys.argv[0] + " help' to display this message again.")

if __name__ == "__main__":
    if (sys.argv[1] == "help") or (len(sys.argv) != 3):
        print_help()
    else:
        if sys.argv[1] == "follow":
            bot = IgBot.IgBot()
            targets = sys.argv[2].split(',')
            accounts = bot.load_from_csv(_configs.working_accounts_file)

            for account in accounts:
                bot.open_browser()
                bot.log_in(account["username"], account["password"])

                bot.follow(targets)

                bot.driver.close()

            print("Done!")
            bot.quit() 
        elif sys.argv[1] == "unfollow":
            bot = IgBot.IgBot()
            targets = sys.argv[2].split(',')
            accounts = bot.load_from_csv(_configs.working_accounts_file)
            
            for account in accounts:
                bot.open_browser()
                bot.log_in(account["username"], account["password"])

                bot.unfollow(targets)

                bot.driver.close()

            print("Done!")
            bot.quit() 
        else:  #Invalid mode
            print_help()

        

