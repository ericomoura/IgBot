import sys

import _configs
import _words
import IgBot
   
def print_help():
    print("")
    print("Correct usage: " + sys.argv[0] + " target num_posts percentage start comments_to_leave")
    print("  target: User whose posts are going to be commented.")
    print("  num_posts: Number of posts to be commented in total.")
    print("  percentage: (optional) Chance for each post to be commented. Skipped posts do not count towards the total amount. Defaults to 100% (every post).")
    print("  start: (optional) Post to start with. Defaults to 0 (first post).")
    print("  comments_to_leave: (optional) Number of comments to leave on the post. Defaults to 0.")
    print("Use '" + sys.argv[0] + " help' to display this message again.")

if __name__ == "__main__":
    if (sys.argv[1] == "help") or len(sys.argv) < 3 or len(sys.argv) > 6:
        print_help()
    else:
        #Grabs parameters from command line
        target = sys.argv[1]
        num_posts = int(sys.argv[2])
        if (len(sys.argv) >= 4):
            percentage = int(sys.argv[3])
        else:
            percentage = 100
        if (len(sys.argv) >= 5):
            start = int(sys.argv[4])
        else:
            start = 0
        if (len(sys.argv) >= 6):
            comments_to_leave = int(sys.argv[5])
        else:
            comments_to_leave = 0

        bot = IgBot.IgBot()
        bot.open_browser()
        bot.log_in("username", "password")
        bot.delete_comments(target, num_posts, percentage, start, comments_to_leave)