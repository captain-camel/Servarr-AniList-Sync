from enum import Enum
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

    # These parameters are optional, so we use os.getenv instead of os.environ 
    anilist_statuses = os.getenv('ANILIST_STATUSES')
    anilist_custom_list = os.getenv('ANILIST_CUSTOM_LIST')
    anilist_custom_list_sonarr = os.getenv('ANILIST_CUSTOM_LIST_SONARR')
    anilist_custom_list_radarr = os.getenv('ANILIST_CUSTOM_LIST_RADARR')

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

    def add_anilist_media_to_sonarr(media: dict):
        tvdb_id = mapper.get_tvdb_id_for_anilist_id(media['media']['id'])

        if not tvdb_id is None:
            series = sonarr.lookup('tvdb:' + str(tvdb_id))
        else:
            series = sonarr.lookup(media['media']['title']['english'] or media['media']['title']['romaji'])

        if series is None:
            print(f"Failed to find series \"{media['media']['title']['userPreferred']}\" on Sonarr")
            return

        if 'id' in series:
            return

        sonarr.add(series, quality_profile_id=sonarr_quality_profile_id, root_folder_path=sonarr_root_folder_path)
        print(f"Series \"{media['media']['title']['userPreferred']}\" added to Sonarr")

    def add_anilist_media_to_radarr(media: dict):
        imdb_id = mapper.get_imdb_id_for_anilist_id(media['media']['id'])

        if not imdb_id is None:
            movie = radarr.lookup_by_imdb_id(imdb_id)
        else:
            movie = radarr.lookup_by_title(media['media']['title']['english'] or media['media']['title']['romaji'])

        if movie is None:
            print(f"Failed to find movie \"{media['media']['title']['userPreferred']}\" on Radarr")
            return

        if 'tmdbId' in movie and radarr.movie_is_in_db(movie['tmdbId']):
            return

        radarr.add(movie, quality_profile_id=radarr_quality_profile_id, root_folder_path=radarr_root_folder_path)
        print(f"Movie \"{media['media']['title']['userPreferred']}\" added to Radarr")

    for media in media_list:
        # Ensure episode count is reliable by rejecting unreleased anime
        released = media['media']['status'] != 'NOT_YET_RELEASED'
        matches_status = (media['status'] in [status.strip() for status in anilist_statuses.split(',')]) if anilist_statuses is not None else False
        in_custom_list = (
            anilist_custom_list is not None and
            anilist_custom_list in media['customLists'] and
            media['customLists'][anilist_custom_list]
        )
        in_custom_list_sonarr = (
            anilist_custom_list_sonarr is not None and
            anilist_custom_list_sonarr in media['customLists'] and
            media['customLists'][anilist_custom_list_sonarr]
        )
        in_custom_list_radarr = (
            anilist_custom_list_radarr is not None and
            anilist_custom_list_radarr in media['customLists'] and
            media['customLists'][anilist_custom_list_radarr]
        )

        if not released:
            continue

        if not (matches_status or in_custom_list):
            continue

        did_add = False

        if in_custom_list_sonarr:
            did_add = True
            add_anilist_media_to_sonarr(media)

        if in_custom_list_radarr:
            did_add = True
            add_anilist_media_to_radarr(media)

        if not did_add:
            if media['media']['episodes'] > 1:
                add_anilist_media_to_sonarr(media)
            else:
                add_anilist_media_to_radarr(media)