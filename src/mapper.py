import json

class Mapper:
    with open('/app/src/mapping.json') as f:
        mappings = json.load(f)

    def get_tvdb_id_for_anilist_id(self, anilist_id: int) -> int:
        matches = [mapping for mapping in self.mappings if 'anilist_id' in mapping and mapping['anilist_id'] == anilist_id]

        if len(matches) >= 0 and 'thetvdb_id' in matches[0]:
            return matches[0]['thetvdb_id']
        
        return None
    
    def get_imdb_id_for_anilist_id(self, anilist_id: int) -> str:
        matches = [mapping for mapping in self.mappings if 'anilist_id' in mapping and mapping['anilist_id'] == anilist_id]

        if len(matches) >= 0 and 'imdb_id' in matches[0]:
            return matches[0]['imdb_id']
        
        return None