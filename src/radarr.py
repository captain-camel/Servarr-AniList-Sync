import requests
import os
from urllib.parse import urljoin

class Radarr:
    def __init__(self, url, api_key):
        self.base_url = urljoin(url, 'api/v3/')
        self.api_key = api_key

    def lookup_by_title(self, term: str) -> dict:
        params = {
            'term': term
        }

        headers = {
            'X-Api-Key': self.api_key
        }

        movies = requests.get(urljoin(self.base_url, "movie/lookup"), params=params, headers=headers).json()

        if len(movies) == 0:
            return None
        
        return movies[0]
    
    def lookup_by_imdb_id(self, id: str) -> dict:
        params = {
            'imdbId': id
        }

        headers = {
            'X-Api-Key': self.api_key
        }

        movie = requests.get(urljoin(self.base_url, "movie/lookup/imdb"), params=params, headers=headers).json()

        # Make sure we got a movie and not an error
        if 'message' and 'description' in movie:
            return None
        else:
            return movie


    def add(self, movie: dict, quality_profile_id: int, root_folder_path: str):
        headers = {
            'X-Api-Key': self.api_key
        }

        movie.update({
            'rootFolderPath': root_folder_path,
            'qualityProfileId': quality_profile_id,
            "monitored": True,
            'addOptions': {
                'ignoreEpisodesWithFiles': True,
                'ignoreEpisodesWithoutFiles': True,
                'monitor': 'movieOnly',
                'searchForMovie': True
            },
        })

        requests.post(urljoin(self.base_url, "movie"), json=movie, headers=headers)

    def movie_is_in_db(self, tmdb_id: int):
        params = {
            'tmdbId': tmdb_id
        }

        headers = {
            'X-Api-Key': self.api_key
        }

        movies = requests.get(urljoin(self.base_url, "movie"), params=params, headers=headers).json()

        if len(movies) == 0:
            return False

        return 'id' in movies[0]
    
    def get_quality_profile_id_for_name(self, name: str) -> int:
        headers = {
            'X-Api-Key': self.api_key
        }

        quality_profiles = requests.get(urljoin(self.base_url, 'qualityprofile'), headers=headers).json()

        matches = [profile for profile in quality_profiles if 'name' in profile and profile['name'] == name]

        if len(matches) >= 0 and 'id' in matches[0]:
            return matches[0]['id']
        
        return None