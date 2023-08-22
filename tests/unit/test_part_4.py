import random
import pytest
from unittest.mock import MagicMock, patch
from Homeworks.Homework_5.part_4 import randomly_assign_discounts, get_bank_with_the_oldest_client, \
    get_debtors_full_name, get_bank_with_the_biggest_capital, get_bank_with_highest_unique_outbound_users, \
    filter_by_datetime_transactions, get_user_last_three_months_transactions


def test_randomly_assign_discounts(magick_cursor):
    random.seed(1)
    magick_cursor.execute.return_value = ((1,), (2,), (3,), (4,), (5,))
    expected = {5: 25, 1: 30, 2: 30}
    actual = randomly_assign_discounts.__wrapped__(magick_cursor)
    assert expected == actual


def test_get_debtors_full_name(magick_cursor):
    magick_cursor.execute.side_effect = [((1,), (2,)),
                                         (('Test_name_1', 'Test_surname_1'),),
                                         (('Test_name_2', 'Test_surname_2'),)]
    expected = ['Test_name_1 Test_surname_1', 'Test_name_2 Test_surname_2']
    actual = get_debtors_full_name.__wrapped__(magick_cursor)
    assert expected == actual


@patch('Homeworks.Homework_5.part_4.py.get_currency', return_value ={'EUR': 0.9747})
def test_get_bank_with_the_biggest_capital(magick_cursor):
    magick_cursor.fetchall.return_value = [(1, 'EUR', 1), (2, 'EUR', 2)]
    magick_cursor.execute.side_effect = [None, [('Test1',)], [('Test2',)]]
    actual = get_bank_with_the_biggest_capital.__wrapped__(magick_cursor)
    expected = 'Test2'
    assert expected == actual


def test_get_bank_with_the_oldest_client(magick_cursor):
    expected = 'Test'
    magick_cursor.fetchone.side_effect = [(None,), ('Test',)]
    actual = get_bank_with_the_oldest_client.__wrapped__(magick_cursor)
    assert expected == actual


def test_get_bank_with_highest_unique_outbound_users(magick_cursor):
    expected = ('Bank1', 2)
    magick_cursor.execute.return_value = (('Bank1', 1), ('Bank2', 2), ('Bank1', 2))
    actual = get_bank_with_highest_unique_outbound_users.__wrapped__(magick_cursor)
    assert expected == actual


def test_filter_by_datetime_transactions():
    insert_param = (None, None, None, None, None, None, None, '1990-11-21 12:12:12')
    actual = filter_by_datetime_transactions(insert_param)
    assert not actual


def test_get_user_last_three_months_transactions(magick_cursor):
    insert_id = 0
    magick_cursor.execute.return_value = ((None, None, None, None, None, None, None, '2023-08-13 09:57:56'),
                                          (None, None, None, None, None, None, None, '2020-08-13 10:57:56'))
    actual = get_user_last_three_months_transactions.__wrapped__(magick_cursor, insert_id)
    expected = [(None, None, None, None, None, None, None, '2023-08-13 09:57:56')]
    assert expected == actual

