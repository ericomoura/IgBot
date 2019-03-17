import sys

import _configs
import _words
import IgBot
   
def print_help():
    print("")
    print("Correct usage: " + sys.argv[0] + " mode targets post num_comments percentage pages")
    print("  mode: 'like' or 'unlike'. 'like' will like the targets' comments. 'unlike' will unlike the targets' comments.")
    print("  targets: List of users whose comments are going to be like/unliked. Comma separated (e.g. user1,user2,user3,user4).")
    print("  post: Post to like/unlike comments from.")
    print("  num_comments: Number of comments to be like/unliked in total.")
    print("  percentage: (optional) Chance for each comment to be liked/unliked. Skipped comment do not count towards the total amount. Defaults to 100% (every post).")
    print("  pages: (optional) Number of comment pages to search. Defaults to 1 (first page).")
    print("Use '" + sys.argv[0] + " help' to display this message again.")

if __name__ == "__main__":
    if (sys.argv[1] == "help") or len(sys.argv) < 5 or len(sys.argv) > 7:
        print_help()
    else:
        #Grabs parameters from command line
        targets = sys.argv[2].split(',')
        post = sys.argv[3]
        num_comments = int(sys.argv[4])
        if (len(sys.argv) >= 6):
            percentage = int(sys.argv[5])
        else:
            percentage = 100
        if (len(sys.argv) >= 7):
            pages = int(sys.argv[6])
        else:
            pages = 1

        if (sys.argv[1] == "like"):
            bot = IgBot.IgBot()
            bot.open_browser()
            bot.log_in("username", "password")
            bot.like_comments(targets, post, num_comments, percentage, pages)
        elif (sys.argv[1] == "unlike"):
            bot = IgBot.IgBot()
            bot.open_browser()
            bot.log_in("username", "password")
            bot.unlike_comments(targets, post, num_comments, percentage, pages)
        else:  #Invalid mode
            print_help()