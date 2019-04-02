import sys

import _configs
import _words
import IgBot
   
def print_help():
    print("")
    print("Correct usage: " + sys.argv[0] + " hashtag num_follows percentage start")
    print("  hashtag: The target hashtag to follow authors from.")
    print("  num_follows: Number of authors to follow in total.")
    print("  percentage: (optional) Chance for each comment to be liked/unliked. Skipped comment do not count towards the total amount. Defaults to 100% (every post).")
    print("  start: (optional) Post to start from. Defaults to 0 (first post).")
    print("Use '" + sys.argv[0] + " help' to display this message again.")

if __name__ == "__main__":
    if (sys.argv[1] == "help") or ((len(sys.argv) < 3) or (len(sys.argv) > 5)):
        print_help()
    else:
        #Grabs parameters from command line
        hashtag = sys.argv[1]
        num_follows = int(sys.argv[2])
        if(len(sys.argv) >= 4):
            percentage = int(sys.argv[3])
        else:
            percentage = 100
        if(len(sys.argv) >= 5):
            start = int(sys.argv[4])
        else:
            start = 0

        bot = IgBot.IgBot()
        bot.open_browser()
        bot.log_in("username", "password")
        bot.follow_from_hashtag(hashtag, num_follows, percentage, start)

        print("Done!")
        bot.quit()

        

