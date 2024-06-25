import pandas as pd
from tqdm import tqdm
from scripts import ClassManager
from scripts import CSV_to_DF
import matplotlib.pyplot as plt
import time


# alphanumerical = 1
# timestamp = 2
# time = 3
# date = 4
# numerical = 5

# All the tagset types
tagset_types = {
    "track_name": 1,
    "album_name": 1,
    "artist_infos": 1,
    "track_duration": 5,
    "track_popularity": 5,
    # "happiness_percentage": 5,
    # "sadness_percentage": 5,
    # "anger_percentage": 5,
    # "fear_percentage": 5,
    "emotion": 1,
    "genre": 1,
    "genre_2": 1,
    "genre_3": 1
}

numerical_tagset_types = {
    "track_duration": 5,
    "track_popularity": 5
    # "happiness_percentage": 5,
    # "sadness_percentage": 5,
    # "anger_percentage": 5,
    # "fear_percentage": 5,
}

alphanumerical_tagset_types = {
    "track_name": 1,
    "album_name": 1,
    "artist_infos": 1,
    "emotion": 1,
    "genre": 1,
    "genre_2": 1,
    "genre_3": 1
}

# Define duration ranges and corresponding tags
duration_ranges = {
    "veryshort": (0, 20),
    "short": (21, 90),
    "medium": (91, 300),
    "long": (301, 600),
    "verylong": (601, 1200),
    "extralong": (1201, float('inf'))
}

def get_duration_tag(duration):
    for tag, (low, high) in duration_ranges.items():
        if low <= duration <= high:
            return tag
    return None

# Define popularity ranges and corresponding tags
popularity_ranges = {
    "veryunpopular": (0, 5),
    "unpopular": (6, 10),
    "mediumpopular": (11, 25),
    "popular": (26, 50),
    "verypopular": (51, 75),
    "extrapopular": (76, 100)
}

def get_popularity_tag(popularity):
    for tag, (low, high) in popularity_ranges.items():
        if low <= popularity <= high:
            return tag
    return None



def parse_data(path: str):
    """
    Description: This function reads the data from the CSV file and creates tagsets and tags for each row.

    Arguments:
    ----------------
    Path: The path to the CSV file.

    Returns:
    ----------------
    tag_manager: The tag manager object that contains the tagsets, tags, and medias.
    """
    # Clean the data and convert it to a DataFrame
    df = CSV_to_DF(path)
    tag_manager = ClassManager()

    # Create tagsets
    for name, type in tagset_types.items():
        tag_manager.get_or_create_tagset_id(name, type)

    start_time = time.time()
    times = []
    rows_processed = []
    
    # Add tags to tagsets with progress bar
    for i, row in tqdm(df.iterrows(), total=len(df), desc="Processing rows", unit="row"):
        file_uri = f"https://open.spotify.com/track/{row['uri']}"
        tags = set()
        for name in alphanumerical_tagset_types.keys():
            tag_value = row[name]
            if pd.notna(tag_value):
                tag_id, new_id = tag_manager.get_or_create_tag_id(tag_value, name)
                # If the tag is new, add it to the tagset
                if new_id:
                    tagset_id = tag_manager.get_or_create_tagset_id(name, 1)
                    tag = {"id": tag_id, "value": tag_value}
                    tag_manager.add_tag_to_tagset(tagset_id, tag)
                tags.add(tag_id)
        for name in numerical_tagset_types.keys():
            tag_value = row[name]
            if pd.notna(tag_value):
                if name == "track_duration":
                    # Get a specific name depending on the value of the track duration
                    duration_tag = get_duration_tag(tag_value)
                    if duration_tag:
                        tag_id, new_id = tag_manager.get_or_create_tag_id(duration_tag, name)
                        if new_id:
                            tagset_id = tag_manager.get_or_create_tagset_id(name, 5)
                            tag = {"id": tag_id, "value": duration_tag}
                            tag_manager.add_tag_to_tagset(tagset_id, tag)
                        tags.add(tag_id)
                if name == "track_popularity":
                    # Get a specific name depending on the value of the track popularity
                    popularity_tag = get_popularity_tag(tag_value)
                    if popularity_tag:
                        tag_id, new_id = tag_manager.get_or_create_tag_id(popularity_tag, name)
                        if new_id:
                            tagset_id = tag_manager.get_or_create_tagset_id(name, 5)
                            tag = {"id": tag_id, "value": popularity_tag}
                            tag_manager.add_tag_to_tagset(tagset_id, tag)
                        tags.add(tag_id)
                
        # Add the media to the tag manager
        tag_manager.add_media(file_uri, list(tags))

        if i % 100 == 0:  # Record every 100 rows
            current_time = time.time()
            times.append(current_time - start_time)
            rows_processed.append(i + 1)
    
    # Plotting the results
    plt.figure(figsize=(10, 6))
    plt.plot(times, rows_processed, label='Rows Processed')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Rows Processed')
    plt.title('Rows Processed Over Time')
    plt.legend()
    plt.grid(True)  

    # Save the plot figure
    plt.savefig('../build/rows_processed_over_time_50k.png')

    return tag_manager
