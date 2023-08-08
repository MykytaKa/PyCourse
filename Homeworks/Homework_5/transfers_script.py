import sqlite3
import csv
import freecurrencyapi
from datetime import datetime, timezone
from validations import validate_bank_data, validate_user_data, validate_account_data
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def establish_db_connection(func):
    """
    A decorator that establishes a connection to the SQLite database, executes the wrapped function,
    and then commits and closes the connection.

    :param func: (function) The function to be wrapped.
    :return function: The wrapper function.
    """
    def wrapper(*args):
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()

        if isinstance(args[0], list):
            result = func(cursor, args[0])
        else:
            result = func(cursor, args)

        conn.commit()
        conn.close()
        return result

    return wrapper


@establish_db_connection
def add_bank(cursor, bank_data):
    """
    Add banks to the database.

    :param cursor: (sqlite3.Cursor) The cursor to interact with the database.
    :param bank_data: (list) A list of bank names to be added.
    :return str: The status of the operation.
    """
    for bank in bank_data:
        validate_bank_data(bank)
        cursor.execute(f'INSERT INTO Bank (name) VALUES ("{bank}")')
    logger.info("Banks added successfully.")
    return 'The operation was successful.'


@establish_db_connection
def add_user(cursor, user_data):
    """
    Add users to the database.

    :param cursor: (sqlite3.Cursor) The cursor to interact with the database.
    :param user_data: (list) A list of user data, where each element is a list containing user information.
                            The format of user_data: [[full_name, birth_day, accounts], ...]
    :return str: The status of the operation.
    """
    for user in user_data:
        name, surname = user[0].split()
        validate_user_data((name, surname, *user[1:]))
        cursor.execute('INSERT INTO User (Name, Surname, Birth_day, Accounts) VALUES (?, ?, ?, ?)',
                       (name, surname, *user[1:]))
    logger.info("Users added successfully.")
    return 'The operation was successful.'


@establish_db_connection
def add_account(cursor, account_data):
    """
    Add accounts to the database.

    :param cursor: (sqlite3.Cursor) The cursor to interact with the database.
    :param account_data: (list) A list of account data, where each element is a list containing account information.
                               The format of account_data: [[User_id, Type, Account_Number,
                                                            Bank_id, Currency, Amount, Status], ...]
    :return str: The status of the operation.
    """
    for account in account_data:
        validate_account_data(account)
        cursor.execute('INSERT INTO Account (User_id, Type, Account_Number, Bank_id, Currency, Amount, Status)'
                       'VALUES (?, ?, ?, ?, ?, ?, ?)', account)
    logger.info("Accounts added successfully.")
    return 'The operation was successful.'


@establish_db_connection
def add_bank_from_csv(cursor, path):
    """
    Add banks to the database from a CSV file.

    :param cursor: (sqlite3.Cursor) The cursor to interact with the database.
    :param path: (list) A list containing the path to the CSV file containing bank data.
    :return str: The status of the operation.
    """
    with open(path[0], 'r', newline='', encoding='utf-8') as file:
        csv_reader = list(csv.DictReader(file))
        for bank in csv_reader:
            validate_bank_data(bank)
            cursor.execute(f'INSERT INTO Bank (name) VALUES ("{bank["name"]}")')
    logger.info("Banks added from CSV successfully.")
    return 'The operation was successful.'


@establish_db_connection
def add_user_from_csv(cursor, path):
    """
    Add users to the database from a CSV file.

    :param cursor: (sqlite3.Cursor) The cursor to interact with the database.
    :param path: (list) A list containing the path to the CSV file containing user data.
    :return str: The status of the operation.
    """
    with open(path[0], 'r', newline='', encoding='utf-8') as file:
        csv_reader = list(csv.DictReader(file))
        for user in csv_reader:
            validate_user_data(user)
            cursor.execute('INSERT INTO User '
                           '(Name, Surname, Birth_day, Accounts) VALUES (?, ?, ?, ?)',
                           (user['Name'], user['Surname'], user['Birth_day'], user['Accounts']))
    logger.info("Users added from CSV successfully.")
    return 'The operation was successful.'


@establish_db_connection
def add_account_from_csv(cursor, path):
    """
    Add accounts to the database from a CSV file.

    :param cursor: (sqlite3.Cursor) The cursor to interact with the database.
    :param path: (list) A list containing the path to the CSV file containing account data.
    :return str: The status of the operation.
    """
    with open(path[0], 'r', newline='', encoding='utf-8') as file:
        csv_reader = list(csv.DictReader(file))
        for account in csv_reader:
            validate_account_data(account)
            cursor.execute('INSERT INTO Account (User_id, Type, Account_Number, Bank_id, Currency, Amount, Status)'
                           'VALUES (?, ?, ?, ?, ?, ?, ?)',
                           (account['User_id'], account['Type'], account['Account_Number'],
                            account['Bank_id'], account['Currency'], account['Amount'], account['Status'],))
    logger.info("Accounts added from CSV successfully.")
    return 'The operation was successful.'


@establish_db_connection
def modify_bank(cursor, bank_data):
    """
    Modify bank information in the database.

    :param cursor: (sqlite3.Cursor) The cursor to interact with the database.
    :param bank_data: (list) A list containing the bank ID and new bank name.
    :return str: The status of the operation.
    """
    validate_bank_data(bank_data[1])
    cursor.execute(f'UPDATE Bank SET name = "{bank_data[1]}" WHERE id = {bank_data[0]}')
    logger.info("Bank modified successfully.")
    return 'The operation was successful.'


@establish_db_connection
def modify_user(cursor, user_data):
    """
    Modify user information in the database.

    :param cursor: (sqlite3.Cursor) The cursor to interact with the database.
    :param user_data: (list) A list containing user ID and modified user data.
    :return str: The status of the operation.
    """
    validate_user_data(user_data[1:])
    cursor.execute(f'UPDATE User '
                   f'SET Name = "{user_data[1]}", Surname = "{user_data[2]}", '
                   f'Birth_day = "{user_data[3]}", Accounts = "{user_data[4]}" WHERE Id = {user_data[0]}')
    logger.info("User modified successfully.")
    return 'The operation was successful.'


@establish_db_connection
def modify_account(cursor, account_data):
    """
    Modify account information in the database.

    :param cursor: (sqlite3.Cursor) The cursor to interact with the database.
    :param account_data: (list) A list containing account ID and modified account data.
    :return str: The status of the operation.
    """
    validate_account_data(account_data[1:])
    cursor.execute(f'UPDATE Account '
                   f'SET User_id = {account_data[1]}, Type = "{account_data[2]}", '
                   f'Account_Number = {account_data[3]}, Bank_id = {account_data[4]}, '
                   f'Currency = "{account_data[5]}", Amount = {account_data[6]}, Status = "{account_data[7]}" '
                   f'WHERE Id = {account_data[0]}')
    logger.info("Account modified successfully.")
    return 'The operation was successful.'


@establish_db_connection
def delete_bank(cursor, bank_id):
    """
    Delete a bank from the database.

    :param cursor: (sqlite3.Cursor) The cursor to interact with the database.
    :param bank_id: (list) A list containing the ID of the bank to be deleted.
    :return str: The status of the operation.
    """
    cursor.execute(f'DELETE FROM Bank WHERE id = {bank_id[0]}')
    logger.info("Bank deleted successfully.")
    return 'The operation was successful.'


@establish_db_connection
def delete_user(cursor, user_id):
    """
    Delete a user from the database.

    :param cursor: (sqlite3.Cursor) The cursor to interact with the database.
    :param user_id: (list) A list containing the ID of the user to be deleted.
    :return str: The status of the operation.
    """
    cursor.execute(f'DELETE FROM User WHERE id = {user_id[0]}')
    logger.info("User deleted successfully.")
    return 'The operation was successful.'


@establish_db_connection
def delete_account(cursor, account_id):
    """
    Delete an account from the database.

    :param cursor: (sqlite3.Cursor) The cursor to interact with the database.
    :param account_id: (list) A list containing the ID of the account to be deleted.
    :return str: The status of the operation.
    """
    cursor.execute(f'DELETE FROM Account WHERE id = {account_id[0]}')
    logger.info("Account deleted successfully.")
    return 'The operation was successful.'


@establish_db_connection
def transfer_money(cursor, transfer_data):
    """
    Perform a money transfer between accounts.

    :param cursor: (sqlite3.Cursor) The cursor to interact with the database.
    :param transfer_data: (list) A list containing sender's account ID, recipient's account ID, and amount.
    :return str: The status of the operation.
    """
    # PREPARE THE DATA FOR FURTHER USE
    sender_amount = list(cursor.execute(f'SELECT Amount FROM Account WHERE Id = {transfer_data[0]}'))[0][0]
    sender_currency = list(cursor.execute(f'SELECT Currency FROM Account WHERE Id = {transfer_data[0]}'))[0][0]
    recipient_currency = list(cursor.execute(f'SELECT Currency FROM Account WHERE Id = {transfer_data[1]}'))[0][0]

    client = freecurrencyapi.Client('fca_live_oEQfakDlvq3ygAFqK36LYvswprqzEXu6MkQ3EmVV')
    currency = client.latest()['data']

    # CONVERT CURRENCY
    if sender_currency == recipient_currency:
        converted_amount = transfer_data[2]
    else:
        converted_amount = transfer_data[2] * currency[sender_currency]

    # MAKE THE TRANSFER
    if sender_amount >= transfer_data[2]:
        # RECIPIENT
        cursor.execute(f'UPDATE Account SET Amount = Amount + {converted_amount} WHERE Id = {transfer_data[1]}')
        # SENDER
        cursor.execute(f'UPDATE Account SET Amount = Amount - {transfer_data[2]} WHERE Id = {transfer_data[0]}')
    else:
        return 'The sender does not have enough money'

    # FILL TRANSACTIONS TABLE
    id_bank_sender = list(cursor.execute(f'SELECT Bank_id FROM Account WHERE Id = {transfer_data[0]}'))[0][0]
    id_bank_receiver = list(cursor.execute(f'SELECT Bank_id FROM Account WHERE Id = {transfer_data[1]}'))[0][0]

    bank_sender_name = list(cursor.execute(f'SELECT name FROM Bank WHERE Id = {id_bank_sender}'))[0][0]
    bank_receiver_name = list(cursor.execute(f'SELECT name FROM Bank WHERE Id = {id_bank_receiver}'))[0][0]

    cursor.execute('INSERT INTO Transactions (Bank_sender_name, Account_sender_id, '
                   'Bank_receiver_name, Account_receiver_id, Sent_Currency, Sent_Amount, Datetime) '
                   'VALUES (?, ?, ?, ?, ?, ?, ?)',
                   (bank_sender_name, transfer_data[0], bank_receiver_name, transfer_data[1],
                    sender_currency, transfer_data[2],
                    datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')))
    logger.info("Money transfer completed successfully.")
    return 'The operation was successful.'


conn1 = sqlite3.connect('data.db')
cursor1 = conn1.cursor()

print('Bank:')
for i in cursor1.execute('SELECT * FROM Bank'):
    print(i)

print('User:')
for i in cursor1.execute('SELECT * FROM User'):
    print(i)

print('Account:')
for i in cursor1.execute('SELECT * FROM Account'):
    print(i)

print('Transactions:')
for i in cursor1.execute('SELECT * FROM Transactions'):
    print(i)

conn1.commit()
conn1.close()
