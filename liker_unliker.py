import sys

import _configs
import _words
import IgBot
   
def print_help():
    print("")
    print("Correct usage: " + sys.argv[0] + " mode target amount percentage start")
    print("  mode: 'like' or 'unlike'. 'like' will like the target's posts. 'unlike' will unlike the target's posts.")
    print("  target: User whose posts are going to be like/unliked.")
    print("  amount: Number of posts to be like/unliked in total.")
    print("  percentage: (optional) Chance for each post to be liked/unliked. Skipped posts do not count towards the total amount. Defaults to 100% (every post).")
    print("  start: (optional) Post to start with. Defaults to 0 (first post).")
    print("Use '" + sys.argv[0] + " help' to display this message again.")

if __name__ == "__main__":
    if (sys.argv[1] == "help") or len(sys.argv) < 4 or len(sys.argv) > 6:
        print_help()
    else:
        #Grabs parameters from command line
        target = sys.argv[2]
        amount = int(sys.argv[3])
        if (len(sys.argv) >= 5):
            percentage = int(sys.argv[4])
        else:
            percentage = 100
        if (len(sys.argv) >= 6):
            start = int(sys.argv[5])
        else:
            start = 0

        if (sys.argv[1] == "like"):
            bot = IgBot.IgBot()
            bot.open_browser()
            bot.log_in("username", "password")
            bot.like_posts(target, amount, percentage, start)
        elif (sys.argv[1] == "unlike"):
            bot = IgBot.IgBot()
            bot.open_browser()
            bot.log_in("username", "password")
            bot.unlike_posts(target, amount, percentage, start)
        else:  #Invalid mode
            print_help()