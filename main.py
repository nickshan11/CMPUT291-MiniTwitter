#Author: Daniel Cui
#Date: 2023-10-24
#Version: 1.0.0

import login  # Importing the login.py file
import feed as fd # Importing the feed.py file
import search_users # Importing the search_users.py file
import list_followers as lf # Importing the list_followers.py file
import ComposeTweet as ct # Importing the ComposeTweet.py file
import search_tweets as st
import sqlite3
import os

EXIT = 'E'

REGISTERED = '1'
UNREGISTERED = '2'

TWEET_SEARCH = 'Z'
USER_SEARCH = 'X'
WRITE_TWEET = 'C'
LIST_FOLLOWERS = 'V'
LOGOUT = 'Q'

PREVIOUS = 'A'
NEXT = 'D'
INTERACT = 'S'
EXIT_FEED = 'F'
FEED_OPTIONS = [PREVIOUS, NEXT, INTERACT, EXIT_FEED]

DISPLAY_FEED = 'DISPLAY_FEED'

cur = None
conn = None

def options():
    '''
    This function prints the options for the user and returns the user's choice
    '''
    print("\n Z - Tweet Search | X - User Search | C - Write Tweet | V - List Followers | Q - Logout")
    userInput = input("Please type your choice: ").upper()
    return userInput

def main():
    '''
    This function is the main function of the program. It connects to the database and initializes the user.
    '''
    # Connecting to the database
    registeredUser = False 
    validPath = False

    # Connecting to the database
    while not validPath: 
        path = input("Please enter the path of the database: ")
        try:
            # Connecting to the database
            if os.path.exists(path) == False: # Checking if the path exists
                print("Invalid path")
                continue
            conn = sqlite3.connect(path)
            cur = conn.cursor()
            cur.execute(' PRAGMA foreign_keys=ON; ')
            conn.commit()
            validPath = True
        except:
            print("Invalid path")

    # Initializing the user
    current = None
    user = None
    usr, name, email, city, timezone = None, None, None, None, None

    while current != EXIT:

        # Logging menu
        current = login.options() #which state the user is in (i.e. if current = LOGIN, then the user is in the login state)
        while current != LOGOUT and current != EXIT:
            if current == REGISTERED:
                usr = login.registered(cur) #usr is the username of the user
                registeredUser = True
            elif current == UNREGISTERED:
                usr = login.unregistered(cur, conn) #usr is the username of the user
                registeredUser = False
            elif current == LOGOUT:
                break 
            else:
                print("Invalid input")
                current = login.options()

            #The user is returning back to the login menu
            if usr == '':
                current = login.options()
            else: #The user has successfully logged in
                if current != LOGOUT and current != EXIT:

                    # Getting the user's information
                    user = login.getUsr(cur, usr)
                    usr, name, email, city, timezone = user[0], user[2], user[3], user[4], user[5]
                    print("\nWelcome to Mini-Twitter, ", name, "!")
                break
        
        # Feed menu
        if registeredUser:

            # Initializing the feed
            feed = fd.getFeed(cur, usr)
            feedPage = 0
            if current != LOGOUT and current != EXIT:
                current = DISPLAY_FEED

            while current != LOGOUT and current != EXIT and current != EXIT_FEED:
                if current == DISPLAY_FEED:
                    current, feedPage = fd.displayFeed(feed, feedPage)
                elif current == INTERACT:
                    current = fd.interactFeed(cur, conn, usr, feed, feedPage)
                    
        # Main menu
        while current != LOGOUT and current != EXIT:
            current = options()
            #if the user wants to search for tweets
            if current == TWEET_SEARCH:
                keywords = list(input("Type keywords to search for: ").split())
                # Call the search_tweets function to get the tweets that match the keywords
                tweets = st.search_tweets(cur, keywords)
                
                index = 0
                
                while True:
                    print(f"\n Tweet ID | Writer |    Date    | Text")
                    print(f"-------------------------------------------------------------------")
                    # Print the next 5 tweets starting from the current index
                    for i in range(index, index + 5):
                        if i < len(tweets):
                            print(f" {tweets[i][0]:^8} | {tweets[i][1]:^6} | {tweets[i][2]:^6} | {tweets[i][3]:^9}")
                    print(f"-------------------------------------------------------------------")
                        
                    # Ask the user for the next action
                    command = input("Please enter 'next' to view the following 5 tweets, 'prev' to go back to the previous 5 tweets, 'more' to access tweet statistics or to reply or retweet, or 'exit' to end the session: ").lower()
                    # If the user wants to see the next 5 tweets, increase the index by 5
                    if command == 'next':
                        index += 5
                    # If the user wants to see the previous 5 tweets, decrease the index by 5 (but not below 0)
                    elif command == 'prev':
                        index = max(0, index - 5)
                    # If the user wants to see more details about a tweet
                    elif command == 'more':
                        tid = input("Please input the ID of the tweet you would like to select or 'q' to go back: ")
                        # Start a loop for the tweet details
                        while tid != 'q':
                            option = input("Type 'stat' to see statistics, 'reply' to reply, 'retweet' to retweet or 'q' to go back: ")
                            if option == 'stat':
                                stats = st.get_tweet_stats(cur, tid)
                                print(f"Retweets: {stats['retweets']}, Replies: {stats['replies']}")
                            elif option == 'reply':
                                st.compose_reply(cur, conn, usr, tid)
                            elif option == 'retweet':
                                print("Successfully retweeted!")
                                st.retweet(cur, usr, tid)
                            # If the user wants to go back, break the inner loop
                            elif option == 'q':
                                break
                    # If the user wants to exit, break the outer loop
                    elif command == 'exit':
                        break

            elif current == WRITE_TWEET:
                ct.ctmain(cur, conn, user[0])
            elif current == USER_SEARCH:
                search_users.return_users(conn, usr)
            elif current == LIST_FOLLOWERS:
                lf.lfmain(cur,conn,user[0])
            elif current == LOGOUT:
                break
            else:
                print("Invalid input")

        if current == LOGOUT:
            print("\n You Have Logged Out.")
        

    print("\nThank you for using Mini-Twitter!")
    print("You have exited the program")
    
    # Closing the connection
    conn.commit()
    conn.close()
    

if __name__ == "__main__":
    main()  