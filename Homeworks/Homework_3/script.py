import argparse as argp
import csv
import requests as re
import logging
import os
from datetime import datetime, timedelta, timezone
from collections import Counter
import shutil

URL = 'https://randomuser.me/api/?results=100&format=csv&seed=mykyta'


def fetch_csv_file():
    """
    Download data from web randomuser using requests lib

    :return: string-type data in csv format
    """
    response = re.get(URL)
    return response.text


def write_data_to_csv(csv_data, csv_file_path):
    """
    Write data to csv file using csv lib

    :param csv_data: str, data that was downloaded and converted into csv format
    :param csv_file_path: str, path to the folder where the csv file is located
    """
    with open(csv_file_path, 'w', encoding='utf-8') as csv_file:
        csv_file.write(csv_data)


def read_data_from_csv_file(csv_file_path):
    """
    Read data from csv file and write it to variable using csv lib

    :param csv_file_path: str, path to the folder where the csv file is located
    :return: list, data that was read from the csv file
    """
    with open(csv_file_path, 'r', encoding='utf-8') as csv_file:
        return list(csv.DictReader(csv_file))


def filter_data(csv_data, filtering_gender, filtering_number_of_rows):
    """
    Filter data using match cases

    :param csv_data: str, data which has to be filtered
    :param filtering_gender: str, a gender by which the data has to be filtered
    :param filtering_number_of_rows: int, a number of rows to be filtered
    :return: list, filtered data
    """
    if filtering_gender is not None:
        return list(filter(lambda row: row['gender'] == filtering_gender, csv_data))
    elif filtering_number_of_rows is not None:
        return csv_data[:filtering_number_of_rows]
    else:
        return csv_data


def rearrange_datetime_data(user_datetime_data, string_format):
    """
    Reformat the value of a user field to another format

    :param user_datetime_data: str, the value of the field to be reformatted
    :param string_format: str, preferred format of value
    :return:
    """
    return datetime.strptime(user_datetime_data, '%Y-%m-%dT%H:%M:%S.%fZ').strftime(string_format)


def rearrange_name_data(user_name_title):
    """
    Change form of the user's name prefix based on their current value

    :param user_name_title: str, current form of the name prefix
    :return: str, changed form of the name prefix
    """
    match user_name_title:
        case 'Mrs':
            return 'missis'
        case 'Ms':
            return 'miss'
        case 'Mr':
            return 'mister'
        case 'Madame':
            return 'mademoiselle'


def rearrange_user_time_data(user_timezone_offset):
    """
    Calculates the user's time based on their time zone

    :param user_timezone_offset: str, current user timezone offset
    :return: str, current user time
    """
    user_timezone = user_timezone_offset.split(':')
    hours = int(user_timezone[0])
    minutes = int(user_timezone[1])
    return (datetime.now(timezone.utc) + timedelta(hours=hours, minutes=minutes)).strftime('%Y-%m-%d %H:%M:%S')


def add_new_fields(csv_data):
    """
    Add new fields and change others in the data using match cases and datetime libs

    :param csv_data: list, data to which new fields will be added and others will be changed
    :return: list, data with added and changed values
    """
    for i, user_info in enumerate(csv_data, start=1):
        user_info['global_index'] = i
        user_info['current_time'] = rearrange_user_time_data(user_info['location.timezone.offset'])
        user_info['name.title'] = rearrange_name_data(user_info['name.title'])
        user_info['dob.date'] = rearrange_datetime_data(user_datetime_data=user_info['dob.date'],
                                                        string_format='%m/%d/%Y')
        user_info['registered.date'] = rearrange_datetime_data(user_datetime_data=user_info['registered.date'],
                                                               string_format='%m-%d-%Y, %H:%M:%S')
    return csv_data


def write_new_data_to_csv(csv_path, csv_data):
    """
    Write updated data to csv file using csv lib

    :param csv_path: str, path to the folder where the csv file is located
    :param csv_data: list, data which has to be written to the csv file
    """
    with open(csv_path, 'w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=csv_data[0].keys())
        csv_writer.writeheader()
        csv_writer.writerows(csv_data)


def create_folder_if_not_exist(destination_folder_path):
    """
    Create a folder at the given destination path if it does not exist already.

    :param destination_folder_path: str, the path where the folder needs to be created.
    """
    if not os.path.exists(destination_folder_path):
        os.makedirs(destination_folder_path)
        logging.info(f'Directory {destination_folder_path} was successfully created')


def rearrange_data(old_csv_data):
    """
    Rearrange data into format 'decades : {countries : [users_data]}'

    :param old_csv_data: list, data from the csv file in the old format
    :return: dict, data which was rearranged from list format to the dict format
    """
    new_data = {}
    for row in old_csv_data:
        decade = f'{row["dob.date"][-2]}0-th'
        country = row['location.country']
        new_data.setdefault(decade, {})
        new_data[decade].setdefault(country, [])
        new_data[decade][country].append(row)
    return new_data


def create_file_name(rearranged_data, folder_decade, folder_country):
    """
    Create a specific name for the CSV file based on user's maximum age, average number of years of registration,
    and the most common id.name.

    :param rearranged_data: list, containing all data about users, organized by decade and country.
    :param folder_decade: str, the name of the folder representing the decade.
    :param folder_country: str, the name of the folder representing the country.
    :return: str, the name of the CSV file based on the provided data.
    """

    users_data = [(int(user['dob.age']), int(user['registered.age']), user['id.name']) for user in
                  rearranged_data[folder_decade][folder_country]]

    return f'{max(users_data, key=lambda user_info: user_info[0])[0]}_' \
           f'{sum([element[1] for element in users_data]) / len(users_data)}_' \
           f'{Counter([element[2] for element in users_data]).most_common(1)[0][0]}'


def create_sub_folders(rearranged_data):
    """
    Create folders with csv files based on the new data format

    :param rearranged_data: dict, data on the structure of which
                            folders are created and csv files into folders are filled
    """
    for decade in rearranged_data:
        decade_path = os.path.join(os.getcwd(), decade)
        os.makedirs(decade_path)
        for country in rearranged_data[decade]:
            country_path = os.path.join(decade_path, country)
            os.makedirs(country_path)

            csv_file_name = create_file_name(rearranged_data, decade, country)
            csv_file_path = os.path.join(country_path, csv_file_name)
            write_new_data_to_csv(csv_path=csv_file_path + '.csv', csv_data=rearranged_data[decade][country])


def remove_data_before_60_th():
    """
    In destination folder delete folders with users which were born before 1960-th
    """
    for dec in os.listdir(os.getcwd()):
        if dec[0] < '6' and dec[0] != '0':
            shutil.rmtree(os.path.join(os.getcwd(), dec))


def log_folder_structure(destination_folder, user_logger):
    """
    Log the data structure that is in destination folder

    :param destination_folder: str, path to destination folder
    :param user_logger: Logger, a custom logger that allows you to record logged information
    """
    for root, dirs, files in os.walk(destination_folder):
        level = root.replace(destination_folder, '').count(os.sep)
        indent = ' ' * 4 * level
        user_logger.info(f'{indent}{os.path.basename(root)}/')
        sub_indent = ' ' * 4 * (level + 1)
        for f in files:
            user_logger.info(f'{sub_indent}{f} (file)')
        for d in dirs:
            user_logger.info(f'{sub_indent}{d} (folder)')


def archive_destination_folder(destination_folder_name):
    """
    Archive destination folder into zip archive

    :param destination_folder_name: str, name of destination folder
    """
    shutil.make_archive(destination_folder_name, 'zip')


def parse_command_line():
    parser = argp.ArgumentParser()

    parser.add_argument('--destination_folder', help='path to the folder where the output file will be placed',
                        required=True)
    parser.add_argument('filename', default='output', help='name of the output file')

    group = parser.add_mutually_exclusive_group()

    group.add_argument('--gender', default=None, help='filter the data by gender')
    group.add_argument('--number_of_rows', default=None, type=int, help='filter the data by the number of rows')

    parser.add_argument('log_level', help='log level')

    return parser.parse_args()


def set_logger(logging_level):
    logging.basicConfig(filename='log.txt',
                        level=logging_level.upper(),
                        format='%(asctime)s:%(levelname)s:%(name)s:%(message)s')
    return logging.getLogger('my_logger')


def main():
    # PARSE COMMAND-LINE ARGUMENTS
    args = parse_command_line()

    file_name = args.filename + '.csv'

    # LOGGING CONFIGURATION
    logger = set_logger(args.log_level)

    # DOWNLOADING CSV FILE DATA
    data = fetch_csv_file()
    logger.info('CSV file was successfully downloaded')

    # WRITING DATA TO CSV FILE
    write_data_to_csv(csv_data=data,
                      csv_file_path=file_name)
    logger.info('Data was successfully writen to the csv file')

    # READING DATA FROM CSV FILE
    data_dict = read_data_from_csv_file(csv_file_path=file_name)
    logger.info('Data was successfully read from csv file')

    # FILTERING INPUT DATA
    data_dict = filter_data(csv_data=data_dict, filtering_gender=args.gender,
                            filtering_number_of_rows=args.number_of_rows)
    logger.info(f'Data was successfully filtered')

    # ADDING NEW FIELDS TO DATA
    data_dict = add_new_fields(data_dict)
    logger.info('New fields were successfully added to the data')
    write_new_data_to_csv(csv_path=file_name, csv_data=data_dict)

    # CREATING DESTINATION FOLDER IF NOT EXIST
    create_folder_if_not_exist(args.destination_folder)

    # CHANGING WORK DIRECTORY
    old_work_directory = os.getcwd()
    os.chdir(args.destination_folder)
    logger.info('Work directory was successfully changed')

    # MOVING CSV FILE TO DESTINATION FOLDER
    os.rename(os.path.join(old_work_directory, file_name), os.path.join(args.destination_folder, file_name))
    logger.info(f'File {file_name}.csv was successfully moved into folder {args.destination_folder}')

    # REARRANGING THE DATA
    data_dict = rearrange_data(data_dict)
    logger.info('Data was successfully rearranged')

    # CREATING SUB FOLDERS
    create_sub_folders(data_dict)
    logger.info('Sub folders were successfully created')

    # REMOVING THE DATA BEFORE 60-TH
    remove_data_before_60_th()
    logger.info('Data before 60-th was successfully removed')

    # LOGGING THE FOLDER STRUCTURE
    logger.info('Data structure:')
    log_folder_structure(args.destination_folder, logger)

    # ARCHIVING DESTINATION FOLDER
    archive_destination_folder(args.destination_folder.split('/')[-2])
    logger.info(f'Destination folder has been archived to {args.destination_folder.split("/")[-2]}', )


if __name__ == '__main__':
    main()
