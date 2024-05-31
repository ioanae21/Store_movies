'''Module which contains the class that fetches data about movies. This will be used for the recommendation page.'''
import requests
import json
import time
from configparser import ConfigParser

reader = ConfigParser()
reader.read('config.ini')


class MovieFinder:
    def __init__(self):
        self._headers = {
        "X-RapidAPI-Key": reader['API_DATA']['KEY'],
        "X-RapidAPI-Host": "moviesminidatabase.p.rapidapi.com"

        }

    def search_func(self, title):
        '''The movie search function. Searches a movie with the given title and returns a JSON which has it's ID.'''

        data = requests.get('https://moviesminidatabase.p.rapidapi.com/movie/imdb_id/byTitle/{}/'.format(title), headers = self._headers)
        return data.json()

    def filter_genre(self, genre = 'Action'):
        '''Filters by genre of the movie'''
        data = requests.get('https://moviesminidatabase.p.rapidapi.com/movie/byGen/{}/'.format(genre), headers = self._headers)
        return data.json()
    
    def filter_year(self, year):
        '''Filters by the release year'''
        data = requests.get('https://moviesminidatabase.p.rapidapi.com/movie/byYear/{}/'.format(year), headers = self._headers)
        return data.json()
    
    
    def parse_moviedata(self, data):
        '''The main method which is used to parse the movies, it utilized their IDs to do so.'''

        finalized_movies = []
        for movie in data['results']:
            movie_data = requests.get('https://moviesminidatabase.p.rapidapi.com/movie/id/{}/'.format(movie['imdb_id']), headers = self._headers).json()
            movie_title = movie_data['results']['title']
            movie_rating = movie_data['results']['rating']
            release_date = movie_data['results']['release']
            finalized_movies.append([movie_title, movie_rating, release_date])

        return finalized_movies

