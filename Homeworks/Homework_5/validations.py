import re
import freecurrencyapi
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def validate_bank_data(bank_data):
    """
    Validates the format of a bank's name.

    :param bank_data: (str) The name of the bank to be validated.
    :raises: ValueError: If the bank's name is not a string.
    """
    logger.info("Validating bank data")
    if type(bank_data) is not str:
        raise 'Invalid bank\'s name!'


def validate_account_number(number):
    """
    Validates the format and length of an account number.

    :param number: (str) The account number to be validated.
    :raises: ValueError: If the account number has an invalid length or format.
    """
    logger.info("Validating account number")
    number = re.sub(r'\W', '-', number)
    if len(number) < 18:
        raise ValueError('Invalid account number: too little chars!')
    if len(number) > 18:
        raise ValueError('Invalid account number: too many chars!')
    if not number.startswith('ID--'):
        raise ValueError('Invalid account number: wrong format!')
    pattern = r'^ID--(\w{1,3})-(\d+)-\w+$'
    if not re.match(pattern, number):
        raise ValueError("Invalid account number: broken ID!")


def validate_user_data(user_data):
    """
    Validates user-related data.

    :param user_data: (list) A list containing user's name, surname, birthdate, and account number.
    :raises: ValueError: If the user data has an invalid number of arguments or incorrect types.
    """
    logger.info("Validating user data")
    if len(user_data) != 4:
        raise ValueError(f'Too few\\many arguments in user\'s data: {user_data}')
    if type(user_data[0]) is not str:
        raise ValueError(f'Invalid value: user\'s name!: {user_data}')
    if type(user_data[1]) is not str:
        raise ValueError(f'Invalid value: user\'s surname!: {user_data}')
    if not re.search(r'(\d{2})-(\d{2})-(\d{4})', user_data[2]) or type(user_data[2]) is not str:
        raise ValueError(f'Invalid value: user\'s birth day!: {user_data}')
    validate_account_number(user_data[3])


def validate_account_data(account_data):
    """
    Validates account-related data, including user ID, account type, account number ID, bank ID,
    currency, amount, and account status.

    :param account_data: (list) A list containing account data.

    :raises ValueError: If the account data has an invalid number of arguments or incorrect types.
                         If the account currency, amount, or status is invalid.
    """
    logger.info("Validating account data")
    if len(account_data) != 7:
        raise ValueError(f'Too few\\many arguments in account\'s data: {account_data}')
    if type(account_data[0]) is not int:
        raise ValueError(f'Invalid value: account\'s user id!: {account_data}')
    if account_data[1] not in ['debit', 'credit']:
        raise ValueError(f'Invalid value: account\'s type!: {account_data}')
    if type(account_data[2]) is not int:
        raise ValueError(f'Invalid value: account\'s number id!: {account_data}')
    if type(account_data[3]) is not int:
        raise ValueError(f'Invalid value: account\'s bank id!: {account_data}')

    client = freecurrencyapi.Client('fca_live_oEQfakDlvq3ygAFqK36LYvswprqzEXu6MkQ3EmVV')
    currency = client.latest()['data']

    if account_data[4] not in currency.keys():
        raise ValueError(f'Invalid value: account\'s currency!: {account_data}')
    if type(account_data[5]) is not float:
        raise ValueError(f'Invalid value: account\'s amount!: {account_data}')
    if account_data[6] not in ['gold', 'silver', 'platinum']:
        raise ValueError(f'Invalid value: account\'s status!: {account_data}')
