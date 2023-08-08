import pytest
from unittest.mock import MagicMock, patch

from Homeworks.Homework_3.script import filter_data, add_new_fields, rearrange_name_data

INPUT_DATA_BEFORE_FILTERING = [{'gender': 'female', 'name.title': 'Mrs', 'name.first': 'Minttu', 'name.last': 'Kalm',
                                'location.street.number': '3773', 'location.street.name': 'Tahmelantie',
                                'location.city': 'Järvenpää', 'location.state': 'Central Ostrobothnia',
                                'location.country': 'Finland', 'location.postcode': '40431',
                                'location.coordinates.latitude': '-29.8722',
                                'location.coordinates.longitude': '145.1505',
                                'location.timezone.offset': '-7:00',
                                'location.timezone.description': 'Mountain Time (US & Canada)',
                                'email': 'minttu.kalm@example.com',
                                'login.uuid': '94626d30-56ab-407c-8fd2-9d214678ed77',
                                'login.username': 'blacklion871', 'login.password': 'slinky', 'login.salt': 'xNSdEVU8',
                                'login.md5': 'e559f0593c4a851cd9c0cfa9231f2bd6',
                                'login.sha1': 'd1b8f8ff97e963b040954262ef22b956a9ae6458',
                                'login.sha256': '7899ee1225921866b1a9fe24e5df2c2b8e2cb1178dcd278652a4a52703db487d',
                                'dob.date': '1954-02-02T17:14:59.158Z', 'dob.age': '69',
                                'registered.date': '2004-01-09T12:57:26.703Z', 'registered.age': '19',
                                'phone': '05-459-844', 'cell': '045-027-35-92', 'id.name': 'HETU',
                                'id.value': 'NaNNA174undefined',
                                'picture.large': 'https://randomuser.me/api/portraits/women/29.jpg',
                                'picture.medium': 'https://randomuser.me/api/portraits/med/women/29.jpg',
                                'picture.thumbnail': 'https://randomuser.me/api/portraits/thumb/women/29.jpg',
                                'nat': 'FI'}]

EXPECTED_DATA_AFTER_FILTERING_BY_ROWS = [
    {'gender': 'female', 'name.title': 'Mrs', 'name.first': 'Minttu', 'name.last': 'Kalm',
     'location.street.number': '3773', 'location.street.name': 'Tahmelantie',
     'location.city': 'Järvenpää', 'location.state': 'Central Ostrobothnia',
     'location.country': 'Finland', 'location.postcode': '40431',
     'location.coordinates.latitude': '-29.8722',
     'location.coordinates.longitude': '145.1505',
     'location.timezone.offset': '-7:00',
     'location.timezone.description': 'Mountain Time (US & Canada)',
     'email': 'minttu.kalm@example.com',
     'login.uuid': '94626d30-56ab-407c-8fd2-9d214678ed77',
     'login.username': 'blacklion871', 'login.password': 'slinky', 'login.salt': 'xNSdEVU8',
     'login.md5': 'e559f0593c4a851cd9c0cfa9231f2bd6',
     'login.sha1': 'd1b8f8ff97e963b040954262ef22b956a9ae6458',
     'login.sha256': '7899ee1225921866b1a9fe24e5df2c2b8e2cb1178dcd278652a4a52703db487d',
     'dob.date': '1954-02-02T17:14:59.158Z', 'dob.age': '69',
     'registered.date': '2004-01-09T12:57:26.703Z', 'registered.age': '19',
     'phone': '05-459-844', 'cell': '045-027-35-92', 'id.name': 'HETU',
     'id.value': 'NaNNA174undefined',
     'picture.large': 'https://randomuser.me/api/portraits/women/29.jpg',
     'picture.medium': 'https://randomuser.me/api/portraits/med/women/29.jpg',
     'picture.thumbnail': 'https://randomuser.me/api/portraits/thumb/women/29.jpg',
     'nat': 'FI'}]


@pytest.mark.parametrize('input_data, input_filtering_gender, input_filtering_number_of_rows, expected',
                         [(INPUT_DATA_BEFORE_FILTERING, None, 1, EXPECTED_DATA_AFTER_FILTERING_BY_ROWS),
                          (INPUT_DATA_BEFORE_FILTERING, 'male', None, []),
                          (INPUT_DATA_BEFORE_FILTERING, None, None, INPUT_DATA_BEFORE_FILTERING)])
def test_filter_data(input_data, input_filtering_gender, input_filtering_number_of_rows, expected):
    actual = filter_data(input_data, input_filtering_gender, input_filtering_number_of_rows)
    assert actual == expected


@patch('Homeworks.Homework_3.script.rearrange_user_time_data', return_value='2023-07-30 08:37:32')
@patch('Homeworks.Homework_3.script.rearrange_name_data', return_value='missis')
@patch('Homeworks.Homework_3.script.rearrange_datetime_data', side_effect=['02/02/1954', '01-09-2004, 12:57:26'])
def test_add_new_fields(mock1_f, mock2_f, mock3_f):
    input_param = [{'gender': 'female', 'name.title': 'Mrs', 'name.first': 'Minttu',
                    'name.last': 'Kalm', 'location.street.number': '3773', 'location.street.name': 'Tahmelantie',
                    'location.city': 'Järvenpää', 'location.state': 'Central Ostrobothnia',
                    'location.country': 'Finland',
                    'location.postcode': '40431', 'location.coordinates.latitude': '-29.8722',
                    'location.coordinates.longitude': '145.1505',
                    'location.timezone.offset': '-7:00', 'location.timezone.description': 'Mountain Time (US & Canada)',
                    'email': 'minttu.kalm@example.com', 'login.uuid': '94626d30-56ab-407c-8fd2-9d214678ed77',
                    'login.username': 'blacklion871',
                    'login.password': 'slinky', 'login.salt': 'xNSdEVU8',
                    'login.md5': 'e559f0593c4a851cd9c0cfa9231f2bd6',
                    'login.sha1': 'd1b8f8ff97e963b040954262ef22b956a9ae6458',
                    'login.sha256': '7899ee1225921866b1a9fe24e5df2c2b8e2cb1178dcd278652a4a52703db487d',
                    'dob.date': '1954-02-02T17:14:59.158Z', 'dob.age': '69',
                    'registered.date': '2004-01-09T12:57:26.703Z', 'registered.age': '19',
                    'phone': '05-459-844', 'cell': '045-027-35-92', 'id.name': 'HETU',
                    'id.value': 'NaNNA174undefined',
                    'picture.large': 'https://randomuser.me/api/portraits/women/29.jpg',
                    'picture.medium': 'https://randomuser.me/api/portraits/med/women/29.jpg',
                    'picture.thumbnail': 'https://randomuser.me/api/portraits/thumb/women/29.jpg', 'nat': 'FI'}]

    actual = add_new_fields(input_param)

    expected = [{'gender': 'female', 'name.title': 'missis', 'name.first': 'Minttu',
                 'name.last': 'Kalm', 'location.street.number': '3773', 'location.street.name': 'Tahmelantie',
                 'location.city': 'Järvenpää', 'location.state': 'Central Ostrobothnia', 'location.country': 'Finland',
                 'location.postcode': '40431', 'location.coordinates.latitude': '-29.8722',
                 'location.coordinates.longitude': '145.1505', 'location.timezone.offset': '-7:00',
                 'location.timezone.description': 'Mountain Time (US & Canada)', 'email': 'minttu.kalm@example.com',
                 'login.uuid': '94626d30-56ab-407c-8fd2-9d214678ed77', 'login.username': 'blacklion871',
                 'login.password': 'slinky', 'login.salt': 'xNSdEVU8', 'login.md5': 'e559f0593c4a851cd9c0cfa9231f2bd6',
                 'login.sha1': 'd1b8f8ff97e963b040954262ef22b956a9ae6458',
                 'login.sha256': '7899ee1225921866b1a9fe24e5df2c2b8e2cb1178dcd278652a4a52703db487d',
                 'dob.date': '02/02/1954', 'dob.age': '69', 'registered.date': '01-09-2004, 12:57:26',
                 'registered.age': '19', 'phone': '05-459-844', 'cell': '045-027-35-92',
                 'id.name': 'HETU', 'id.value': 'NaNNA174undefined',
                 'picture.large': 'https://randomuser.me/api/portraits/women/29.jpg',
                 'picture.medium': 'https://randomuser.me/api/portraits/med/women/29.jpg',
                 'picture.thumbnail': 'https://randomuser.me/api/portraits/thumb/women/29.jpg',
                 'nat': 'FI', 'global_index': 1, 'current_time': '2023-07-30 08:37:32'}]

    assert actual == expected


@pytest.mark.parametrize('input_param, expected', [('Mrs', 'missis'),
                                                   ('Ms', 'miss'),
                                                   ('Mr', 'mister'),
                                                   ('Madame', 'mademoiselle')])
def test_rearrange_name_data(input_param, expected):
    actual = rearrange_name_data(input_param)
    assert actual == expected
