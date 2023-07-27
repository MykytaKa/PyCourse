import argparse as argp
import csv
import requests as re
import logging
import os
from datetime import datetime
from pytz import timezone
from timezonefinder import TimezoneFinder
from geopy.geocoders import Nominatim
from collections import Counter
import shutil
import zipfile


def download_csv_file():
    """
    Download data from web randomuser using requests lib
    :return: string-type data in csv format
    """
    url = 'https://randomuser.me/api/?results=50&format=csv'
    response = re.get(url)
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
    dict_data = []
    with open(csv_file_path, 'r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            dict_data.append(row)
    return dict_data


def filter_data(csv_data, filtering):
    """
    Filter data using match cases
    :param csv_data: str, data which has to be filtered
    :param filtering: list, list with information about filtering
                      where the first value is a type of filtering: gender or number;
                      the second value is a gender by which the data has to be filtered;
                      the third value is ф number of rows to be filtered
    :return: list, filtered data
    """
    match filtering[0]:
        case 'gender':
            return list(filter(lambda row: row['gender'] == filtering[1], csv_data))
        case 'number':
            return csv_data[:filtering[2]]
        case _:
            return csv_data


def add_new_fields(csv_data):
    """
    Add new fields and change others in the data using match
    cases and timezonefinder, geopy.geocoders, pytz, datetime libs
    :param csv_data: list, data to which new fields will be added and others will be changed
    :return: list, data with added and changed values
    """
    for i, user_info in enumerate(csv_data):
        # ADDING FIELD 'global_index'
        user_info['global_index'] = i + 1

        # ADDING FIELD 'current_time'
        obj = TimezoneFinder()
        geolocator = Nominatim(user_agent="geoapiExercises")
        location = geolocator.geocode(f'{user_info["location.city"]}')
        latitude = location.latitude
        longitude = location.longitude
        obj.timezone_at(lat=latitude, lng=longitude)
        now_utc = datetime.now(timezone('UTC'))
        user_time = now_utc.astimezone(timezone(obj.timezone_at(lat=location.latitude, lng=location.longitude)))
        user_info['current_time'] = user_time.strftime('%Y-%m-%d %H:%M:%S')

        # CHANGING VALUES IN FIELD 'name.title'
        match user_info['name.title']:
            case 'Mrs':
                user_info['name.title'] = 'missis'
            case 'Ms':
                user_info['name.title'] = 'miss'
            case 'Mr':
                user_info['name.title'] = 'mister'
            case 'Madame':
                user_info['name.title'] = 'mademoiselle'

        # CHANGING VALUES IN FIELD 'dob.date'
        user_info['dob.date'] = datetime.strptime(user_info['dob.date'],
                                                  '%Y-%m-%dT%H:%M:%S.%fZ').strftime('%m/%d/%Y')

        # CHANGING VALUES IN FIELD 'register.date'
        user_info['registered.date'] = datetime.strptime(user_info['registered.date'],
                                                         '%Y-%m-%dT%H:%M:%S.%fZ').strftime('%m-%d-%Y, %H:%M:%S')
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


def rearrange_data(old_csv_data):
    """
    Rearrange data into format 'decades : {countries : [users_data]}'
    :param old_csv_data: list, data from the csv file in the old format
    :return: dict, data which was rearranged from list format to the dict format
    """
    new_data = {}
    for row in old_csv_data:
        decade = row['dob.date'][-2] + '0-th'
        country = row['location.country']
        if decade not in new_data:
            new_data[decade] = {}
        if country not in new_data[decade]:
            new_data[decade][country] = []
        new_data[decade][country].append(row)
    return new_data


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
            users_age = [int(user["dob.age"]) for user in rearranged_data[decade][country]]
            users_registered_age = [int(user["registered.age"]) for user in rearranged_data[decade][country]]
            users_id_name = [user["id.name"] for user in rearranged_data[decade][country]]
            csv_file_name = f'{max(users_age)}_' \
                            f'{sum(users_registered_age)/len(users_registered_age)}_' \
                            f'{Counter(users_id_name).most_common(1)[0][0]}'
            csv_file_path = os.path.join(country_path, csv_file_name)
            with open(csv_file_path + '.csv', 'w', newline='', encoding='utf-8') as csv_file:
                csv_writer = csv.DictWriter(csv_file, rearranged_data[decade][country][0].keys())
                csv_writer.writeheader()
                csv_writer.writerows(rearranged_data[decade][country])


if __name__ == "__main__":
    # PARSE COMMAND-LINE ARGUMENTS
    parser = argp.ArgumentParser()

    parser.add_argument('--destination_folder', help='path to the folder where the output file will be placed',
                        required=True)
    parser.add_argument('--filename', default='output', help='name of the output file')
    parser.add_argument('--filtering', help='data filtering method')
    parser.add_argument('--gender', default=None, help='filter the data by gender')
    parser.add_argument('--number_of_rows', default=None, type=int, help='filter the data by the number of rows')
    parser.add_argument('--log_level', help='log level')

    args = parser.parse_args()

    # LOGGING CONFIGURATION
    open('log.txt', 'w')
    logging.basicConfig(filename='log.txt',
                        level=args.log_level.upper(),
                        format='%(asctime)s:%(levelname)s:%(name)s:%(message)s')

    # DOWNLOADING CSV FILE DATA
    data = download_csv_file()
    logging.info('CSV file was successfully downloaded')

    # CREATING CSV FILE
    open(args.filename + '.csv', 'w')
    logging.info(f'File {args.filename}.csv was successfully created')

    # WRITING DATA TO CSV FILE
    write_data_to_csv(csv_data=data,
                      csv_file_path=args.filename + '.csv')
    logging.info('Data was successfully writen to the csv file')

    # READING DATA FROM CSV FILE
    data_dict = read_data_from_csv_file(csv_file_path=args.filename + '.csv')

    # FILTERING INPUT DATA
    data_dict = filter_data(csv_data=data_dict, filtering=[args.filtering, args.gender, args.number_of_rows])
    logging.info(f'Data was successfully filtered by {args.filtering}')

    # ADDING NEW FIELDS TO DATA
    data_dict = add_new_fields(data_dict)
    logging.info('New fields were successfully added to the data')
    write_new_data_to_csv(csv_path=args.filename + '.csv', csv_data=data_dict)

    # CREATING DESTINATION FOLDER IF NOT EXIST
    if not os.path.exists(args.destination_folder):
        os.makedirs(args.destination_folder)
        logging.info(f'Directory {args.destination_folder} was successfully created')

    # CHANGING WORK DIRECTORY
    old_work_directory = os.getcwd()
    os.chdir(args.destination_folder)
    new_work_directory = args.destination_folder
    logging.info('Work directory was successfully changed')

    # MOVING SCV FILE TO DESTINATION FOLDER
    os.rename(f'{old_work_directory}/{args.filename}.csv',
              new_work_directory + args.filename + '.csv')
    logging.info(f'File {args.filename}.csv was successfully moved into folder {args.destination_folder}')

    # REARRANGING THE DATA
    data_dict = rearrange_data(data_dict)
    logging.info('Data was successfully rearranged')

    # CREATING SUB FOLDERS
    create_sub_folders(data_dict)
    logging.info('Sub folders were successfully created')

    # REMOVING THE DATA BEFORE 60-TH
    decades = list(os.walk('.'))[0][1]
    for dec in decades:
        if int(dec[0]) < 6 and int(dec[0]) != 0:
            shutil.rmtree(f'{os.getcwd()}/{dec}')
    logging.info('Data before 60-th was successfully removed')

    # LOGGING THE FOLDER STRUCTURE
    logging.info('Data structure:')
    for root, dirs, files in os.walk(args.destination_folder):
        level = root.replace(args.destination_folder, '').count(os.sep)
        indent = ' ' * 4 * level
        logging.info(f"{indent}{os.path.basename(root)}/")
        sub_indent = ' ' * 4 * (level + 1)
        for f in files:
            logging.info(f"{sub_indent}{f} (file)")
        for d in dirs:
            logging.info(f"{sub_indent}{d} (folder)")

    # ARCHIVING DESTINATION FOLDER
    destination_folder_name = args.destination_folder.split('/')[-2]
    archive_name = f"{destination_folder_name}.zip"
    with zipfile.ZipFile(archive_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for folder_name, _, files in os.walk(args.destination_folder):
            for file in files:
                if file.endswith('.csv'):
                    file_path = os.path.join(folder_name, file)
                    zipf.write(file_path, os.path.relpath(file_path, args.destination_folder))
    logging.info(f"Destination folder has been archived to {archive_name}")
