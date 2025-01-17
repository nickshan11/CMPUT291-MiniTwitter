#Author: Daniel Cui
#Date: 2023-10-24
#Version: 1.0.0

import sqlite3
import hashlib
import getpass

HASH = False

EXIT = 'E'
REGISTERED = '1'
UNREGISTERED = '2'

def options():
    """
    This function prints the options for the user to choose from
    """
    print("\n 1 - Existing Users | 2 - New Users | E - Exit")
    while True:
        userInput = input("\nPlease type your choice: ").upper()
        if userInput == REGISTERED:
            return REGISTERED
        elif userInput == UNREGISTERED:
            return UNREGISTERED
        elif userInput == EXIT:
            return EXIT
        else:
            print("\nInvalid input\n")

def registered(cur):
    """
    This function prompts the user for their user id and password and checks if it is valid
    """
    valid = False
    while not valid:
        usr = input("\nPlease enter your user id or Press enter to go back: ")

        # If the user presses enter, go back to the previous menu
        if usr == '':
            return ''
        
        pwd = getpass.getpass("Please enter your password: ") # getpass hides the password as the user types it
        
        if tryLogin(cur, usr, pwd) == None:
            print("\nInvalid username or password")
        else:
            valid = True
    return usr


def unregistered(cur, conn):
    """
    This function prompts the user for their information and creates a new user
    """
    name = input("\nPlease enter your name or Press enter to go back: ")

    # If the user presses enter, go back to the previous menu
    if name == '':
        return ''
    
    pwd = getpass.getpass("Please enter your password: ")
    email = input("Please enter your email: ")
    city = input("Please enter your city: ")
    timezone = input("Please enter your timezone: ")

    usr = createUsr(cur, conn, pwd, name, email, city, timezone)
    
    print("\nYour user id is: ", usr)
    print("Please remember your user id, as you will need it to login")

    return usr


def hash_password(password):
    """
    This function hashes the password using SHA256
    """
    alg = hashlib.sha256()
    alg.update(password.encode('utf-8'))
    return alg.hexdigest()

def createUsr(cur, conn, pwd, name, email, city, timezone):   
    """
    This function creates a new user and returns the user id
    """
    cur.execute('SELECT MAX(usr) FROM users;')
    usr = cur.fetchone()[0] + 1
    if (HASH == True):
        pwdH = hash_password(pwd)
    cur.execute('INSERT INTO users VALUES (?, ?, ?, ?, ?, ?);', (usr, pwd, name, email, city, timezone,))
    conn.commit()
    return usr


def tryLogin(cur, usr, pwd):
    """
    This function checks if the user id and password is valid
    """
    if (HASH == True):
        pwd = hash_password(pwd)
    cur.execute('SELECT * FROM users WHERE usr = ? AND pwd = ?;', (usr, pwd,))
    return cur.fetchone()


def getUsr(cur, usr):
    """
    This function returns the user information
    """
    cur.execute("SELECT * FROM users WHERE usr = ?", (usr,))
    user = cur.fetchone()
    return user

def main():
    path = input("Please enter the path of the database: ")
    conn = sqlite3.connect(path)
    cur = conn.cursor()

    print("Welcome to Mini-Twitter!")

    current = options()
    while current != EXIT:
        if current == REGISTERED:
            usr = registered(cur)
            break
        elif current == UNREGISTERED:
            current = unregistered(cur)
            break
        else:
            print("Invalid input")
            current = options()

    #get all the details about the user except for the password
    cur.execute("SELECT * FROM users WHERE usr = ?", (usr,))
    user = cur.fetchone()
    print(f"\nUser ID: {user[0]}, Name: {user[2]}, Email: {user[3]}, City: {user[4]}, Timezone: {user[5]}")

    conn.commit()
    conn.close()

    print("\nThank you for using Mini-Twitter!")
if __name__ == "__main__":
    main()