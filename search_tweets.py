#Author: Nick Shan & Peter Davidson
#Date: 2023-11-04

import sqlite3
import ComposeTweet as ct # Importing the ComposeTweet.py file

#inserts a new tweet into the tweets table with the given tid, usr, text, and replyto values.
def compose_tweet(cur, tid, usr, text, replyto):
    cur.execute("INSERT INTO tweets (tid,writer,tdate,text,replyto) VALUES (?, ?, date('now'), ?, ?);", (tid, usr, text, replyto))
    cur.connection.commit()

#inserts a new mention into the mentions table with the given tid and term values.
def mention(cur, tid, temp):
    cur.execute('INSERT INTO mentions (tid,term) VALUES (?, ?);', (tid, temp))
    cur.connection.commit()

#inserts a new hashtag into the hashtags table with the given term value.
def hash(cur, temp):
    cur.execute('INSERT INTO hashtags (term) VALUES (?);', (temp,))

#returns a list of all distinct hashtags from the hashtags table.
def get_hashtags(cur):
    cur.execute('SELECT DISTINCT (term) FROM hashtags;')
    return cur.fetchall()

#returns the maximum tid value from the tweets table, or None if the table is empty.
def get_tid(cur):
    cur.execute('SELECT MAX(tid) FROM tweets;')
    return cur.fetchone()[0] # make a unique tid

#deletes a mention from the mentions table, given the tid and term values.
def delete_mentions(cur, tid, word):
    cur.execute('DELETE FROM mentions WHERE tid = ? AND term = ?;', (tid, word))

#deletes a tweet and its associated mention from the tweets and mentions tables, given the tid and term values.
def delete_tweet(cur, tid, word):
    cur.execute('DELETE FROM mentions WHERE tid = ? AND term = ?;', (tid, word))
    cur.execute('DELETE FROM tweets WHERE tid = ?;', (tid,))

#returns a list of tuples containing the tid and term values from the mentions table, given the tid and term values.
def get_mentions(cur, tid, temp):
    cur.execute('SELECT tid, term FROM mentions WHERE tid = ? AND term = ?;', (tid, temp))
    return cur.fetchall()

#returns a list of tuples containing the tid values from the mentions table, given the tid and term values.
def get_mentions_others(cur, tid, word):
    cur.execute('SELECT tid FROM mentions WHERE tid != ? AND term = ?;', (tid, word))
    return cur.fetchall()

#deletes a hashtag from the hashtags table, given the term value.
def delete_hashtags(cur, word):
    cur.execute('DELETE FROM hashtags WHERE term = ?;', (word,))

#allows the user to compose a reply to a tweet
#also checks if the reply contains any hashtags, 
#and inserts them into the hashtags and mentions tables if they are not already present.
#also prompts the user to save or discard the reply, and to compose another tweet if desired.
def compose_reply(cur, conn, usr, replyto):
    Looping = True
    while Looping == True:
        text = input("Compose your reply: ")
        res = text.replace('#', ' #')
        res = res.split()
        tid = get_tid(cur)
        tid = 1 if tid is None else tid + 1
        if len(res) == 0:
            compose_tweet(cur, tid, usr, text, replyto)
            conn.commit()
        else:
            compose_tweet(cur, tid, usr, text, replyto)
            conn.commit()
            for word in res:
                if word[0] == "#":
                    temp = word.replace('#', '', 1)
                    result = get_hashtags(cur)
                    duplicates = False
                    for documented_term in result:
                        for x in documented_term:
                            test = x.lower() 
                        if(test == temp.lower()):
                            duplicates = True
                            break
                    if (duplicates == False):
                        hash(cur, temp.lower())
                        conn.commit()
                    mentions_duplicate = get_mentions(cur, tid, temp.lower())
                    if len(mentions_duplicate) == 0:
                        mention(cur, tid, temp.lower())
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
                    existing_mentions = get_mentions_others(cur, tid, word.lower())
                    if len(existing_mentions) == 0:
                        delete_hashtags(cur, word.lower())
                        conn.commit()
            delete_tweet(cur, tid)
            conn.commit()
            print("exited")
            Looping = False
            break

    conn.commit()

#connects to the database, used for debugging
def connect_to_db(db_file):
    conn = sqlite3.connect(db_file)
    return conn.cursor()

#searches for tweets that contain any of the given keywords, either in the text or as a hashtag.
#the function returns a list of tuples containing the tid, writer, tdate, and text of the matching tweets, ordered by date in descending order.
def search_tweets(cur, keywords):
    tweets = []
    for keyword in keywords:
        query = """
        SELECT DISTINCT tweets.tid, tweets.writer, tweets.tdate, tweets.text
        FROM tweets
        LEFT JOIN mentions ON tweets.tid = mentions.tid
        WHERE tweets.text LIKE ?
        OR mentions.term = ?
        ORDER BY tweets.tdate DESC;
        """
        cur.execute(query, ('%' + keyword + '%', keyword))
        tweets.extend(cur.fetchall())
    return tweets

#retrives statistics about a tweet, given the tid value.
def get_tweet_stats(cur, tid):
    query = "SELECT COUNT(*) FROM retweets WHERE tid = ?"
    cur.execute(query, (tid,))
    retweets = cur.fetchone()[0]

    query = "SELECT COUNT(*) FROM tweets WHERE replyto = ?"
    cur.execute(query, (tid,))
    replies = cur.fetchone()[0]

    return {'retweets': retweets, 'replies': replies}

#retweets a tweet, given the tid and usr values.
def retweet(cur, usr, tid):
    query = "INSERT INTO retweets(usr, tid, rdate) VALUES (?, ?, date('now'))"
    cur.execute(query, (usr, tid))
    cur.connection.commit()

# used for debugging
if __name__ == "__main__":
    cur = connect_to_db('/Users/nshan/Documents/CMPUT-291/f23-proj1-somequerylearners/mp1.db')
    conn = sqlite3.connect('/Users/nshan/Documents/CMPUT-291/f23-proj1-somequerylearners/mp1.db')
    tweets = search_tweets(cur, ['oilers'])
    for tweet in tweets:
        print(tweet)
        stats = get_tweet_stats(cur, tweet[0])
        print(stats)
        compose_reply(cur,conn, 12, tweet[0])
        break
        #retweet(cur, 12, tweet[0])
