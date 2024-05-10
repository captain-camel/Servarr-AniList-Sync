# Servarr AniList Sync

A python script to **automatically sync your AniList anime list to Sonarr and Radarr.** *Servarr AniList Sync* will periodically grab media from your anime list based on criteria you specify, and add it to Sonarr or Radarr.

## Usage

*Servarr AniList Sync* can sync anime from your list based on status (planning, watching, etc...) and/or from a custom list.

The script will attempt to add anime by its TVDB or IMDB ID, and will fall back to searching by title if an ID is not found.

### Status

Pass a comma separated list of the statuses you would like to sync as the `ANILIST_STATUSES` parameter. Whenever a sync is executed, anime with any of these statuses will be synced.

See [the AniList docs](https://anilist.github.io/ApiV2-GraphQL-Docs/) for which statuses can be specified.

### Custom List

Specify a custom list which should be synced to your server using the `ANILIST_CUSTOM_LIST` parameter.

### What determines where an anime is added?

Whether anime is treated as a series and added to Sonarr, or as a movie and added to Radarr, is determined by the number of episodes (1 -> Radarr, more than 1 -> Sonarr), rather than the format reported by AniList. This is because AniList labels some multi-episodes series as movies (eg. [Memories](https://anilist.co/anime/1462/MEMORIES)), and those are better handled by Sonarr.

If you would like fine-grained control over which application an anime is added to, use the `ANILIST_CUSTOM_LIST_SONARR` and `ANILIST_CUSTOM_LIST_RADARR` parameters. When an anime is synced for any reason, its presence on these lists determines which app it should be added to. If it is on neither, the app will be decided automatically like normal. (Note that solely adding an anime to one of these lists will not cause it to be synced. A sync must be triggered by its status or presence on `ANILIST_CUSTOM_LIST`.)

## Installation

#### docker compose

```yaml
services:
  servarr_anilist_sync:
    image: captaincamel/servarr_anilist_sync
    container_name: servarr_anilist_sync
    environment:
      - CRON_SCHEDULE=*/30 * * * *
      - SONARR_URL=http://sonarr:8989/
      - RADARR_URL=http://radarr:7878/
      - SONARR_API_KEY=
      - RADARR_API_KEY=
      - ANILIST_USERNAME=
      - ANILIST_STATUSES=CURRENT,PLANNING
      - ANILIST_CUSTOM_LIST=
      - SONARR_QUALITY_PROFILE=
      - RADARR_QUALITY_PROFILE=
      - SONARR_ROOT_FOLDER=
      - RADARR_ROOT_FOLDER=
      - SONARR_AUTO_SEARCH=true
      - RADARR_AUTO_SEARCH=true
    restart: unless-stopped
```

#### docker cli

```sh
docker run -d \
  --name servarr_anilist_sync \
  -e CRON_SCHEDULE=*/30 * * * * \
  -e SONARR_URL=http://sonarr:8989/ \
  -e RADARR_URL=http://radarr:7878/ \
  -e SONARR_API_KEY= \
  -e RADARR_API_KEY= \
  -e ANILIST_USERNAME= \
  -e ANILIST_STATUSES=CURRENT,PLANNING \
  -e ANILIST_CUSTOM_LIST= \
  -e SONARR_QUALITY_PROFILE= \
  -e RADARR_QUALITY_PROFILE= \
  -e SONARR_ROOT_FOLDER= \
  -e RADARR_ROOT_FOLDER= \
  -e SONARR_AUTO_SEARCH=true \
  -e RADARR_AUTO_SEARCH=true \
  --restart unless-stopped \
  captaincamel/servarr_anilist_sync
```

#### Other

The docker image uses `cron` to run the script periodically. To use it outside of Docker, you will have to set up scheduling yourself. The script itself is contained in the  `/src` directory, so that is all you will need. Remember to pass in parameters through the environment.

### Parameters

All parameters are passed as environment variables. No ports or volumes are necessary.

| Parameter                    | Function                                                                                                                         |
|------------------------------|----------------------------------------------------------------------------------------------------------------------------------|
| `CRON_SCHEDULE`              | Determines when and how often `cron` runs the script (see [here](https://www.ibm.com/docs/en/db2oc?topic=task-unix-cron-format)) |
| `SONARR_URL`                 | Sonarr server URL                                                                                                                |
| `RADARR_URL`                 | Radarr server URL                                                                                                                |
| `SONARR_API_KEY`             | Sonarr API key (from Sonarr general settings)                                                                                    |
| `RADARR_API_KEY`             | Radarr API key (from Radarr general settings)                                                                                    |
| `ANILIST_USERNAME`           | Your AniList username                                                                                                            |
| `ANILIST_STATUSES`           | A comma separated list of AniList statuses which should be synced **(optional)**                                                 |
| `ANILIST_CUSTOM_LIST`        | The AniList custom list to sync with Sonarr or Radarr **(optional)**                                                             |
| `ANILIST_CUSTOM_LIST_SONARR` | The AniList custom list to sync with only Sonarr **(optional)**                                                                  |
| `ANILIST_CUSTOM_LIST_RADARR` | The AniList custom list to sync with only Radarr **(optional)**                                                                  |
| `SONARR_QUALITY_PROFILE`     | The name of the quality profile to use when adding series to Sonarr                                                              |
| `RADARR_QUALITY_PROFILE`     | The name of the quality profile to use when adding movies to Radarr                                                              |
| `SONARR_ROOT_FOLDER`         | The folder which series added to Sonarr will be placed in                                                                        |
| `RADARR_ROOT_FOLDER`         | The folder which series added to Radarr will be placed in                                                                        |
| `SONARR_AUTO_SEARCH`         | Whether Sonarr should automatically begin searching for added series                                                             |
| `RADARR_AUTO_SEARCH`         | Whether Radarr should automatically begin searching for added movies                                                             |

## Credits

Anime mapping is from <https://github.com/Fribb/anime-lists>.