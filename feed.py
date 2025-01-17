#Author: Daniel Cui
#Date: 2023-10-24
#Version: 1.0.0

import sqlite3
import search_tweets as st

PREVIOUS = 'A'
NEXT = 'D'
INTERACT = 'S'
EXIT_FEED = 'F'
FEED_OPTIONS = [PREVIOUS, NEXT, INTERACT, EXIT_FEED]

MORE_INFO = 'Y'
REPLY = 'R'
RETWEET = 'T'
BACK = 'B'

def getFeed(cur, usr):
    """
    This function returns the feed of the user
    """
    query = """
                WITH Following AS(
                SELECT DISTINCT flwee
                FROM Follows
                WHERE flwer == ?
                )
                , FollowingTweets AS(
                SELECT tid, writer, tdate, text
                FROM Tweets
                WHERE writer in Following
                )
                , FollowingRetweets AS(
                SELECT t.tid, t.writer, r.rdate as tdate, t.text
                FROM Tweets t, Retweets r
                WHERE r.usr in Following
                AND t.tid = r.tid
                )
                , Feed AS (
                SELECT DISTINCT *
                FROM FollowingTweets
                UNION
                SELECT DISTINCT *
                FROM FollowingRetweets
                )
                SELECT
                    ROW_NUMBER() OVER (ORDER BY f.tdate DESC) AS tweet_number, 
                    f.tid,
                    f.writer,
                    COALESCE(r.usr, 'None') as retweeter,
                    f.tdate, 
                    f.text
                FROM Feed f
                LEFT JOIN Retweets r ON r.tid = f.tid AND r.usr IN Following;
            """
    cur.execute(query, (usr,))
    return cur.fetchall()

def showFeed(feed, page):
    """
    This function shows the feed of the user
    """
    print(f"\n Tweet Number | Tweet ID | Writer | Retweeter |    Date    | Text")
    print(f"-------------------------------------------------------------------")
    for i in range(page, page + 5):
        if i < len(feed): #if the tweet exists
            print(f" {feed[i][0]:^12} | {feed[i][1]:^8} | {feed[i][2]:^6} | {feed[i][3]:^9} | {feed[i][4]:^10} | {feed[i][5]}")
    print(f"-------------------------------------------------------------------")


def feedOptions(feedPage, lenFeed):
    """
    This function shows the feed options
    """
    if feedPage < lenFeed - 5 and feedPage >= 5: #if there are more than 5 tweets left
        msg = "       A - Previous | D - Next | S - Interact | F - Exit Feed"
    elif feedPage >= lenFeed - 5 and feedPage >= 5: #if there are less than 5 tweets left
        msg = "       A - Previous | S - Interact | F - Exit Feed"
    elif feedPage < lenFeed - 5 and feedPage == 0: #if there are more than 5 tweets left
        msg = "       D - Next | S - Interact | F - Exit Feed"
    else: #if there are less than 5 tweets left
        msg = "       S - Interact | F - Exit Feed"
    print(f"{msg:^61}")

def validFeedInput(userInput, feedPage, lenFeed):
    """
    This function checks if the user input is valid
    """
    if feedPage < lenFeed - 5 and feedPage >= 5: #if there are more than 5 tweets left
        if userInput not in FEED_OPTIONS: return False
        else: return True
    elif feedPage >= lenFeed - 5 and feedPage >= 5: #if there are less than 5 tweets left
        if userInput != PREVIOUS and userInput != INTERACT and userInput != EXIT_FEED: return False
        else: return True
    elif feedPage < lenFeed - 5 and feedPage == 0: #if there are more than 5 tweets left
        if userInput != NEXT and userInput != INTERACT and userInput != EXIT_FEED: return False
        else: return True
    else: #if there are less than 5 tweets left
        if userInput != INTERACT and userInput != EXIT_FEED: return False
        else: return True

def displayFeed(feed, feedPage):
    """
    This function displays the feed
    """
    lenFeed = len(feed)
    while True:

        # Displaying the feed
        showFeed(feed, feedPage)
        valid = False
        while not valid:

            # Displaying the feed options
            feedOptions(feedPage, lenFeed)
            userInput = input("Please type your choice: ").upper()
            valid = validFeedInput(userInput, feedPage, lenFeed)
            if not valid: print("Invalid input")

        # Checking the user input
        if userInput == PREVIOUS:
            feedPage -= 5
        elif userInput == NEXT:
            feedPage += 5
        elif userInput == INTERACT:
            return 'S', feedPage
        elif userInput == EXIT_FEED:
            return 'F', feedPage
                
def interactFeed(cur, conn, usr, feed, feedPage):
    """
    This function allows the user to interact with the feed
    """
    # Getting the list of tweet ids that the user can interact with on this page
    tweets = []
    for i in range(feedPage, feedPage + 5):
        if i < len(feed): #if the tweet exists
            tweets.append(str(feed[i][1]))
    print("If you would like to see more information about a tweet, or reply, or retweet, please type the tweet id.")
    print("If you would like to go back to the feed, please type 'B'.")
    print("If you would like to exit feed menu, please type F.")

    # Getting the user input
    valid = False
    while not valid:
        userInput = input("\nPlease type your choice: ").upper()
        if userInput == 'B':
            return 'DISPLAY_FEED'
        elif userInput in tweets:
            tweetOptions(cur, conn, userInput, usr)
            return 'DISPLAY_FEED'
        elif userInput == 'F':
            return 'F'
        else:
            print("Invalid input")

def tweetOptions(cur, conn, tid, usr):
    """
    This function displays the options for the user to choose from
    """
    while True:

        # Displaying the options
        print(f"\nY - More Info | R - Reply | T - Retweet | B - Back")
        userInput = input("\nPlease type your choice: ").upper()
        if userInput == MORE_INFO:
            st.get_tweet_stats(cur, tid)
            print("\nRetweets: ", st.get_tweet_stats(cur, tid)['retweets'])
            print("Replies: ", st.get_tweet_stats(cur, tid)['replies'], "\n")
        elif userInput == REPLY:
            st.compose_reply(cur, conn, usr, tid)
            print("Reply sent!")
        elif userInput == RETWEET:
            st.retweet(cur, usr, tid)
            print("Retweet sent!")
        elif userInput == BACK:
            return
        else:
            print("Invalid input")

            
def main():
    # Connecting to the database
    validPath = False
    while not validPath: 
        path = 'mp1.db'
        # path = input("Please enter the path of the database: ")
        try:
            conn = sqlite3.connect(path)
            cur = conn.cursor()
            cur.execute(' PRAGMA foreign_keys=ON; ')
            conn.commit()
            validPath = True
        except:
            print("Invalid path")

    # usr = input("Please enter your user id: ")
    usr = 97
    feed = getFeed(cur, usr)

    lenFeed = len(feed)
    feedPage = 0
    displayFeed = True
    MODE = 'F'
    while displayFeed and MODE == 'F':
        showFeed(feed, feedPage)
        valid = False
        while not valid:
            feedOptions(feedPage, lenFeed)
            userInput = input("Please type your choice: ").upper()
            valid = validFeedInput(userInput, feedPage, lenFeed)
            if not valid: print("Invalid input")

        if userInput == PREVIOUS:
            feedPage -= 5
        elif userInput == NEXT:
            feedPage += 5
        elif userInput == INTERACT:
            MODE = 'I'
        elif userInput == EXIT_FEED:
            displayFeed = False
            

    conn.commit()
    conn.close()

if __name__ == "__main__":
    main()