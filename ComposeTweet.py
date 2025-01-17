#Author: Peter Davidson
#Date: 2023-10-31

import sqlite3

def compose_tweet(cur, tid, usr, text):
    """
    Compose a tweet and add it to the database.
    """
    cur.execute("INSERT INTO tweets (tid,writer,tdate,text,replyto) VALUES (?, ?, date('now'), ?, NULL);", (tid, usr, text))

def mention(cur, tid, temp):
    """
    Add a mention to the database.
    """
    cur.execute('INSERT INTO mentions (tid,term) VALUES (?, ?);', (tid, temp))

def hash(cur, temp):
    """
    Add a hashtag to the database.
    """
    cur.execute('INSERT INTO hashtags (term) VALUES (?);', (temp,))

def get_hashtags(cur):
    """
    Get all hashtags from the database.
    """
    cur.execute('SELECT DISTINCT (term) FROM hashtags;')
    return cur.fetchall()

def get_tid(cur):
    """
    Get the highest tid from the database.
    """
    cur.execute('SELECT MAX(tid) FROM tweets;')
    return cur.fetchone()[0] # make a unique tid

def delete_mentions(cur, tid, word):
    """
    Delete a mentioned term from the database.
    """
    cur.execute('DELETE FROM mentions WHERE tid = ? AND term = ?;', (tid, word))
def delete_tweet(cur, tid):
    """
    Delete a tweet from the database.
    """
    cur.execute('DELETE FROM tweets WHERE tid = ?;', (tid,))

def get_mentions(cur, tid, temp):
    """
    Get all mentions from the database.
    """
    cur.execute('SELECT tid, term FROM mentions WHERE tid = ? AND term = ?;', (tid, temp))
    return cur.fetchall()

def get_existing_mentions(cur, tid, word):
    """
    Get all existing mentions from the database but of other tids.
    """
    cur.execute('SELECT tid FROM mentions WHERE tid != ? AND term = ?;', (tid, word))
    return cur.fetchall()

def delete_hashtags(cur, word):
    """
    Delete a hashtag from the database.
    """
    cur.execute('DELETE FROM hashtags WHERE term = ?;', (word,))

def ctmain(cur,conn, usr):
    Looping = True
    while Looping == True:
        text = input("Compose your tweet: ")
        res = text.replace('#', ' #') #handles text#A#B to be text #A #B
        res = res.split()
        tid = get_tid(cur)
        if tid == None: #in case tweets is empty
            tid = 1
        elif tid != None:
            tid = tid + 1
        if len(res) == 0: #handles if only [whitespace] or [whitespaces]
            compose_tweet(cur, tid, usr, text)
            conn.commit()
        else:
            compose_tweet(cur, tid, usr, text)
            conn.commit()
            for word in res:
                if word[0] == "#":
                    temp = word.replace('#', '', 1) #replaces #A to be A
                    result = get_hashtags(cur)
                    duplicates = False
                    for documented_term in result: #gets all documented_terms that exist already in the hashtags table
                        for x in documented_term: #traverse through and make it all lower case so case insensitive
                            test = x.lower() 
                        if(test == temp.lower()): #checks if there are duplicates then no need to add to hashtags
                            duplicates = True
                            break
                    if (duplicates == False): #if there isn't then add
                        hash(cur, temp.lower())
                        conn.commit()
                    mentions_duplicate = get_mentions(cur, tid, temp.lower()) #handles text #A #A to be just text #a
                    if len(mentions_duplicate) == 0:
                        mention(cur, tid, temp.lower()) #adds the first #A and ignores the second one
                        conn.commit()

        action = input("Enter 's' to save and tweet, anything else to quit and discard\n")
        
        if action.lower() == 's':
            print("saved")
            while (True):
                another_one = input("Do you want to compose another tweet? Type y for yes or n for no\n")
                if (another_one.lower()) == "n":
                    Looping = False
                    break
                elif (another_one.lower() == 'y'):
                    break

        else: #if they discard then delete all progress and check if someone already used that hashtag, if not then delete it as well
            for word in res:
                if word[0] == "#":
                    word = word.replace('#', '', 1)
                    delete_mentions(cur, tid, word.lower())
                    conn.commit()
                    existing_mentions = get_existing_mentions(cur, tid, word.lower())
                    if len(existing_mentions) == 0:
                        delete_hashtags(cur, word.lower())
                        conn.commit()
            delete_tweet(cur, tid)
            conn.commit()
            print("exited")
            Looping = False
            break

    conn.commit()

if __name__ == "__main__":
    ctmain()
