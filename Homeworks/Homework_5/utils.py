import logging
import sqlite3
from functools import wraps
import freecurrencyapi


def establish_db_connection(func):
    """
    A decorator that establishes a connection to the SQLite database, executes the wrapped function,
    and then commits and closes the connection.

    :param func: (function) The function to be wrapped.
    :return function: The wrapper function.
    """
    @wraps(func)
    def wrapper(*args):
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()

        if args == ():
            result = func(cursor)
        elif len(args) == 1 and type(args[0]) is not tuple:
            result = func(cursor, args[0])
        else:
            result = func(cursor, args)

        conn.commit()
        conn.close()
        return result

    return wrapper


def get_logger():
    """
    Creates and configures a logger for the module.

    :return logging.Logger: A logger instance configured for the module.
    """
    logging.basicConfig(level=logging.INFO)
    return logging.getLogger(__name__)


def get_currency():
    """
    Retrieves the latest currency data using the Free Currency API.

    :return dict: The latest currency data as returned by the Free Currency API.
    """
    client = freecurrencyapi.Client('fca_live_oEQfakDlvq3ygAFqK36LYvswprqzEXu6MkQ3EmVV')
    return client.latest()['data']
