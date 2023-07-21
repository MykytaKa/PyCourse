import requests as re
import csv
import copy
from collections import Counter
import time as t
from datetime import timedelta, date, datetime


class CinemaUser:
    HEADERS = {
        'accept': 'application/json',
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIzMTI3NGFmYTRlNTUyMjRjYzRlN2Q0NmNlMTNkOTZjOSIsInN1YiI6IjVkNmZhMWZmNzdjMDFmMDAxMDU5NzQ4OSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.lbpgyXlOXwrbY0mUmP-zQpNAMCw_h-oaudAJB6Cn5c8'
    }

    def __init__(self, number_of_pages):
        self.data = []
        self.collection_of_structures = []
        self.fetch_data_from_desired_pages(number_of_pages)

    def get_response(self, number_of_page):
        url = f'https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&sort_by=popularity.desc&page={number_of_page}'
        return re.get(url, headers=self.HEADERS)

    def fetch_data_from_desired_pages(self, end):
        for i in range(1, end + 1):
            response = self.get_response(i)
            self.data.extend(response.json()['results'])

    def get_all_data_from_page(self):
        return self.data

    def get_data_about_movies(self, start, end, step):
        return self.data[start:end:step]

    def get_the_most_popular_movie(self):
        return max(self.data, key=lambda x: x['popularity'])['original_title']

    def find_movie(self, find_text):
        return [film['original_title'] for film in self.data if find_text in film['overview']]

    def get_present_genres(self):
        return tuple({genre for film in self.data for genre in film['genre_ids']})

    def delete_movies_with_genre(self, deleted_genre):
        return [film['original_title'] for film in self.data if deleted_genre not in film['genre_ids']]

    def get_most_popular_genre(self):
        return Counter([genre for film in self.data for genre in film['genre_ids']]).most_common(1)[0][0]

    def group_movies(self):
        common_movies = [(film['original_title'], movie['original_title'])
                         for i, film in enumerate(self.data)
                         for genre in film['genre_ids']
                         for movie in self.data
                         if genre in movie['genre_ids']]
        return common_movies

    def change_genre_id(self, movie):
        movie['genre_ids'][0] = 22
        return movie

    def get_original_and_copy_data(self):
        return self.data, list(map(self.change_genre_id, copy.deepcopy(self.data)))

    def print_collection_of_structures(self):
        for film in self.data:
            example = {'Title': film['original_title'],
                       'Popularity': round(film['popularity'], 1),
                       'Score': int(film['vote_average']),
                       'Last_day_in_cinema': (datetime.strptime(film['release_date'], "%Y-%m-%d") + timedelta(weeks=10, days=4)).strftime('%Y-%m-%d')}
            self.collection_of_structures.append(example)
        return self.collection_of_structures

    def write_collection_to_file(self, path):
        with open(path, 'w', newline='') as csv_file:
            fieldnames = ['Title', 'Popularity', 'Score', 'Last_day_in_cinema']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            for film in self.collection_of_structures:
                writer.writerow(film)


print('Task 1:')
user = CinemaUser(1)

print('\nTask 2:')
print(user.get_all_data_from_page())

print('\nTask 3:')
print(user.get_data_about_movies(3, 19, 4))

print('\nTask 4:')
print(user.get_the_most_popular_movie())

print('\nTask 5:')
print(user.find_movie('human'))

print('\nTask 6:')
print(user.get_present_genres())

print('\nTask 7:')
print(user.delete_movies_with_genre(28))

print('\nTask 8:')
print(user.get_most_popular_genre())

print('\nTask 9:')
print(user.group_movies())

print('\nTask 10:')
print(f'{user.get_original_and_copy_data()[0]}\n{user.get_original_and_copy_data()[1]}')

print('\nTask 11:')
data = user.print_collection_of_structures()
for movie in data:
    print(movie)

print('\nTask 12:')
user.write_collection_to_file('file.csv')
