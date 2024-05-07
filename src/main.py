from sonarr import Sonarr
from radarr import Radarr
from anilist import Anilist
from mapper import Mapper
import os

# TODO: Sync servarr -> anilist

if __name__ == '__main__':
    print("Beginning sync")

    sonarr_url = os.environ['SONARR_URL']
    radarr_url = os.environ['RADARR_URL']

    sonarr_api_key = os.environ['SONARR_API_KEY']
    radarr_api_key = os.environ['RADARR_API_KEY']

    anilist_username = os.environ['ANILIST_USERNAME']

    anilist_custom_list = os.environ['ANILIST_CUSTOM_LIST']

    sonarr_quality_profile_name = os.environ['SONARR_QUALITY_PROFILE']
    radarr_quality_profile_name = os.environ['RADARR_QUALITY_PROFILE']

    sonarr_root_folder_path = os.environ['SONARR_ROOT_FOLDER']
    radarr_root_folder_path = os.environ['RADARR_ROOT_FOLDER']

    sonarr = Sonarr(sonarr_url, sonarr_api_key)
    radarr = Radarr(radarr_url, radarr_api_key)
    anilist = Anilist()
    mapper = Mapper()

    media_list = anilist.get_media_list(anilist_username)

    sonarr_quality_profile_id = sonarr.get_quality_profile_id_for_name(sonarr_quality_profile_name)
    radarr_quality_profile_id = radarr.get_quality_profile_id_for_name(radarr_quality_profile_name)

    def media_predicate(media: dict) -> bool:
        in_custom_list = anilist_custom_list in media['customLists'] and media['customLists'][anilist_custom_list]
        current = media['status'] == 'CURRENT'
        released = media['media']['status'] != 'NOT_YET_RELEASED'

        return (in_custom_list or current) and released
    
    media_list_filtered = filter(media_predicate, media_list)

    for media in media_list_filtered:
        english_title = media['media']['title']['english']

        if media['media']['episodes'] > 1:
            # Series
            tvdb_id = mapper.get_tvdb_id_for_anilist_id(media['media']['id'])

            if not tvdb_id is None:
                series = sonarr.lookup('tvdb:' + str(tvdb_id))
            else:
                series = sonarr.lookup(english_title)

            if series is None:
                print(f"Failed to find series \"{english_title}\" on Sonarr")
                continue

            if 'id' in series:
                continue

            sonarr.add(series, quality_profile_id=sonarr_quality_profile_id, root_folder_path=sonarr_root_folder_path)
            print(f"Series \"{english_title}\" added to Sonarr")

        else:
            # Movie
            imdb_id = mapper.get_imdb_id_for_anilist_id(media['media']['id'])

            if not imdb_id is None:
                movie = radarr.lookup_by_imdb_id(imdb_id)
            else:
                movie = radarr.lookup_by_title(english_title)

            if movie is None:
                print(f"Failed to find movie \"{english_title}\" on Radarr")
                continue

            if 'tmdbId' in movie and radarr.movie_is_in_db(movie['tmdbId']):
                continue

            radarr.add(movie, quality_profile_id=radarr_quality_profile_id, root_folder_path=radarr_root_folder_path)
            print(f"Movie \"{english_title}\" added to Radarr")