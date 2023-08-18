from Homeworks.Homework_5.transfers_script import modify_data, add_data, \
    parse_user_full_name, add_data_from_csv, delete_data, transfer_money
from unittest.mock import MagicMock

MAGICK_CURSOR = MagicMock()
TEST_DATA = [(1, 2),
             (3, 4)]
TEST_MESSAGE = 'Test message'


def test_modify_data():
    actual_message = modify_data(MAGICK_CURSOR, TEST_DATA, 'Test_table', 'param_1, param_2', TEST_MESSAGE, MagicMock())
    MAGICK_CURSOR.execute.assert_called_once_with(f'UPDATE Test_table SET param_2 = ? WHERE param_1 = ?', TEST_DATA)
    assert TEST_MESSAGE == actual_message


def test_add_data():
    actual_message = add_data(MAGICK_CURSOR, TEST_DATA, 'Test_table', 'param1, param2', TEST_MESSAGE, MagicMock())
    MAGICK_CURSOR.execute.assert_called_once_with(
        (f'INSERT INTO Test_table (param1, param2) VALUES (?,?)', TEST_DATA[0]),
        (f'INSERT INTO Test_table (param1, param2) VALUES (?,?)', TEST_DATA[1]))
    assert TEST_MESSAGE == actual_message


def test_parse_user_full_name():
    expected = [('Test1', 'Test1', 1), ('Test2', 'Test2', 2)]
    input_param = [('Test1 Test1', 1), ('Test2 Test2', 2)]
    actual = parse_user_full_name(input_param)
    assert expected == actual


def test_add_data_from_csv():
    actual_message = add_data_from_csv(MAGICK_CURSOR, 'Test_path', 'Test_table',
                                       'param1, param2', TEST_MESSAGE, MagicMock())
    MAGICK_CURSOR.execute.assert_called_once_with(
        (f'INSERT INTO Test_table (param1, param2) VALUES (?,?)', TEST_DATA[0]),
        (f'INSERT INTO Test_table (param1, param2) VALUES (?,?)', TEST_DATA[1]))
    assert TEST_MESSAGE == actual_message


def test_delete_data():
    actual_message = delete_data(MAGICK_CURSOR, 1, 'Test_table', 'param1, param2', TEST_MESSAGE)
    MAGICK_CURSOR.execute.assert_called_once_with(f'DELETE FROM Test_table WHERE param1, param2 = 1')
    assert TEST_MESSAGE == actual_message


def test_transfer_money():
    actual_message = transfer_money.__wrapped__(MAGICK_CURSOR, (1, 2, 100))
    MAGICK_CURSOR.fetchone.side_effect = [(100, 'USD'), 'USD', 1, 2, 'Test_bank1', 'Test-bank2']
    MAGICK_CURSOR.execute.assert_called_once_with('UPDATE Account SET Amount = Amount + 100 WHERE Id = 2',
                                                  'UPDATE Account SET Amount = Amount - 100 WHERE Id = 1')
    assert TEST_MESSAGE == actual_message
