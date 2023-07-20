import requests as re
import csv
import copy
from collections import Counter
import time as t
from datetime import timedelta, date

class CinemaUser:
    HEADERS = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIzMTI3NGFmYTRlNTUyMjRjYzRlN2Q0NmNlMTNkOTZjOSIsInN1YiI6IjVkNmZhMWZmNzdjMDFmMDAxMDU5NzQ4OSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.lbpgyXlOXwrbY0mUmP-zQpNAMCw_h-oaudAJB6Cn5c8"
    }

    def __init__(self, number):
        self.data = []
        self.collection_of_structures = []
        self.fetch_data_from_desired_pages(number)

    def get_response(self, number):
        url = f'https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&sort_by=popularity.desc&page={number}'
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
        necessary_movies = [film['original_title'] for film in self.data if film['overview'].find(find_text) > 0]
        return necessary_movies

    def print_genres(self):
        genre_list = set(genre for film in self.data for genre in film['genre_ids'])
        return genre_list

    def delete_movies_with_genre(self, deleted_genre):
        return [film['original_title'] for film in self.data if deleted_genre not in film['genre_ids']]

    def get_most_popular_genre(self):
        genres_popularity = [genre for film in self.data for genre in film['genre_ids']]
        return Counter(genres_popularity).most_common(1)[0][0]

    def group_movies(self):
        common_movies = [{film['original_title'], movie['original_title']} for i, film in enumerate(self.data) for genre in film['genre_ids'] for movie in self.data[i+1::] if genre in movie['genre_ids']]
        # I left it here because the top line is a little bit too long, but it is written in one line :)
        #
        # for i, film in enumerate(self.data):
        #     for genre in film['genre_ids']:
        #         for movie in self.data[i+1::]:
        #             if genre in movie['genre_ids']:
        #                 common_movies.append({film['original_title'], movie['original_title']})
        return common_movies

    def replace_genre(self):
        movies_copy = copy.deepcopy(self.data)
        print(f'Default data:{self.data}')
        movies_copy = list(map(change_genre_id, movies_copy))
        print(f'Changed data:{movies_copy}')

    def print_collection_of_structures(self):
        for film in self.data:
            example = {'Title': '',
                       'Popularity': 0,
                       'Score': 0,
                       'Last_day_in_cinema': ''}
            example['Title'] = film['original_title']
            example['Popularity'] = round(film['popularity'], 1)
            example['Score'] = int(film['vote_average'])
            date_str = film['release_date'].split('-')
            date_int = [int(element) for element in date_str]
            release_date = date(date_int[0], date_int[1], date_int[2]) + timedelta(weeks=6, days=2)
            example['Last_day_in_cinema'] = release_date.strftime('%Y-%m-%d')
            self.collection_of_structures.append(example)
        return self.collection_of_structures

    def write_collection_to_file(self, path):
        with open(path, 'w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(['Data'])
            writer.writerows(data)


def change_genre_id(movie):
    movie['genre_ids'][0] = 22
    return movie

print('Task 1:')
user = CinemaUser(1)

print('\nTask 2:')
user.get_all_data_from_page()

print('\nTask 3:')
print(user.get_data_about_movies(3, 19, 4))

print('\nTask 4:')
print(user.get_the_most_popular_movie())

print('\nTask 5:')
print(user.find_movie('human'))

print('\nTask 6:')
print(user.print_genres())

print('\nTask 7:')
print(user.delete_movies_with_genre(28))

print('\nTask 8:')
print(user.get_most_popular_genre())

print('\nTask 9:')
print(user.group_movies())

print('\nTask 10:')
user.replace_genre()

print('\nTask 11:')
data = user.print_collection_of_structures()
for movie in data:
    print(movie)

print('\nTask 12:')
user.write_collection_to_file('C:/file.csv')
