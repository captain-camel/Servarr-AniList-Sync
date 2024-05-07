import requests
import os
from urllib.parse import urljoin

class Sonarr:
    def __init__(self, url, api_key):
        self.base_url = urljoin(url, 'api/v3/')
        self.api_key = api_key

    def lookup(self, term: str) -> dict:
        params = {
            'term': term
        }

        headers = {
            'X-Api-Key': self.api_key
        }

        series = requests.get(urljoin(self.base_url, "series/lookup"), params=params, headers=headers).json()

        if len(series) == 0:
            return None
        
        return series[0]

    def add(self, series: dict, quality_profile_id: int, root_folder_path: str):
        headers = {
            'X-Api-Key': self.api_key
        }

        series.update({
            'rootFolderPath': root_folder_path,
            'qualityProfileId': quality_profile_id,
            'seriesType': 'anime',
            'addOptions': {
                'ignoreEpisodesWithFiles': True,
                'ignoreEpisodesWithoutFiles': False,
                'searchForMissingEpisodes': os.environ['SONARR_AUTO_SEARCH'] == "true",
                'searchForCutoffUnmetEpisodes': False,
            },
        })

        requests.post(urljoin(self.base_url, "series"), json=series, headers=headers)
    
    def get_quality_profile_id_for_name(self, name: str) -> int:
        headers = {
            'X-Api-Key': self.api_key
        }

        quality_profiles = requests.get(urljoin(self.base_url, 'qualityprofile'), headers=headers).json()

        matches = [profile for profile in quality_profiles if 'name' in profile and profile['name'] == name]

        if len(matches) >= 0 and 'id' in matches[0]:
            return matches[0]['id']
        
        return None