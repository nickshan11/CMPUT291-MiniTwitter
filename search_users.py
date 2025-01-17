#Author: Anshul Verma

import sqlite3
from datetime import datetime

def return_users(connection, cur_usr_id):
    # Returns the search results and prints them in the desired output
    
    connection.row_factory = sqlite3.Row
    c = connection.cursor()
    keyword = input("Enter the name of the user you'd like to find: ")
    c.execute(f"SELECT usr,name FROM Users where name like '%{keyword}%';")
    # Fetching the user ids, name of the users with similar name as the keyword
    rows = c.fetchall()
    res1 = {}
    for row in rows:
        res1[row["usr"]] = row["name"]
    # sorting the created dictionary on the basis of the user name length
    res1_sorted = dict(sorted(res1.items(), key=lambda item: len(item[1])))    
    user_ids = list(res1_sorted.keys())
    user_names = list(res1_sorted.values())


    c.execute(f"SELECT usr,name,city FROM Users where city like '%{keyword}%';")
    # Fetching the user ids, name and city of the users with similar city as the keyword
    rows = c.fetchall()
    res2 = {}
    res3 = {}
    # Using parallel dictionaries for the user name and city with the user id as the common key.
    for row in rows:
        res2[row["usr"]] = row["city"]
        res3[row["usr"]] = row["name"]
    # sorting the created dictionary on the basis of the user city length
    res2_sorted = dict(sorted(res2.items(), key=lambda item: len(item[1])))
    temp = list(res2_sorted.keys())
    for i in range(len(temp)):
        # using the user id from the sorted dictionary as a key to get the corresponding name of the user
        try:
            # Ensures there are no duplicate user ids and names being appended
            test = res1_sorted[temp[i]]
        except KeyError:
            user_names.append(res3[temp[i]])        
            user_ids.append(temp[i])

    if len(user_names) == 0:
        print("Your search resulted in 0 matches, please try again with a different keyword.")
        return 0
    
    selection = None
    selection_valid = False
    check_selection = False
    list_len = len(user_names)
    index = 0
    while index < list_len:
        print(f"\n Option | User ID | Name")
        print(f"-------------------------------------")
        for i in range(index, index+5):
            if i < list_len:                
                print(f"{i+1:>6} | {user_ids[i]:^7} | {user_names[i]:^9}")
            else:
                break
        print(f"------------------------------------")
        
        choice = check_input_nav()
        if choice == 'n':
            input_valid = True
            if index+5 <= list_len-1:
                index += 5
            else:
                print("You've scrolled to the end!")
        elif choice == 'p':
            input_valid = True
            if index-5 >= 0:
                index -= 5
            else:
                print("You've scrolled to the start!")
        elif choice == 'e':
            input_valid = True
            return 0
        elif choice == 's':
            input_valid = True
            check_selection = True
            break
        else:
            print('Invalid Input')

                    
    if check_selection is True:
        while selection_valid is False:
            try:
                selection = int(input("\nPlease select an option: "))
                user_id = user_ids[selection-1]
                selection_valid = True
            except Exception:
                print(f"Please enter a valid number from 1 to {len(user_ids)}")

        selection_name = user_names[selection-1]
        print(f"\nYour selected user is {selection_name} and here are some stats about this user -\n")
        c.execute("select count(writer) from tweets where writer = :id;", {"id":user_id})
        tweet_count = c.fetchone()[0]
        c.execute("select count(flwee) from follows where flwee = :id;", {"id":user_id})
        flwers = c.fetchone()[0]
        c.execute("select count(flwer) from follows where flwer = :id;", {"id":user_id})
        flwing = c.fetchone()[0]
        print(f"Number of Tweets: {tweet_count}\n"
              f"Number of Followers: {flwers}\n"
              f"Number of users being followed: {flwing}\n")
        if (tweet_count != 0):
            print(f"\nHere are some recent tweets by {selection_name} -\n")
            c.execute("SELECT tid, text, tdate FROM tweets where writer = :id ORDER BY tdate DESC;", {"id":user_id})
            tweets = c.fetchall()
            j = 0
            k = 0
            tweets_len = len(tweets)
            print(f"\n Tweet No. | Tweet ID | Text")
            print(f"------------------------------------------------------------------------")
            while j < tweets_len and k < 3:
                print(f"{j+1:^9} | {tweets[j]['tid']:^9} | {tweets[j]['text']:^9}")
                j+=1
                k+=1
            print(f"------------------------------------------------------------------------")
        else:
            print(f"\nThere are no tweets by {selection_name} so far!\n")

        text = f"Do you wish to follow {selection_name} (y/n): "
        choice = check_input(text)
        if choice == 'y':
            input_valid = True
            try:
                if cur_usr_id != user_id:
                    # we get the current date in the required format using the datetime library
                    c.execute("insert into follows values (?,?,?);", (cur_usr_id, user_id, datetime.today().strftime('%Y-%m-%d')))                    
                    # committing the changes to the database
                    connection.commit()
                    print(f"You're now following {selection_name}!")
                else:
                    # we can follow ourself since it does not violate the primary key constraint
                    print("You can't follow yourself!")
            except sqlite3.IntegrityError:
                # handles the primary key constraint error, i.e. checks if the user is already following the selected user
                print(f"You are already following {selection_name}!")

        
        text = f"Do you wish to see more tweets by {selection_name} (y/n): "
        choice = check_input(text)
        if choice == 'y':
            if tweet_count > 3:
                index = 3
                while index < tweets_len:
                    print(f"\nTweet No. | Tweet ID | Text")
                    print(f"------------------------------------------------------------------------")
                    for i in range(index, index+5):
                        if i < tweets_len:            
                            print(f"{i+1:^9} | {tweets[i]['tid']:^8} | {tweets[i]['text']:^9}")
                        else:
                            break
                    print(f"------------------------------------------------------------------------")
                    
                    input_valid = False
                    while input_valid == False:
                        inp = input("Type 'N' for next 5 tweets, 'P' for previous 5 tweets, or 'E' to exit to the main menu: ")
                        if inp.lower() == 'n':
                            input_valid = True
                            if index+5 <= tweets_len-1:
                                index += 5
                            else:
                                print("You've scrolled to the end!")
                        elif inp.lower() == 'p':
                            input_valid = True
                            if index-5 >= 0:
                                index -= 5
                            else:
                                print("You've scrolled to the start!")
                        elif inp.lower() == 'e':
                            input_valid = True
                            return 0
                        else:
                            print('Invalid Input')
            else:
                print("There are no more tweets by this user!")


def check_input(text):
    # Loops to receive a valid user input
    input_valid = 0
    while input_valid == 0:
        inp = input(text)
        if inp.lower() == 'y':
            input_valid = 1

        elif inp.lower() == 'n':
            input_valid = 1
    return inp.lower()


def check_input_nav():
    # Loops to receive a valid user input to navigate the search results
    input_valid = 0
    while input_valid == 0:
        inp = input("Type 'N' for next 5 users, 'P' for previous 5 users, 'S' to stop viewing and make a selection or 'E' to exit to the main menu: ")
        if inp.lower() == 'n':
            input_valid = 1

        elif inp.lower() == 'p':
            input_valid = 1

        elif inp.lower() == 's':
            input_valid = 1
        
        elif inp.lower() == 'e':
            input_valid = 1
            
    return inp.lower()