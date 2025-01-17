from datetime import datetime

def add_follower(connection, cursor, flwer, flwee):
    if flwer == flwee:
        print("You can't follow yourself!")
        return 0
    cursor.execute("insert into follows values (?,?,?);", (flwer, flwee, datetime.today().strftime('%Y-%m-%d')))
    connection.commit()