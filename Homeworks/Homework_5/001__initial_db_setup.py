import sqlite3
import argparse as arg


def create_database(unique=False):
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()

    # CREATING BANK TABLE
    cursor.execute('''CREATE TABLE IF NOT EXISTS Bank (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL UNIQUE
                    )''')

    # CREATING TRANSACTION TABLE
    cursor.execute('''CREATE TABLE IF NOT EXISTS Transactions (
                    id INTEGER PRIMARY KEY,
                    Bank_sender_name TEXT NOT NULL,
                    Account_sender_id INTEGER NOT NULL,
                    Bank_receiver_name TEXT NOT NULL,
                    Account_receiver_id INTEGER NOT NULL,
                    Sent_Currency TEXT NOT NULL,
                    Sent_Amount REAL NOT NULL,
                    Datetime TEXT
                    )''')

    # CREATING USER TABLE
    unique_values = 'UNIQUE' if unique else ''
    cursor.execute(f'''CREATE TABLE IF NOT EXISTS User (
                    Id INTEGER PRIMARY KEY,
                    Name TEXT NOT NULL {unique_values},
                    Surname TEXT NOT NULL {unique_values},
                    Birth_day TEXT,
                    Accounts TEXT NOT NULL
                    )''')

    # CREATING ACCOUNT TABLE
    cursor.execute('''CREATE TABLE IF NOT EXISTS Account (
                    Id INTEGER PRIMARY KEY,
                    User_id INTEGER NOT NULL,
                    Type TEXT NOT NULL,
                    Account_Number INTEGER NOT NULL UNIQUE,
                    Bank_id INTEGER NOT NULL,
                    Currency TEXT NOT NULL,
                    Amount REAL NOT NULL,
                    Status TEXT
                    )''')

    conn.commit()
    conn.close()


parser = arg.ArgumentParser()
parser.add_argument('--unique', action='store_true')
args = parser.parse_args()
create_database(args.unique)
