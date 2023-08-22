import re
from Homeworks.Homework_5.utils import get_logger, get_currency

logger = get_logger()

ACCOUNT_STATUSES = ['gold', 'silver', 'platinum']


def check_objects_instance(objects, data):
    for key, value in objects.items():
        if not isinstance(data[key], value[0]):
            raise ValueError(f'Invalid value: {value[1]}')


def validate_bank_data(bank_data):
    """
    Validates the format of a bank's name.

    :param bank_data: (str) The name of the bank to be validated.
    :raises: ValueError: If the bank's name is not a string.
    """
    logger.info('Validating bank data')
    checked_values = {0: (str, f'bank\'s name!: {bank_data}')}
    check_objects_instance(checked_values, bank_data)


def validate_account_number(number):
    """
    Validates the format and length of an account number.

    :param number: (str) The account number to be validated.
    :raises: ValueError: If the account number has an invalid length or format.
    """
    logger.info('Validating account number')
    number = re.sub(r'\W', '-', number)
    if len(number) < 18:
        raise ValueError('Invalid account number: too little chars!')
    elif len(number) > 18:
        raise ValueError('Invalid account number: too many chars!')
    elif not number.startswith('ID--'):
        raise ValueError('Invalid account number: wrong format!')
    pattern = r'....\w{1,3}-\d+-\w+'
    if not re.match(pattern, number):
        raise ValueError('Invalid account number: broken ID!')


def validate_user_data(user_data):
    """
    Validates user-related data.

    :param user_data: (list) A list containing user's name, surname, birthdate, and account number.
    :raises: ValueError: If the user data has an invalid number of arguments or incorrect types.
    """
    logger.info('Validating user data')
    if len(user_data) != 4:
        raise ValueError(f'Too few\\many arguments in user\'s data: {user_data}')
    elif not re.search(r'(\d{2})-(\d{2})-(\d{4})', user_data[2]) or not isinstance(user_data[2], str):
        raise ValueError(f'Invalid value: user\'s birth day!: {user_data}')
    validate_account_number(user_data[3])

    checked_values = {
        0: (str, f'user\'s name!: {user_data}'),
        1: (str, f'user\'s surname!: {user_data}')
    }
    check_objects_instance(checked_values, user_data)


def validate_account_data(account_data):
    """
    Validates account-related data, including user ID, account type, account number ID, bank ID,
    currency, amount, and account status.

    :param account_data: (list) A list containing account data.

    :raises ValueError: If the account data has an invalid number of arguments or incorrect types.
                         If the account currency, amount, or status is invalid.
    """
    logger.info('Validating account data')
    currency = get_currency()

    if len(account_data) != 7:
        raise ValueError(f'Too few\\many arguments in account\'s data: {account_data}')
    elif account_data[1] not in ['debit', 'credit']:
        raise ValueError(f'Invalid value: account\'s type!: {account_data}')
    elif account_data[4] not in currency.keys():
        raise ValueError(f'Invalid value: account\'s currency!: {account_data}')
    elif account_data[6] not in ACCOUNT_STATUSES:
        raise ValueError(f'Invalid value: account\'s status!: {account_data}')
    checked_values = {
        0: (int, f'account\'s user id!: {account_data}'),
        2: (int, f'account\'s number id!: {account_data}'),
        3: (int, f'account\'s bank id!: {account_data}'),
        5: (float, f'account\'s amount!: {account_data}')
    }
    check_objects_instance(checked_values, account_data)
