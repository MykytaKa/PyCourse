import csv
import sqlite3
from datetime import datetime, timezone
from Homeworks.Homework_5.validations import validate_bank_data, validate_user_data, validate_account_data
from Homeworks.Homework_5.utils import establish_db_connection, get_logger, get_currency

logger = get_logger()


def add_data(cursor, input_data, table_name, params_insert, message_return, vld_fnc):
    """
    Add data to a database table using the provided cursor.
    This function inserts data into a specified database table using the given cursor.

    :param cursor: (sqlite3.Cursor) The cursor object to execute SQL commands.
    :param input_data: (list) List of data to be inserted into the table.
    :param table_name: (str) The name of the target database table.
    :param params_insert: (str) Comma-separated string of column names for insertion.
    :param message_return: (str) Message to be returned upon successful insertion.
    :param vld_fnc: (callable) Validation function to validate input_data.

    :return str: The message_return upon successful data insertion.

    :raise Exception: If validation fails for any of the input_data.
    """
    for data in input_data:
        vld_fnc(data)
        question_marks = ('?,' * len(params_insert.split(',')))[:-1]
        cursor.execute(f'INSERT INTO {table_name} ({params_insert}) VALUES ({question_marks})', data)
    return message_return


@establish_db_connection
def add_bank(cursor, bank_data):
    """
    Add banks to the database.

    :param cursor: (sqlite3.Cursor) The cursor to interact with the database.
    :param bank_data: (list) A list of bank names to be added.

    :return str: The status of the operation.
    """
    return add_data(cursor, bank_data, 'Bank', 'name', 'Banks added successfully.', validate_bank_data)


def parse_user_full_name(user_data):
    """
    Parse user full name data into a formatted list.
    This function takes a list of user data where each element contains the first name,
    last name, and additional information. It parses this data and returns a list
    of tuples containing formatted first name, last name, and additional information.

    :param user_data: (list) List of user data where each element contains first name,
                             last name, and additional information.

    :return list: A list of tuples with formatted user information.
    """
    return [(*i[0].split(), *i[1:]) for i in user_data]


@establish_db_connection
def add_user(cursor, user_data):
    """
    Add users to the database.

    :param cursor: (sqlite3.Cursor) The cursor to interact with the database.
    :param user_data: (list) A list of user data, where each element is a list containing user information.
                            The format of user_data: [[full_name, birth_day, accounts], ...]

    :return str: The status of the operation.
    """
    user_data = parse_user_full_name(user_data)
    return add_data(cursor, user_data, 'User', 'Name, Surname, Birth_day, Accounts',
                    'User(s) added successfully.', validate_user_data)


@establish_db_connection
def add_account(cursor, account_data):
    """
    Add accounts to the database.

    :param cursor: (sqlite3.Cursor) The cursor to interact with the database.
    :param account_data: (list) A list of account data, where each element is a tuple containing account information.
                                The format of account_data: [(User_id, Type, Account_Number,
                                                            Bank_id, Currency, Amount, Status), ...]

    :return str: The status of the operation.
    """
    return add_data(cursor, account_data, 'Account', 'User_id, Type, Account_Number, Bank_id, Currency, Amount, Status',
                    'Accounts added successfully.', validate_account_data)


def add_data_from_csv(cursor, path, table_name, params_insert, return_message, vld_fnc):
    """
    Add data from a CSV file to a database table.
    This function reads data from a CSV file and inserts it into a specified database table
    using the provided cursor.

    :param cursor: (sqlite3.Cursor) The cursor object to execute SQL commands.
    :param path: (str) Path to the CSV file.
    :param table_name: (str) The name of the target database table.
    :param params_insert: (str) Comma-separated string of column names for insertion.
    :param return_message: (str) Message to be returned upon successful insertion.
    :param vld_fnc: (callable) Validation function to validate input data from the CSV.

    :return str: The return_message upon successful data insertion.

    :raise Exception: If validation fails for any of the data from the CSV file.
    """
    with open(path[0], 'r', newline='', encoding='utf-8') as file:
        csv_reader = list(csv.DictReader(file))
        for data in csv_reader:
            vld_fnc(list(data.values()))
            question_marks = ('?,' * len(params_insert.split(',')))[:-1]
            cursor.execute(f'INSERT INTO {table_name} ({params_insert}) VALUES ({question_marks})', list(data.values()))
    return return_message


@establish_db_connection
def add_bank_from_csv(cursor, path):
    """
    Add banks to the database from a CSV file.

    :param cursor: (sqlite3.Cursor) The cursor to interact with the database.
    :param path: (list) A list containing the path to the CSV file containing bank data.

    :return str: The status of the operation.
    """
    return add_data_from_csv(cursor, path, 'Bank', 'name', 'Banks added from CSV successfully.', validate_bank_data)


@establish_db_connection
def add_user_from_csv(cursor, path):
    """
    Add users to the database from a CSV file.

    :param cursor: (sqlite3.Cursor) The cursor to interact with the database.
    :param path: (list) A list containing the path to the CSV file containing user data.

    :return str: The status of the operation.
    """
    return add_data_from_csv(cursor, path, 'User', 'Name, Surname, Birth_day, Accounts',
                             'Users added from CSV successfully.', validate_user_data)


@establish_db_connection
def add_account_from_csv(cursor, path):
    """
    Add accounts to the database from a CSV file.

    :param cursor: (sqlite3.Cursor) The cursor to interact with the database.
    :param path: (list) A list containing the path to the CSV file containing account data.

    :return str: The status of the operation.
    """
    add_data_from_csv(cursor, path, 'Account', 'User_id, Type, Account_Number, Bank_id, Currency, Amount, Status',
                      'Accounts added from CSV successfully.', validate_account_data)


def modify_data(cursor, data, table_name, params_insert, return_message, vld_fnc):
    """
    Modify data in a database table using the provided cursor.
    This function updates data in a specified database table using the given cursor.

    :param cursor: (sqlite3.Cursor) The cursor object to execute SQL commands.
    :param data: (list) List of data to be updated in the table.
    :param table_name: (str) The name of the target database table.
    :param params_insert: (str) Comma-separated string of column names for update.
    :param return_message: (str) Message to be returned upon successful modification.
    :param vld_fnc: (callable) Validation function to validate input data.

    :return str: The return_message upon successful data modification.

    :raise Exception: If validation fails for the data to be updated.
    """
    vld_fnc(data[:-1])
    params = params_insert.split(',')
    params_insert_string = [f'{param.strip()} = ?' for param in params[1:]]
    params_insert_string = ', '.join(params_insert_string)
    cursor.execute(f'UPDATE {table_name} SET {params_insert_string} WHERE {params[0]} = ?', data)
    return return_message


@establish_db_connection
def modify_bank(cursor, bank_data):
    """
    Modify bank information in the database.

    :param cursor: (sqlite3.Cursor) The cursor to interact with the database.
    :param bank_data: (list) A list containing the bank ID and new bank name.
    :return str: The status of the operation.
    """
    return modify_data(cursor, bank_data, 'Bank', 'id, name', 'Bank modified successfully.', validate_bank_data)


@establish_db_connection
def modify_user(cursor, user_data):
    """
    Modify user information in the database.

    :param cursor: (sqlite3.Cursor) The cursor to interact with the database.
    :param user_data: (list) A list containing user ID and modified user data.
    :return str: The status of the operation.
    """
    return modify_data(cursor, user_data, 'User', 'Id, Name, Surname, Birth_day, Accounts',
                       'User modified successfully.', validate_user_data)


@establish_db_connection
def modify_account(cursor, account_data):
    """
    Modify account information in the database.

    :param cursor: (sqlite3.Cursor) The cursor to interact with the database.
    :param account_data: (list) A list containing account ID and modified account data.
    :return str: The status of the operation.
    """
    return modify_data(cursor, account_data, 'Account', 'Id, User_id, Type, Account_Number, Bank_id, '
                                                        'Currency, Amount, Status',
                       'Account modified successfully.', validate_account_data)


def delete_data(cursor, data_id, table_name, input_param, return_message):
    """
    Delete data from a database table using the provided cursor.

    This function deletes data from a specified database table using the given cursor.

    Args:
    :param cursor: (sqlite3.Cursor) The cursor object to execute SQL commands.
    :param data_id: (int) The id of the data identifier for deletion.
    :param table_name: (str) The name of the target database table.
    :param input_param: (str) The name of the column used for data identification.
    :param return_message: (str) Message to be returned upon successful deletion.

    :return str: The return_message upon successful data deletion.
    """
    cursor.execute(f'DELETE FROM {table_name} WHERE {input_param} = {data_id}')
    return return_message


@establish_db_connection
def delete_bank(cursor, bank_id):
    """
    Delete a bank from the database.

    :param cursor: (sqlite3.Cursor) The cursor to interact with the database.
    :param bank_id: (list) A list containing the ID of the bank to be deleted.
    :return str: The status of the operation.
    """
    return delete_data(cursor, bank_id, 'Bank', 'id', 'Bank deleted successfully.')


@establish_db_connection
def delete_user(cursor, user_id):
    """
    Delete a user from the database.

    :param cursor: (sqlite3.Cursor) The cursor to interact with the database.
    :param user_id: (list) A list containing the ID of the user to be deleted.
    :return str: The status of the operation.
    """
    return delete_data(cursor, user_id, 'User', 'Id', 'User deleted successfully.')


@establish_db_connection
def delete_account(cursor, account_id):
    """
    Delete an account from the database.

    :param cursor: (sqlite3.Cursor) The cursor to interact with the database.
    :param account_id: (list) A list containing the ID of the account to be deleted.
    :return str: The status of the operation.
    """
    return delete_data(cursor, account_id, 'Account', 'Id', 'Account deleted successfully.')


@establish_db_connection
def transfer_money(cursor, transfer_data):
    """
    Perform a money transfer between accounts.

    :param cursor: (sqlite3.Cursor) The cursor to interact with the database.
    :param transfer_data: (list) A list containing sender's account ID, recipient's account ID, and amount.
    :return str: The status of the operation.
    """
    # PREPARE THE DATA FOR FURTHER USE
    cursor.execute(f'SELECT Amount, Currency FROM Account WHERE Id = {transfer_data[0]}')
    sender_amount, sender_currency = cursor.fetchone()
    cursor.execute(f'SELECT Currency FROM Account WHERE Id = {transfer_data[1]}')
    recipient_currency = cursor.fetchone()[0]

    currency = get_currency()

    # CONVERT CURRENCY
    converted_amount = transfer_data[2] if sender_currency == recipient_currency \
        else transfer_data[2] * currency[sender_currency]

    # MAKE THE TRANSFER
    if sender_amount >= transfer_data[2]:
        # RECIPIENT
        cursor.execute(f'UPDATE Account SET Amount = Amount + {converted_amount} WHERE Id = {transfer_data[1]}')
        # SENDER
        cursor.execute(f'UPDATE Account SET Amount = Amount - {transfer_data[2]} WHERE Id = {transfer_data[0]}')
    else:
        return 'The sender does not have enough money'

    # FILL TRANSACTIONS TABLE
    cursor.execute(f'SELECT Bank_id FROM Account WHERE Id = {transfer_data[0]}')
    id_bank_sender = cursor.fetchone()[0]
    cursor.execute(f'SELECT Bank_id FROM Account WHERE Id = {transfer_data[1]}')
    id_bank_receiver = cursor.fetchone()[0]

    cursor.execute(f'SELECT name FROM Bank WHERE Id = {id_bank_sender}')
    bank_sender_name = cursor.fetchone()[0]
    cursor.execute(f'SELECT name FROM Bank WHERE Id = {id_bank_receiver}')
    bank_receiver_name = cursor.fetchone()[0]

    cursor.execute('INSERT INTO Transactions (Bank_sender_name, Account_sender_id, '
                   'Bank_receiver_name, Account_receiver_id, Sent_Currency, Sent_Amount, Datetime) '
                   'VALUES (?, ?, ?, ?, ?, ?, ?)',
                   (bank_sender_name, transfer_data[0], bank_receiver_name, transfer_data[1],
                    sender_currency, transfer_data[2],
                    datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')))
    return 'Money transfer completed successfully.'
