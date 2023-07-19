import requests as re
import csv
import copy

class CinemaUser:
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIzMTI3NGFmYTRlNTUyMjRjYzRlN2Q0NmNlMTNkOTZjOSIsInN1YiI6IjVkNmZhMWZmNzdjMDFmMDAxMDU5NzQ4OSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.lbpgyXlOXwrbY0mUmP-zQpNAMCw_h-oaudAJB6Cn5c8"
    }

    def get_inf_from_desired_pages(self, start, end):
        for i in range(start, end + 1):
            url = f'https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&sort_by=popularity.desc&page={i}'
            response = re.get(url, headers=self.headers)
            print(response.json())

    def get_all_data_from_page(self, page_numb):
        url = f'https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&sort_by=popularity.desc&page={page_numb}'
        response = re.get(url, headers=self.headers)
        print(f'Get: {response}\nJson: {response.json()}\nHeaders: {response.headers}\nText: {response.text}\nContent: {response.content}')

    def get_data_about_movies(self, start, end, step, page):
        url = f'https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&sort_by=popularity.desc&page={page}'
        response = re.get(url, headers=self.headers)
        information = response.json()
        for i in range(start, end + 1, step):
            films = information['results']
            print(films[i]['original_title'])

    def get_the_most_popular_movie(self):
        url = f'https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&sort_by=popularity.desc&page={1}'
        response = re.get(url, headers=self.headers)
        information = response.json()
        the_most_popular_movie_popularity = information['results'][0]['popularity']
        the_most_popular_movie_title = information['results'][0]['original_title']
        for movie in information['results']:
            if movie['popularity'] > the_most_popular_movie_popularity:
                the_most_popular_movie_popularity = movie['popularity']
                the_most_popular_movie_title = movie['original_title']
        print(the_most_popular_movie_title)

    def find_movie(self, find_text):
        url = f'https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&sort_by=popularity.desc&page={1}'
        response = re.get(url, headers=self.headers)
        information = response.json()
        for film in information['results']:
            if film['overview'].find(find_text) > 0:
                print(film['original_title'])

    def print_genres(self):
        genre_url = 'https://api.themoviedb.org/3/genre/movie/list?language=en'
        genre_response = re.get(genre_url, headers=self.headers)
        genre_information = genre_response.json()
        print(genre_information['genres'])

    def delete_movies_with_genre(self, deleted_genre):
        url = f'https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&sort_by=popularity.desc&page={1}'
        response = re.get(url, headers=self.headers)
        information = response.json()
        movies = information['results']
        k = 0
        for i in movies:
            for genre in movies[k]['genre_ids']:
                if genre == deleted_genre:
                    movies.pop(k)
            k += 1
        for film in information['results']:
            print(film['original_title'])

# ERRRRRRRRRRRRRRRROOOOOOOOOORRRRRR
    # def get_most_popular_genre(self):
    #     url = f'https://https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&sort_by=popularity.desc&page={1}'
    #     response = re.get(url, headers=self.headers)
    #     information = response.json()
    #
    #     genre_url = 'https://api.themoviedb.org/3/genre/movie/list?language=en'
    #     genre_response = re.get(genre_url, headers=self.headers)
    #     genre_information = genre_response.json()
    #
    #     genre_popularity = []
    #     print(genre_popularity)


    def group_movies(self, common_genre):
        url = f'https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&sort_by=popularity.desc&page={1}'
        response = re.get(url, headers=self.headers)
        information = response.json()
        movies = information['results']
        k = 0
        common_movies = []
        for i in movies:
            for genre in movies[k]['genre_ids']:
                if genre == common_genre:
                    common_movies.append(movies[k]['original_title'])
            k += 1
        print(common_movies)

    def replace_genre(self):
        url = f'https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&sort_by=popularity.desc&page={1}'
        response = re.get(url, headers=self.headers)
        information = response.json()
        movies = information['results']
        movies_copy = copy.deepcopy(movies)
        print(f'Default data:{movies}')
        for i in range(len(movies_copy)):
            movies_copy[i]['genre_ids'][0] = 22
        print(f'Changed data:{movies_copy}')

    def print_collection_of_structures(self):
        url = f'https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&sort_by=popularity.desc&page={1}'
        response = re.get(url, headers=self.headers)
        information = response.json()
        movies = information['results']
        collection_of_structures = []
        for i in range(len(movies)):
            example = {'Title': '',
                       'Popularity': 0,
                       'Score': 0,
                       'Last_day_in_cinema': ''}
            example['Title'] = movies[i]['original_title']
            example['Popularity'] = round(movies[i]['popularity'], 1)
            example['Score'] = int(movies[i]['vote_average'])
            tmp = movies[i]['release_date']
#           Converting date
            tmp_list = tmp.split('-')
            for m in range(len(tmp_list)):
                tmp_list[m] = int(tmp_list[m])
            tmp_list[1] += 2
            tmp_list[2] += 14
            while True:
                while True:
                    if tmp_list[2] > 31:
                        tmp_list[1] += 1
                        tmp_list[2] -= 31
                    else:
                        break
                if tmp_list[1] > 12:
                    tmp_list[0] += 1
                    tmp_list[1] -= 12
                else:
                    break
            for m in range(len(tmp_list)):
                tmp_list[m] = str(tmp_list[m])
            tmp = "-".join(tmp_list)
#           Converting data
            example['Last_day_in_cinema'] = tmp
            collection_of_structures.append(example)
        for element in collection_of_structures:
            print(element)

        return collection_of_structures


user = CinemaUser()

print('Task 1:')
user.get_inf_from_desired_pages(1, 3)

print('\nTask 2:')
user.get_all_data_from_page(3)

print('\nTask 3:')
user.get_data_about_movies(3, 19, 4, 1)

print('\nTask 4:')
user.get_the_most_popular_movie()

print('\nTask 5:')
user.find_movie('human')

print('\nTask 6:')
user.print_genres()

print('\nTask 7:')
user.delete_movies_with_genre(28)

print('\nTask 8:')
# user.get_most_popular_genre()

print('\nTask 9:')
user.group_movies(16)

print('\nTask 10:')
user.replace_genre()

print('\nTask 11:')
data = user.print_collection_of_structures()

print('\nTask 12:')
# file_path = 'D:/'
# with open(file_path, 'w', newline='') as csv_file:
#     writer = csv.writer(csv_file)
#     writer.writerow(['Data'])
#     writer.writerows(data)
