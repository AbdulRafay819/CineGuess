import json
import os

import requests

# TMDB API Setup
TMDB_API_KEY = os.getenv("API_KEY")
BASE_URL = "https://api.themoviedb.org/3"

# Base class for data fetching
class DataFetcher:
    def __init__(self, api_key, base_url):
        self.api_key = api_key
        self.base_url = base_url

    def fetch(self, url):
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error fetching data: {response.status_code}")
            return None

# MovieFetcher class that inherits from DataFetcher
class MovieFetcher(DataFetcher):
    def __init__(self, api_key, base_url):
        super().__init__(api_key, base_url)
        self.genres = self.fetch_genres()

    def fetch_movies(self):
        url = f"{self.base_url}/discover/movie?api_key={self.api_key}&sort_by=popularity.desc"
        response = self.fetch(url)
        if response:
            movies = response['results']
            movie_data = []
            for movie in movies:
                movie_data.append({
                    'title': movie['title'],
                    'genre_ids': movie['genre_ids'],  # Genres are represented as IDs
                    'release_date': movie['release_date'],
                    'vote_average': movie['vote_average'],  # Popularity score
                    'id': movie['id']
                })
            return movie_data
        return []

    def fetch_genres(self):
        url = f"{self.base_url}/genre/movie/list?api_key={self.api_key}"
        response = self.fetch(url)
        if response:
            genres = response['genres']
            return {genre['id']: genre['name'] for genre in genres}
        return {}

    def fetch_cast(self, movie_id):
        url = f"{self.base_url}/movie/{movie_id}/credits?api_key={self.api_key}"
        response = self.fetch(url)
        if response:
            cast = response.get('cast', [])
            return [actor['name'] for actor in cast[:3]]  # Top 3 actors
        return []

    def fetch_movies_data_with_details(self, pages):
      
        detailed_movies = []

        for page in range(1, pages + 1):  # Fetch movies from multiple pages
            url = f"{self.base_url}/discover/movie?api_key={self.api_key}&sort_by=popularity.desc&page={page}"
            response = self.fetch(url)
            if response:
                movies = response['results']
                for movie in movies:
                    cast = self.fetch_cast(movie['id'])
                    release_year = movie['release_date'].split('-')[0] if movie.get('release_date') else "Unknown"
                    detailed_movies.append({
                        'title': movie['title'],
                        'genre': [self.genres[gid] for gid in movie['genre_ids'] if gid in self.genres],
                        'release_year': release_year,
                        'actors': cast,
                        'vote_average': movie['vote_average']
                    })
            else:
                print(f"Error fetching movies on page {page}.")
                break  # Stop fetching if an error occurs

        return detailed_movies

# Save data to a JSON file
def save_to_json(data, filename="movies.json"):
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)

# Load data from a JSON file
def load_from_json(filename="movies.json"):
    try:
        with open(filename, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

# Main Function
if __name__ == "__main__":

    movie_fetcher = MovieFetcher(TMDB_API_KEY, BASE_URL)


    print("Fetching movie data...")
    detailed_movies = movie_fetcher.fetch_movies_data_with_details(pages=30)
    print(f"Fetched {len(detailed_movies)} movies.")

    # Save to a JSON file
    save_to_json(detailed_movies, "movies.json")

    # Load from the JSON file
    loaded_movies = load_from_json("movies.json")
    print(f"Loaded {len(loaded_movies)} movies from JSON.")