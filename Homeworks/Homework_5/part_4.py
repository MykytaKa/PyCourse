import random
from datetime import datetime, timezone, timedelta
import sqlite3
import freecurrencyapi
from collections import Counter
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def establish_connection(func):
    """
    A decorator that establishes a connection to the SQLite database, executes the wrapped
    function, and then commits and closes the connection.

    :param: func (function): The function to be wrapped.
    :return: function: The wrapper function.
    """
    def wrapper():
        logger.info("Establishing database connection")
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()

        result = func(cursor)

        conn.commit()
        conn.close()
        logger.info("Database connection closed")
        return result

    return wrapper


def randomly_assign_discounts(num_users):
    """
    Randomly assigns discounts to a specified number of users.

    :param: num_users (int): The number of users to assign discounts to.
    :return: dict: A dictionary containing user IDs as keys and assigned discounts as values.
    :raises: ValueError: If the number of users is too high or negative.
    """
    logger.info(f"Randomly assigning discounts to {num_users} users")
    if num_users > 10:
        raise ValueError('Too many users have been selected')
    if num_users < 0:
        raise ValueError('Amount of user\'s can not be negative')

    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()

    credits_discount = [25, 30, 50]
    user_with_discounts = {}
    user_ids = [i[0] for i in cursor.execute('SELECT Id FROM User')]
    user_ids = random.sample(user_ids, num_users)

    for user_id in user_ids:
        discount = random.choice(credits_discount)
        user_with_discounts[user_id] = discount

    conn.commit()
    conn.close()
    logger.info("Discount assignment completed")
    return user_with_discounts


@establish_connection
def get_debtors_full_name(cursor):
    """
    Retrieves the full names of users with negative account balances.

    :return: list: A list of full names of users with negative account balances.
    """
    logger.info("Retrieving full names of users with negative account balances")
    debtors_id = [i[0] for i in cursor.execute('SELECT User_id FROM Account WHERE Amount < 0')]
    return [' '.join(list(cursor.execute(f'SELECT Name, Surname FROM User WHERE Id = {debtor_id}'))[0])
            for debtor_id in debtors_id]


@establish_connection
def get_bank_with_the_biggest_capital(cursor):
    """
    Retrieves the bank with the highest capital in converted currency.

    :return: tuple: A tuple containing a dictionary of bank capitals and the name of the bank
                    with the highest capital.
    """
    logger.info("Retrieving bank with the highest capital")
    client = freecurrencyapi.Client('fca_live_oEQfakDlvq3ygAFqK36LYvswprqzEXu6MkQ3EmVV')
    currency = client.latest()['data']
    banks_capital = {}

    cursor.execute('SELECT Bank_id, Currency, Amount FROM Account')
    rows = cursor.fetchall()

    for row in rows:
        bank_id, account_currency, account_amount = row
        converted_amount = account_amount * currency[account_currency]
        bank_name = list(cursor.execute(f'SELECT name FROM Bank WHERE id = {bank_id}'))[0]
        banks_capital.setdefault(bank_name, 0)
        banks_capital[bank_name] += converted_amount
    logger.info("Capital retrieval completed")
    return max(banks_capital)[0]


@establish_connection
def get_bank_with_the_oldest_client(cursor):
    """
    Retrieves the name of the bank with the oldest client.

    :return: str: The name of the bank with the oldest client.
    """
    logger.info("Retrieving bank with the oldest client")
    account_data = [i for i in list(cursor.execute('SELECT User_id, Bank_id FROM Account'))]
    bank_id_with_the_oldest_client = account_data[0][1]
    the_oldest_client_birth_day = datetime.strptime(list(cursor.execute(f'SELECT Birth_day FROM User '
                                                                        f'WHERE Id = {account_data[0][0]}'))[0][0],
                                                    '%d-%m-%Y')
    for user_id, bank_id in account_data:
        current_account_birth_day = datetime.strptime(list(cursor.execute(f'SELECT Birth_day FROM User '
                                                                          f'WHERE Id = {user_id}'))[0][0],
                                                      '%d-%m-%Y')
        if the_oldest_client_birth_day > current_account_birth_day:
            the_oldest_client_birth_day = current_account_birth_day
            bank_id_with_the_oldest_client = bank_id
    logger.info("Bank with the oldest client retrieved")
    return list(cursor.execute(f'SELECT name FROM Bank WHERE id = {bank_id_with_the_oldest_client}'))[0][0]


@establish_connection
def get_bank_with_highest_unique_outbound_users(cursor):
    """
    Retrieves the bank with the highest number of unique users with outbound transactions.

    :return: tuple: A tuple containing the bank name and the count of unique outbound users.
    """
    logger.info("Retrieving bank with the highest unique outbound users")
    transactions_data = set([i for i in list(cursor.execute('SELECT Bank_sender_name, Account_sender_id '
                                                        'FROM Transactions'))])
    bank_frequency = {}
    for data in transactions_data:
        bank_frequency.setdefault(data[0], 0)
        bank_frequency[data[0]] += 1
    return Counter(bank_frequency).most_common(1)[0][0]


def filter_by_datetime_transactions(transaction):
    """
    Filters transactions based on their datetime.

    :param: transaction (tuple): A tuple containing transaction data.
    :return: bool: True if the transaction datetime is within the last 90 days, otherwise False.
    """
    logger.info("Filtering transactions by datetime")
    transaction_datetime = datetime.strptime(transaction[7], '%Y-%m-%d %H:%M:%S')

    time_delta = datetime.now(timezone.utc) - timedelta(days=90)
    temp_date = datetime.strftime(time_delta, '%Y-%m-%d %H:%M:%S')
    delta_time = datetime.strptime(temp_date, '%Y-%m-%d %H:%M:%S')

    if transaction_datetime > delta_time:
        return True
    else:
        return False


def get_user_last_three_months_transactions(user_id):
    """
    Retrieves a user's transactions from the last three months.

    :param: user_id (int): The ID of the user whose transactions are being retrieved.

    :return: list: A list of transactions within the last three months for the given user.
    """
    logger.info(f"Retrieving transactions for user {user_id} from the last three months")
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()

    transactions = [i for i in list(cursor.execute('SELECT * FROM Transactions'))]
    transactions = [transaction for transaction in transactions
                    if transaction[2] == user_id or transaction[4] == user_id]
    transactions = list(filter(filter_by_datetime_transactions, transactions))
    conn.commit()
    conn.close()
    logger.info("Transaction retrieval completed")
    return transactions


print(get_bank_with_highest_unique_outbound_users())
