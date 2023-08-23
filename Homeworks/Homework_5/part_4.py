"""
The module contains functions for querying and analyzing banking-related data from the database.
It focuses on generating insights such as assigning discounts, retrieving user information, analyzing bank statistics,
and filtering transaction data.

Functions:
- randomly_assign_discounts(cursor): Randomly assigns discounts to a specified number of users.
- get_user_name_and_surname(cursor, debtor_id): Retrieve the name and surname of a user (debtor) based on their user ID.
- get_debtors_full_name(cursor): Retrieves the full names of users with negative account balances.
- get_bank_with_the_biggest_capital(cursor): Retrieves the bank with the highest capital in converted currency.
- get_bank_with_the_oldest_client(cursor): Retrieves the name of the bank with the oldest client.
- get_bank_with_highest_unique_outbound_users(cursor): Retrieves the bank with the highest number of unique users
  with outbound transactions.
- filter_by_datetime_transactions(transaction): Filters transactions based on their datetime.
- get_user_last_three_months_transactions(cursor, user_id): Retrieves a user's transactions from the last three months.

Global Constants:
- logger: The logger instance configured for the module.

Note: The module uses functions from the "utils" module for database connection management, as well as
global constants and SQL commands from the "constants" module. It also utilizes the "groupby" function from the
"itertools" module for grouping transactions by bank name.
"""
from itertools import groupby
from random import randint, sample, choice
from datetime import datetime, timezone, timedelta
from Homeworks.Homework_5.utils import establish_db_connection, get_logger, get_currency
from Homeworks.Homework_5.constants import SELECT_COMMAND_WITHOUT_WHERE, SELECT_COMMAND_ONLY_WHERE, SELECT_COMMAND

logger = get_logger()


@establish_db_connection
def randomly_assign_discounts(cursor):
    """
    Randomly assigns discounts to a specified number of users.

    :param cursor: (sqlite3.Cursor) The cursor object to execute SQL commands.
    :return: dict: A dictionary containing user IDs as keys and assigned discounts as values.
    :raises: ValueError: If the number of users is too high or negative.
    """
    num_users = randint(1, 10)
    logger.info(f'Randomly assigning discounts to {num_users} users')

    credits_discount = [25, 30, 50]
    user_ids = [i[0] for i in cursor.execute(SELECT_COMMAND_WITHOUT_WHERE.format('Id', 'User'))]
    user_ids = sample(user_ids, num_users)
    user_with_discounts = {user_id: choice(credits_discount) for user_id in user_ids}
    logger.info('Discount assignment completed')
    return user_with_discounts


def get_user_name_and_surname(cursor, debtor_id):
    """
    Retrieve the name and surname of a user (debtor) based on their user ID.

    :param cursor: (sqlite3.Cursor) The cursor object to execute SQL commands.
    :param debtor_id: (int) User ID of the debtor
    :return: (str) The concatenated name and surname of the user.
    """
    return ' '.join(list(cursor.execute(SELECT_COMMAND.format('Name, Surname', 'User', debtor_id)))[0])


@establish_db_connection
def get_debtors_full_name(cursor):
    """
    Retrieves the full names of users with negative account balances.

    :param cursor: (sqlite3.Cursor) The cursor object to execute SQL commands.
    :return: list: A list of full names of users with negative account balances.
    """
    logger.info('Retrieving full names of users with negative account balances')
    debtors_id = [i[0] for i in cursor.execute(SELECT_COMMAND_ONLY_WHERE.format('User_id', 'Account', 'Amount < 0'))]
    return [get_user_name_and_surname(cursor, debtor_id) for debtor_id in debtors_id]


@establish_db_connection
def get_bank_with_the_biggest_capital(cursor):
    """
    Retrieves the bank with the highest capital in converted currency.

    :param cursor: (sqlite3.Cursor) The cursor object to execute SQL commands.
    :return: tuple: A tuple containing a dictionary of bank capitals and the name of the bank
                    with the highest capital.
    """
    logger.info('Retrieving bank with the highest capital')
    currency = get_currency()
    banks_capital = {}

    cursor.execute(SELECT_COMMAND_WITHOUT_WHERE.format('Bank_id, Currency, Amount', 'Account'))
    rows = cursor.fetchall()

    for row in rows:
        bank_id, account_currency, account_amount = row
        converted_amount = account_amount * currency[account_currency]
        banks_capital.setdefault(bank_id, 0)
        banks_capital[bank_id] += converted_amount

    the_richest_bank_id = max(banks_capital, key=lambda name: banks_capital[name])
    cursor.execute(SELECT_COMMAND.format('name', 'Bank', the_richest_bank_id))
    the_richest_bank_name = cursor.fetchone()[0]
    logger.info('Capital retrieval completed')
    return the_richest_bank_name


@establish_db_connection
def get_bank_with_the_oldest_client(cursor):
    """
    Retrieves the name of the bank with the oldest client.

    :param cursor: (sqlite3.Cursor) The cursor object to execute SQL commands.
    :return: str: The name of the bank with the oldest client.
    """
    logger.info('Retrieving bank with the oldest client')
    clients_birth_day = list(cursor.execute(SELECT_COMMAND_WITHOUT_WHERE.format('id, Birth_day', 'User')))
    the_oldest_user = min(clients_birth_day, key=lambda client: datetime.strptime(client[1], '%d-%m-%Y'))
    cursor.execute(SELECT_COMMAND_ONLY_WHERE.format('Bank_id', 'Account', f'User_id = {the_oldest_user[0]}'))
    the_oldest_user_bank_id = cursor.fetchone()[0]
    cursor.execute(SELECT_COMMAND.format('name', 'Bank', the_oldest_user_bank_id))
    return cursor.fetchone()[0]


@establish_db_connection
def get_bank_with_highest_unique_outbound_users(cursor):
    """
    Retrieves the bank with the highest number of unique users with outbound transactions.

    :param cursor: (sqlite3.Cursor) The cursor object to execute SQL commands.
    :return: tuple: A tuple containing the bank name and the count of unique outbound users.
    """
    logger.info('Retrieving bank with the highest unique outbound users')
    transactions_data = set(cursor.execute(SELECT_COMMAND_WITHOUT_WHERE.format('Bank_sender_name, Account_sender_id',
                                                                               'Transactions')))
    bank_frequency = {key: list(group) for key, group in groupby(transactions_data, lambda transaction: transaction[0])}
    bank_name = max(bank_frequency, key=len)
    users_amount = len(bank_frequency[max(bank_frequency, key=len)])
    return bank_name, users_amount


def filter_by_datetime_transactions(transaction):
    """
    Filters transactions based on their datetime.

    :param: transaction (tuple): A tuple containing transaction data.
    :return: bool: True if the transaction datetime is within the last 90 days, otherwise False.
    """
    logger.info('Filtering transactions by datetime')
    transaction_datetime = datetime.strptime(transaction, '%Y-%m-%d %H:%M:%S')

    time_delta = datetime.now(timezone.utc) - timedelta(days=90)
    temp_date = datetime.strftime(time_delta, '%Y-%m-%d %H:%M:%S')
    delta_time = datetime.strptime(temp_date, '%Y-%m-%d %H:%M:%S')

    return transaction_datetime > delta_time


@establish_db_connection
def get_user_last_three_months_transactions(cursor, user_id):
    """
    Retrieves a user's transactions from the last three months.

    :param cursor: (sqlite3.Cursor) The cursor object to execute SQL commands.
    :param: user_id (int): The ID of the user whose transactions are being retrieved.
    :return: list: A list of transactions within the last three months for the given user.
    """
    logger.info(f'Retrieving transactions for user {user_id} from the last three months')
    transactions = list(cursor.execute(SELECT_COMMAND_ONLY_WHERE.format('*', 'Transactions',
                                                                        f'Account_sender_id = {user_id} OR '
                                                                        f'Account_receiver_id = {user_id}')))
    transactions = list(filter(lambda x: filter_by_datetime_transactions(x[7]), transactions))

    logger.info('Transaction retrieval completed')
    return transactions
