import pandas as pd
from SpotifyDataParser.spotify_data_parser.ClassManager import ClassManager
from SpotifyDataParser.spotify_data_parser.clean_CSV import CSV_to_DF

tagset_types = {
    "sp_track_name": 1,
    "sp_track_duration": 5,
    "sp_track_popularity": 5,
    "sp_album_name": 1,
    "sp_artist_infos": 1,
    "x": 5,
    "y": 5,
    "z": 5,
    "color": 1,
    "happiness_percentage": 5,
    "sadness_percentage": 5,
    "anger_percentage": 5,
    "fear_percentage": 5,
    "emotion_code": 1,
    "genre_1": 1,
    "genre_2": 1,
    "genre_3": 1
}

def parse_data(path):
    df = CSV_to_DF(path)
    tag_manager = ClassManager()
    for name, type in tagset_types.items():
        tag_manager.get_or_create_tagset_id(name, type)
    
    for _, row in df.iterrows():
        file_uri = f"https://open.spotify.com/track/{row['sp_uri']}"
        tags = []
        for name in tagset_types.keys():
            tag_value = row[name]
            if pd.notna(tag_value):
                tag_id = tag_manager.get_or_create_tag_id(tag_value)
                tagset_id = tag_manager.get_or_create_tagset_id(name, tagset_types[name])
                tag = {"id": tag_id, "value": tag_value}
                tag_manager.add_tag_to_tagset(tagset_id, tag)
                tags.append(tag_id)
        
        tag_manager.add_media(file_uri, tags)
    
    return tag_manager
