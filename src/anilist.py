import requests

class Anilist:
    baseUrl = 'https://graphql.anilist.co'

    def get_media_list(self, username: str) -> list:
        query = '''
        query ($page: Int, $perPage: Int, $userName: String) {
            Page (page: $page, perPage: $perPage) {
                pageInfo {
                    total
                    currentPage
                    lastPage
                    hasNextPage
                    perPage
                }
                mediaList (userName: $userName, type: ANIME) {
                    id
                    media {
                        id
                        title {
                            romaji
                            english
                            native
                            userPreferred
                        }
                        episodes
                        status(version: 2)
                    }
                    status
                    customLists
                }
            }
        }
        '''

        variables = {
            'page': 1,
            'perPage': 50,
            'userName': username
        }

        media_list = []

        while True:
            data = requests.post(self.baseUrl, json={'query': query, 'variables': variables}).json()['data']

            media_list.extend(data['Page']['mediaList'])

            if not data['Page']['pageInfo']['hasNextPage']:
                break
            
            variables['page'] += 1
            
        return media_list