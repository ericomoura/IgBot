import sys

import _configs
import _words
import IgBot

def print_help():
    print("")
    print("Correct usage: " + sys.argv[0] + " single username password")
    print("               or")
    print("               " + sys.argv[0] + " multiple csv_file_path")
    print("  mode: 'single' or 'multiple' accounts. Single takes username/password as arguments. Multiple takes a CSV file as argument.")
    print("  username: Username of the account in single mode.")
    print("  password: Password of the account in single mode.")
    print("  csv_file_path: Path to the CSV file with the accounts. Defaults to 'working_accounts_file' in _configs.py")
    print("Use '" + sys.argv[0] + " help' to display this message again.")

if __name__ == "__main__":
    if (sys.argv[1] == "help") or ((len(sys.argv) > 4) and (len(sys.argv) < 2)):
        print_help()
    else:
        if (sys.argv[1] == "single"):
            bot = IgBot.IgBot()

            bot.open_browser()
            bot.log_in(sys.argv[2], sys.argv[3])

            bot.open_profile()
            bot.set_profile_picture()
            bot.set_bio()
            bot.set_gender()
            bot.save_profile()

            bot.close_browser()

            print("")
            print("Done!")
            bot.quit()
        elif (sys.argv[1] == "multiple"):
            bot = IgBot.IgBot()
            if(len(sys.argv) > 2):
                accounts = bot.load_from_csv(sys.argv[2])
            else:
                accounts = bot.load_from_csv(_configs.working_accounts_file)

            for account in accounts:
                bot.open_browser()
                bot.log_in(account["username"], account["password"])

                bot.open_profile()
                bot.set_profile_picture()
                bot.set_bio()
                bot.set_gender()
                bot.save_profile()

                bot.close_browser()

            print("")
            print("Done!")
            bot.quit()
        else:
            print_help()

    

        

