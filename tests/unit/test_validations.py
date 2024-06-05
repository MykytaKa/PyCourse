import pytest
from unittest.mock import MagicMock, patch

import Homeworks.Homework_5.validations
from Homeworks.Homework_5.validations import check_objects_instance, validate_account_number, validate_user_data, validate_account_data


INVALID_TEST_DATA = ['True', '1']
TEST_OBJECT_INFO = {0: (int, 'Test'), 1: (str, 'Test')}


def test_check_objects_instance():
    with pytest.raises(ValueError):
        check_objects_instance(TEST_OBJECT_INFO, INVALID_TEST_DATA)


def test_validate_account_number():
    with pytest.raises(ValueError):
        validate_account_number('ID--h4-5265d234-h1')


@patch('Homeworks.Homework_5.validations.check_objects_instance')
@patch('Homeworks.Homework_5.validations.validate_account_number')
def test_validate_user_data(mock_check, mock_vld_ac):
    with pytest.raises(ValueError):
        validate_user_data(['Test', 'Test', '12-03-200', 'Test'])


@patch('Homeworks.Homework_5.utils.get_currency')
@patch('Homeworks.Homework_5.validations.check_objects_instance')
def test_validate_account_data(mock_cur, mock_check):
    with pytest.raises(ValueError):
        validate_user_data(['Test'])
