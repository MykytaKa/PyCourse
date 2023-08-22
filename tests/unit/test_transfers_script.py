import pytest
from Homeworks.Homework_5.transfers_script import modify_data, add_data, \
    parse_user_full_name, add_data_from_csv, delete_data, transfer_money, make_approved_transfer
from unittest.mock import MagicMock, call, mock_open, patch
from Homeworks.Homework_5.utils import UPDATE_COMMAND, SELECT_COMMAND

TEST_DATA = [(1, 2),
             (3, 4)]
TEST_MESSAGE = 'Test message'


def test_modify_data(magick_cursor):
    actual_message = modify_data(magick_cursor, TEST_DATA, 'Test_table', 'param_1, param_2', TEST_MESSAGE, MagicMock())
    magick_cursor.execute.assert_called_once_with(f'UPDATE Test_table SET param_2 = ? WHERE param_1 = ?', TEST_DATA)
    assert TEST_MESSAGE == actual_message


def test_add_data(magick_cursor):
    actual_message = add_data(magick_cursor, TEST_DATA, 'Test_table', 'param1, param2', TEST_MESSAGE, MagicMock())
    magick_calls = [call.execute(f'INSERT INTO Test_table (param1, param2) VALUES (?,?)', TEST_DATA[0]),
                    call.execute(f'INSERT INTO Test_table (param1, param2) VALUES (?,?)', TEST_DATA[1])]
    assert magick_cursor.mock_calls == magick_calls
    assert TEST_MESSAGE == actual_message


def test_parse_user_full_name():
    expected = [('Test1', 'Test1', 1), ('Test2', 'Test2', 2)]
    input_param = [('Test1 Test1', 1), ('Test2 Test2', 2)]
    actual = parse_user_full_name(input_param)
    assert expected == actual


@patch('builtins.open', new_callable=mock_open(read_data='param1, param2\ndata1, data2\ndata3, data4\n'))
def test_add_data_from_csv(mock_file, magick_cursor):
    actual_message = add_data_from_csv(magick_cursor, 'Test_path', 'Test_table',
                                       'param1, param2', TEST_MESSAGE, MagicMock())
    assert TEST_MESSAGE == actual_message


def test_delete_data(magick_cursor):
    actual_message = delete_data(magick_cursor, 1, 'Test_table', 'param1, param2', TEST_MESSAGE)
    magick_cursor.execute.assert_called_once_with('DELETE FROM Test_table WHERE param1, param2 = 1')
    assert TEST_MESSAGE == actual_message


@patch('Homeworks.Homework_5.transfers_script.make_approved_transfer',
       return_value='Money transfer completed successfully.')
@pytest.mark.parametrize('money_amount, calls_amount, expected_message',
                         [
                             (200, 2, 'Money transfer completed successfully.'),
                             (1, 0, 'The sender does not have enough money')
                         ])
def test_transfer_money(money_amount, calls_amount, expected_message, magick_cursor):
    magick_cursor.fetchone.side_effect = [(100, 'USD'), ['USD']]
    actual_message = transfer_money.__wrapped__(magick_cursor, 1, 2, money_amount)
    assert calls_amount == len(magick_cursor.fetchone.mock_calls)
    assert expected_message == actual_message


def test_make_approved_transfer(magick_cursor):
    actual_message = make_approved_transfer(magick_cursor, 100, 99, 1, 2, 'USD')
    magick_cursor.assert_has_calls([
        call.cursor.execute(UPDATE_COMMAND.format('+', 99, 1)),
        call.execute(UPDATE_COMMAND.format('-', 100, 2))
    ])
    assert 'Money transfer completed successfully.' == actual_message
