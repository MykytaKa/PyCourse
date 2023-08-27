import pytest
from Homeworks.Homework_5.transfers_script import modify_data, add_data, parse_user_full_name, add_data_from_csv, \
    delete_data, transfer_money, make_approved_transfer, convert_money
from unittest.mock import MagicMock, call, mock_open, patch
from Homeworks.Homework_5.constants import UPDATE_COMMAND

TEST_DATA = [(1, 2),
             (3, 4)]
TEST_MESSAGE = 'Test message'


def test_modify_data(magick_cursor):
    actual_message = modify_data(magick_cursor, TEST_DATA, 'Test_table', 'param_1, param_2', TEST_MESSAGE, MagicMock())
    magick_cursor.execute.assert_called_once_with('UPDATE Test_table SET param_2 = ? WHERE param_1 = ?', TEST_DATA)
    assert TEST_MESSAGE == actual_message


def test_add_data(magick_cursor):
    actual_message = add_data(magick_cursor, TEST_DATA, 'Test_table', 'param1, param2', TEST_MESSAGE, MagicMock())
    magick_calls = [call.execute('INSERT INTO Test_table (param1, param2) VALUES (?,?)', TEST_DATA[0]),
                    call.execute('INSERT INTO Test_table (param1, param2) VALUES (?,?)', TEST_DATA[1])]
    assert magick_cursor.mock_calls == magick_calls
    assert TEST_MESSAGE == actual_message


def test_parse_user_full_name():
    expected = [('Test1', 'Test1', 1), ('Test2', 'Test2', 2)]
    input_param = [('Test1 Test1', 1), ('Test2 Test2', 2)]
    actual = parse_user_full_name(input_param)
    assert expected == actual


@patch('Homeworks.Homework_5.transfers_script.add_data')
@patch('builtins.open', new_callable=mock_open(read_data='param1, param2\ndata1, data2\ndata3, data4\n'))
def test_add_data_from_csv(mock_file, magick_cursor):
    actual_message = add_data_from_csv(magick_cursor, 'Test_path', 'Test_table',
                                       'param1, param2', TEST_MESSAGE, MagicMock())
    assert TEST_MESSAGE == actual_message


def test_delete_data(magick_cursor):
    actual_message = delete_data(magick_cursor, 1, 'Test_table', 'param1, param2', TEST_MESSAGE)
    magick_cursor.execute.assert_called_once_with('DELETE FROM Test_table WHERE param1, param2 = 1')
    assert TEST_MESSAGE == actual_message


def mock_convert(param1, param2, param3, param4):
    return param4


@patch('Homeworks.Homework_5.transfers_script.make_approved_transfer',
       return_value='Money transfer completed successfully.')
@patch('Homeworks.Homework_5.transfers_script.convert_money', return_value=mock_convert)
@pytest.mark.parametrize('money_amount, necessary_calls, expected_message',
                         [
                             (200, False, 'The sender does not have enough money'),
                             (1, True, 'Money transfer completed successfully.')
                         ])
def test_transfer_money(mock_cur, mock_conv, magick_cursor, money_amount, necessary_calls, expected_message):
    magick_cursor.fetchone.side_effect = [(100, 'USD')]
    actual_message = transfer_money.__wrapped__(magick_cursor, 1, 2, money_amount)
    assert mock_cur.called == necessary_calls
    assert mock_conv.called == necessary_calls
    assert expected_message == actual_message


@patch('Homeworks.Homework_5.utils.get_currency', return_value={'USD': 1})
def test_convert_money(mock_cur, magick_cursor):
    expected = 100
    magick_cursor.fetchone.return_value = 'USD'
    actual = convert_money(magick_cursor, 'USD', 1, 100)
    assert expected == actual


def test_make_approved_transfer(magick_cursor):
    actual_message = make_approved_transfer(magick_cursor, 100, 99, 1, 2, 'USD', '12-03-2004 12:12:12')
    magick_cursor.assert_has_calls([
        call.execute(UPDATE_COMMAND.format('-', 100, 2)),
        call.execute(UPDATE_COMMAND.format('+', 99, 1))
    ], any_order=True)
    assert 'Money transfer completed successfully.' == actual_message
