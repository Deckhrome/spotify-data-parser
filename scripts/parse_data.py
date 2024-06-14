import pandas as pd
from tqdm import tqdm
from scripts import ClassManager
from scripts import CSV_to_DF

tagset_types = {
    "sp_track_name": 1,
    "sp_track_duration": 5,
    "sp_track_popularity": 5,
    "sp_album_name": 1,
    "sp_artist_infos": 1,
    "happiness_percentage": 5,
    "sadness_percentage": 5,
    "anger_percentage": 5,
    "fear_percentage": 5,
    "genre_1": 1,
    "genre_2": 1,
    "genre_3": 1
}

def parse_data(path):
    df = CSV_to_DF(path)
    tag_manager = ClassManager()

    # Create tagsets
    for name, type in tagset_types.items():
        tag_manager.get_or_create_tagset_id(name, type)
    
    # Add tags to tagsets with progress bar
    for _, row in tqdm(df.iterrows(), total=len(df), desc="Processing rows", unit="row"):
        file_uri = f"https://open.spotify.com/track/{row['sp_uri']}"
        tags = []
        for name in tagset_types.keys():
            tag_value = row[name]
            if pd.notna(tag_value):
                tag_id = tag_manager.get_or_create_tag_id(tag_value, name)
                tagset_id = tag_manager.get_or_create_tagset_id(name, tagset_types[name])
                tag = {"id": tag_id, "value": tag_value}
                tag_manager.add_tag_to_tagset(tagset_id, tag)
                tags.append(tag_id)
        
        # Eliminate any duplicate tags
        tags = list(set(tags))
        
        # Add the media to the tag manager
        tag_manager.add_media(file_uri, tags)
    
    return tag_manager
