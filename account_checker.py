import sys

import _configs
import _words
import IgBot

def print_help():
    print("")
    print("Correct usage: " + sys.argv[0] + " [source_file working_file banned_file]")
    print("  source_file: (optional) File with accounts to be checked. Defaults to 'accounts/new_accounts.csv'.")
    print("  working_file: (optional) File to place working accounts. Defaults to 'accounts/working_accounts.csv'.")
    print("  banned_file: (optional) File to place banned accounts. Defaults to 'accounts/banned_accounts.csv'.")
    print("Use '" + sys.argv[0] + " help' to display this message again.")

if __name__ == "__main__":

    if ((len(sys.argv) > 1) and (sys.argv[1] == "help")) or ((len(sys.argv) != 4) and (len(sys.argv) != 1)):
        print_help()
    else:
        #Gets source file from arguments if present or uses default
        if(len(sys.argv) >= 2):
            source_file = sys.argv[1]
        else:
            source_file = _configs.new_accounts_file
        
        #Gets working file from arguments if present or uses default
        if(len(sys.argv) >= 3):
            working_file = sys.argv[2]
        else:
            working_file = _configs.working_accounts_file
        
        #Gets banned file from arguments if present or uses default
        if(len(sys.argv) >= 4):
            banned_file = sys.argv[3]
        else:
            banned_file = _configs.banned_accounts_file

        bot = IgBot.IgBot()

        accounts = bot.load_from_csv(source_file)

        for account in accounts:
            bot.open_browser()
            status = bot.check_account(account["username"], account["password"])

            if(status == "banned"):
                bot.move_account(account, source_file, banned_file)
            elif(status == "ok"):
                bot.move_account(account, source_file, working_file)

            bot.close_browser()

        bot.quit()

        print("")
        print("Done!")