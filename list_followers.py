#Author: Nick Shan
#Date: 2023-10-28

import sqlite3

# This function retrieves the names and IDs of the followers of a given user.
def get_followers(cur, current_user):
    cur.execute("""
        SELECT users.name, flwer 
        FROM follows 
        JOIN users ON follows.flwer = users.usr 
        WHERE follows.flwee = ?
    """, (current_user,))
    return cur.fetchall()

# This function retrieves the information of a given user from the users table.
def get_follower_info(cur, selected_follower):
    cur.execute("SELECT usr, name, email, city, timezone FROM users WHERE usr = ?", (selected_follower,))
    return cur.fetchone()

# This function counts the number of tweets written by a given user.
def get_tweet_count(cur, selected_follower):
    cur.execute("SELECT COUNT(*) FROM tweets WHERE writer = ?", (selected_follower,))
    return cur.fetchone()[0]

# This function counts the number of users a given user is following.
def get_following_count(cur, selected_follower):
    cur.execute("SELECT COUNT(*) FROM follows WHERE flwer = ?", (selected_follower,))
    return cur.fetchone()[0]

# This function counts the number of followers of a given user.
def get_follower_count(cur, selected_follower):
    cur.execute("SELECT COUNT(*) FROM follows WHERE flwee = ?", (selected_follower,))
    return cur.fetchone()[0]

# This function retrieves the three most recent tweets written by a given user.
def get_recent_tweets(cur, selected_follower):
    cur.execute("SELECT * FROM tweets WHERE writer = ? ORDER BY tdate DESC LIMIT 3", (selected_follower,))
    return cur.fetchall()

# This function inserts a new row into the follows table, indicating that a user has started following another user.
def follow_user(cur, current_user, selected_follower):
    cur.execute("INSERT INTO follows (flwer, flwee, start_date) VALUES (?, ?, date('now'))", (current_user, selected_follower))

# This function retrieves all tweets written by a given user, ordered by date in descending order.
def get_more_tweets(cur, selected_follower):
    cur.execute("SELECT * FROM tweets WHERE writer = ? ORDER BY tdate DESC", (selected_follower,))
    return cur.fetchall()

# This function displays information about the followers of a given user and allows the user to interact with them.
def lfmain(cur, conn, id):
    # Set the current user to the given ID
    current_user = id
    # Get the followers of the current user
    followers = get_followers(cur, current_user)
    # Print the list of followers
    while True:
        print("\nFollower(s):")
        for follower in followers:
            print(f"ID: {follower[1]}, Name: {follower[0]}")
        # Ask the user to select a follower or quit
        selected_follower = input("Enter a follower ID to see more information or 'q' to quit: ")
        if selected_follower.lower() == 'q':
            break

        # Check if the follower ID is valid
        follower_ids = [str(follower[1]) for follower in followers]
        if selected_follower not in follower_ids:
            print("Invalid follower ID. Please try again.")
            continue

        # Get and print the information of the selected follower
        info = get_follower_info(cur, selected_follower)
        print(f"\nUser: {info[0]} \nName: {info[1]} \nEmail: {info[2]} \nCity: {info[3]} \nTimezone: {info[4]}")
        
        # Get and print the number of tweets of the selected follower
        tweet_count = get_tweet_count(cur, selected_follower)
        print(f"Number of tweets: {tweet_count}")
        
        # Get and print the number of users the selected follower is following
        following_count = get_following_count(cur, selected_follower)
        print(f"Number of users being followed: {following_count}")
        
        # Get and print the number of followers of the selected follower
        follower_count = get_follower_count(cur, selected_follower)
        print(f"Number of followers: {follower_count}")
        
        # Get and print the most recent tweets of the selected follower
        recent_tweets = get_recent_tweets(cur, selected_follower)
        print("\nMost recent tweets:")
        print(f"\n Tweet ID | Writer |    Date    | Text ")
        print(f"-------------------------------------------------------------------")
        for tweets in recent_tweets:
            print(f" {tweets[0]:^8} | {tweets[1]:^6} | {tweets[2]:^6} | {tweets[3]:^9}")
        print(f"-------------------------------------------------------------------")
            
        # Ask the user to follow the selected follower, see more tweets, or quit
        action = input("\nEnter 'f' to follow this user or 'm' to see more tweets or 'q' to quit: ")
        if action.lower() == 'f':
            follow_user(cur, current_user, selected_follower)
            conn.commit()
            print(f"You are now following {selected_follower}")
        elif action.lower() == 'm':
            more_tweets = get_more_tweets(cur, selected_follower)
            tweet_index = 0
            while True:
                print("\nMore tweets:")
                print(f"\n Tweet ID | Writer |    Date    | Text ")
                print(f"-------------------------------------------------------------------")
                for i in range(tweet_index, tweet_index + 5):
                    if i < len(more_tweets):
                        print(f" {more_tweets[i][0]:^8} | {more_tweets[i][1]:^6} | {more_tweets[i][2]:^6} | {more_tweets[i][3]:^9}")
                print(f"-------------------------------------------------------------------")
                
                command = input("Enter 'next' to view the next 5 tweets, 'prev' to view the previous 5 tweets, or 'q' to quit: ").lower()
                if command == 'next':
                    tweet_index += 5
                elif command == 'prev':
                    tweet_index = max(0, tweet_index - 5)
                elif command == 'q':
                    break
   
        elif action.lower() == 'q':
            break
