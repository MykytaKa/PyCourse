"""
The module contains functions for adding, modifying, and deleting data in the database, as well as performing
money transfers between accounts.

It provides functions to perform various operations on database tables including banks, users, and accounts. These
functions handle data insertion, modification, deletion, and money transfers using the provided cursor. The module also
uses decorators and utility functions for database connection management, logging, and currency retrieval.

Global Constants:
- logger: The logger instance configured for the module.

Functions:
- add_data(cursor, input_data, table_name, params_insert, message_return, vld_fnc): Add data to a database table.
- add_bank(cursor, *bank_data): Add banks to the database.
- parse_user_full_name(user_data): Parse user full name data into a formatted list.
- add_user(cursor, *user_data): Add users to the database.
- add_account(cursor, *account_data): Add accounts to the database.
- add_data_from_csv(cursor, path, table_name, params_insert, return_message, vld_fnc): Add data from a CSV file to a
database table.
- add_bank_from_csv(cursor, path): Add banks to the database from a CSV file.
- add_user_from_csv(cursor, path): Add users to the database from a CSV file.
- add_account_from_csv(cursor, path): Add accounts to the database from a CSV file.
- modify_data(cursor, data, table_name, params_insert, return_message, vld_fnc): Modify data in a database table.
- modify_bank(cursor, *bank_data): Modify bank information in the database.
- modify_user(cursor, *user_data): Modify user information in the database.
- modify_account(cursor, *account_data): Modify account information in the database.
- delete_data(cursor, data_id, table_name, input_param, return_message): Delete data from a database table.
- delete_bank(cursor, bank_id): Delete a bank from the database.
- delete_user(cursor, user_id): Delete a user from the database.
- delete_account(cursor, account_id): Delete an account from the database.
- transfer_money(cursor, sender_id, recipient_id, money_amount, user_date=None): Perform a money transfer between
accounts.
- convert_money(cursor, sender_currency, recipient_id, money_amount): Convert money from the sender's currency to
the recipient's currency.
- make_approved_transfer(cursor, money_amount, converted_amount, recipient_id, sender_id, sender_currency, user_date):
    Execute an approved money transfer between accounts and record the transaction.

Note: The module contains a combination of functions for database operations and money transfers, utilizing
decorators for database connection management, validation functions for data input, and utility functions for
logging and currency retrieval.
"""
import csv
import re
from datetime import datetime, timezone
from Homeworks.Homework_5.validations import validate_bank_data, validate_user_data, validate_account_data
from Homeworks.Homework_5.utils import establish_db_connection, get_logger, get_currency
from Homeworks.Homework_5.constants import SELECT_COMMAND, UPDATE_COMMAND

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

    :return: (str) The message_return upon successful data insertion.

    :raise Exception: If validation fails for any of the input_data.
    """
    for data in input_data:
        vld_fnc(data)
        question_marks = ('?,' * len(params_insert.split(',')))[:-1]
        cursor.execute(f'INSERT INTO {table_name} ({params_insert}) VALUES ({question_marks})', data)
    return message_return


@establish_db_connection
def add_bank(cursor, *bank_data):
    """
    Add banks to the database.

    :param cursor: (sqlite3.Cursor) The cursor to interact with the database.
    :param bank_data: (list) A list of bank names to be added.

    :return: (str) The status of the operation.
    """
    return add_data(cursor=cursor,
                    input_data=bank_data,
                    table_name='Bank',
                    params_insert='name',
                    message_return='Banks added successfully.',
                    vld_fnc=validate_bank_data)


def parse_user_full_name(user_data):
    """
    Parse user full name data into a formatted list.
    This function takes a list of user data where each element contains the first name,
    last name, and additional information. It parses this data and returns a list
    of tuples containing formatted first name, last name, and additional information.

    :param user_data: (list) List of user data where each element contains first name,
                             last name, and additional information.

    :return: (list) A list of tuples with formatted user information.
    """
    user_data = [(re.sub('[~!@#$%^&*()_+|/\\?.,=-]', '', i[0]), *i[1:]) for i in user_data]
    return [(*i[0].split(), *i[1:]) for i in user_data]


@establish_db_connection
def add_user(cursor, *user_data):
    """
    Add users to the database.

    :param cursor: (sqlite3.Cursor) The cursor to interact with the database.
    :param user_data: (list) A list of user data, where each element is a list containing user information.
                            The format of user_data: [[full_name, birth_day, accounts], ...]

    :return: (str) The status of the operation.
    """
    user_data = parse_user_full_name(user_data)
    return add_data(cursor=cursor,
                    input_data=user_data,
                    table_name='User',
                    params_insert='Name, Surname, Birth_day, Accounts',
                    message_return='User(s) added successfully.',
                    vld_fnc=validate_user_data)


@establish_db_connection
def add_account(cursor, *account_data):
    """
    Add accounts to the database.

    :param cursor: (sqlite3.Cursor) The cursor to interact with the database.
    :param account_data: (list) A list of account data, where each element is a tuple containing account information.
                                The format of account_data: [(User_id, Type, Account_Number,
                                                            Bank_id, Currency, Amount, Status), ...]

    :return: (str) The status of the operation.
    """
    return add_data(cursor=cursor,
                    input_data=account_data,
                    table_name='Account',
                    params_insert='User_id, Type, Account_Number, Bank_id, Currency, Amount, Status',
                    message_return='Accounts added successfully.',
                    vld_fnc=validate_account_data)


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

    :return: (str) The return_message upon successful data insertion.

    :raise Exception: If validation fails for any of the data from the CSV file.
    """
    with open(path[0], 'r', newline='', encoding='utf-8') as file:
        csv_reader = list(csv.DictReader(file))
        for data in csv_reader:
            add_data(cursor=cursor,
                     input_data=list(data.values()),
                     table_name=table_name,
                     params_insert=params_insert,
                     message_return=return_message,
                     vld_fnc=vld_fnc)
    return return_message


@establish_db_connection
def add_bank_from_csv(cursor, path):
    """
    Add banks to the database from a CSV file.

    :param cursor: (sqlite3.Cursor) The cursor to interact with the database.
    :param path: (str) The path to the CSV file containing bank data.

    :return: (str) The status of the operation.
    """
    return add_data_from_csv(cursor=cursor,
                             path=path,
                             table_name='Bank',
                             params_insert='name',
                             return_message='Banks added from CSV successfully.',
                             vld_fnc=validate_bank_data)


@establish_db_connection
def add_user_from_csv(cursor, path):
    """
    Add users to the database from a CSV file.

    :param cursor: (sqlite3.Cursor) The cursor to interact with the database.
    :param path: (str) The path to the CSV file containing user data.

    :return: (str) The status of the operation.
    """
    return add_data_from_csv(cursor=cursor,
                             path=path,
                             table_name='User',
                             params_insert='Name, Surname, Birth_day, Accounts',
                             return_message='Users added from CSV successfully.',
                             vld_fnc=validate_user_data)


@establish_db_connection
def add_account_from_csv(cursor, path):
    """
    Add accounts to the database from a CSV file.

    :param cursor: (sqlite3.Cursor) The cursor to interact with the database.
    :param path: (str) The path to the CSV file containing account data.

    :return: (str) The status of the operation.
    """
    add_data_from_csv(cursor=cursor,
                      path=path,
                      table_name='Account',
                      params_insert='User_id, Type, Account_Number, Bank_id, Currency, Amount, Status',
                      return_message='Accounts added from CSV successfully.',
                      vld_fnc=validate_account_data)


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

    :return: (str) The return_message upon successful data modification.

    :raise Exception: If validation fails for the data to be updated.
    """
    vld_fnc(data[:-1])
    params = params_insert.split(',')
    params_insert_string = [f'{param.strip()} = ?' for param in params[1:]]
    params_insert_string = ', '.join(params_insert_string)
    cursor.execute(f'UPDATE {table_name} SET {params_insert_string} WHERE {params[0]} = ?', data)
    return return_message


@establish_db_connection
def modify_bank(cursor, *bank_data):
    """
    Modify bank information in the database.

    :param cursor: (sqlite3.Cursor) The cursor to interact with the database.
    :param bank_data: (list) A list containing the bank ID and new bank name.
    :return: (str) The status of the operation.
    """
    return modify_data(cursor=cursor,
                       data=bank_data,
                       table_name='Bank',
                       params_insert='id, name',
                       return_message='Bank modified successfully.',
                       vld_fnc=validate_bank_data)


@establish_db_connection
def modify_user(cursor, *user_data):
    """
    Modify user information in the database.

    :param cursor: (sqlite3.Cursor) The cursor to interact with the database.
    :param user_data: (list) A list containing user ID and modified user data.
    :return: (str) The status of the operation.
    """
    return modify_data(cursor=cursor,
                       data=user_data,
                       table_name='User',
                       params_insert='Id, Name, Surname, Birth_day, Accounts',
                       return_message='User modified successfully.',
                       vld_fnc=validate_user_data)


@establish_db_connection
def modify_account(cursor, *account_data):
    """
    Modify account information in the database.

    :param cursor: (sqlite3.Cursor) The cursor to interact with the database.
    :param account_data: (list) A list containing account ID and modified account data.
    :return: (str) The status of the operation.
    """
    return modify_data(cursor=cursor,
                       data=account_data,
                       table_name='Account',
                       params_insert='Id, User_id, Type, Account_Number, Bank_id, Currency, Amount, Status',
                       return_message='Account modified successfully.',
                       vld_fnc=validate_account_data)


def delete_data(cursor, data_id, table_name, input_param, return_message):
    """
    Delete data from a database table using the provided cursor.
    This function deletes data from a specified database table using the given cursor.

    :param cursor: (sqlite3.Cursor) The cursor object to execute SQL commands.
    :param data_id: (int) The id of the data identifier for deletion.
    :param table_name: (str) The name of the target database table.
    :param input_param: (str) The name of the column used for data identification.
    :param return_message: (str) Message to be returned upon successful deletion.

    :return: (str) The return_message upon successful data deletion.
    """
    cursor.execute(f'DELETE FROM {table_name} WHERE {input_param} = {data_id}')
    return return_message


@establish_db_connection
def delete_bank(cursor, bank_id):
    """
    Delete a bank from the database.

    :param cursor: (sqlite3.Cursor) The cursor to interact with the database.
    :param bank_id: (int) The ID of the bank to be deleted.
    :return: (str) The status of the operation.
    """
    return delete_data(cursor=cursor,
                       data_id=bank_id,
                       table_name='Bank',
                       input_param='id',
                       return_message='Bank deleted successfully.')


@establish_db_connection
def delete_user(cursor, user_id):
    """
    Delete a user from the database.

    :param cursor: (sqlite3.Cursor) The cursor to interact with the database.
    :param user_id: (int) The ID of the user to be deleted.
    :return: (str) The status of the operation.
    """
    return delete_data(cursor=cursor,
                       data_id=user_id,
                       table_name='User',
                       input_param='Id',
                       return_message='User deleted successfully.')


@establish_db_connection
def delete_account(cursor, account_id):
    """
    Delete an account from the database.

    :param cursor: (sqlite3.Cursor) The cursor to interact with the database.
    :param account_id: (int) The ID of the account to be deleted.
    :return: (str) The status of the operation.
    """
    return delete_data(cursor=cursor,
                       data_id=account_id,
                       table_name='Account',
                       input_param='Id',
                       return_message='Account deleted successfully.')


@establish_db_connection
def transfer_money(cursor, sender_id, recipient_id, money_amount, user_date=None):
    """
    Perform a money transfer between accounts.

    :param cursor: (sqlite3.Cursor) The cursor to interact with the database.
    :param sender_id: (int) The ID of the sender's account.
    :param recipient_id: (int) The ID of the recipient's account.
    :param money_amount: (float) The amount of money to be transferred.
    :param user_date: (str, optional) The date and time of the transfer in UTC. Defaults to None.
    :return str: The status of the operation.
    """
    # PREPARE THE DATA FOR FURTHER USE
    cursor.execute(SELECT_COMMAND.format('Amount, Currency', 'Account', sender_id))
    sender_amount, sender_currency = cursor.fetchone()

    # TERMINATE THE EXECUTION IN CASE OF LACK OF FUNDS
    if sender_amount < money_amount:
        return 'The sender does not have enough money'

    # CONVERT CURRENCY
    converted_amount = convert_money(cursor=cursor,
                                     sender_currency=sender_currency,
                                     recipient_id=recipient_id,
                                     money_amount=money_amount)

    # MAKE THE TRANSFER
    return make_approved_transfer(cursor=cursor,
                                  money_amount=money_amount,
                                  converted_amount=converted_amount,
                                  recipient_id=recipient_id,
                                  sender_id=sender_id,
                                  sender_currency=sender_currency,
                                  user_date=user_date)


def convert_money(cursor, sender_currency, recipient_id, money_amount):
    """
    Convert a certain amount of money from the sender's currency to the recipient's currency.

    :param cursor: (sqlite3.Cursor) The cursor used to interact with the database.
    :param sender_currency: (str) The currency code of the sender's account.
    :param recipient_id: (int) The recipient's account ID.
    :param money_amount: (float) The amount of money to be converted.
    Returns: (float) The converted amount of money in the recipient's currency.
    """
    cursor.execute(SELECT_COMMAND.format('Currency', 'Account', recipient_id))
    recipient_currency = cursor.fetchone()[0]
    currency = get_currency()
    currency_rate = 1 if sender_currency == recipient_currency else currency[sender_currency]
    return money_amount * currency_rate


def make_approved_transfer(cursor, money_amount, converted_amount, recipient_id, sender_id, sender_currency, user_date):
    """
    Execute an approved money transfer between accounts and record the transaction.

    :param cursor: (sqlite3.Cursor) The cursor to interact with the database.
    :param money_amount: (float) The original amount of money to be transferred.
    :param converted_amount: (float) The amount of money after currency conversion.
    :param recipient_id: (int) The ID of the recipient's account.
    :param sender_id: (int) The ID of the sender's account.
    :param sender_currency: (str) The currency of the sender's account.
    :param user_date: (str) The date and time of the transfer in UTC.

    :return: (str) A status message indicating the successful completion of the transfer.

    :raises: Any database-related exceptions that may occur during execution.
    """
    # RECIPIENT
    cursor.execute(UPDATE_COMMAND.format('+', converted_amount, recipient_id))
    # SENDER
    cursor.execute(UPDATE_COMMAND.format('-', money_amount, sender_id))

    # FILL TRANSACTIONS TABLE
    cursor.execute(SELECT_COMMAND.format('Bank_id', 'Account', sender_id))
    id_bank_sender = cursor.fetchone()[0]
    cursor.execute(SELECT_COMMAND.format('Bank_id', 'Account', recipient_id))
    id_bank_receiver = cursor.fetchone()[0]

    cursor.execute(SELECT_COMMAND.format('name', 'Bank', id_bank_sender))
    bank_sender_name = cursor.fetchone()[0]
    cursor.execute(SELECT_COMMAND.format('name', 'Bank', id_bank_receiver))
    bank_receiver_name = cursor.fetchone()[0]
    transfer_date = user_date if not user_date else datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')

    cursor.execute('INSERT INTO Transactions (Bank_sender_name, Account_sender_id, '
                   'Bank_receiver_name, Account_receiver_id, Sent_Currency, Sent_Amount, Datetime) '
                   'VALUES (?, ?, ?, ?, ?, ?, ?)',
                   (bank_sender_name, sender_id, bank_receiver_name, recipient_id,
                    sender_currency, money_amount, transfer_date))
    return 'Money transfer completed successfully.'
