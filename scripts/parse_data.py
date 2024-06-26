import pandas as pd
from tqdm import tqdm
from scripts import ClassManager, CSV_to_DF
import matplotlib.pyplot as plt
import time

# Define tagset types
TAGSET_TYPES = {
    "track_name": 1,
    "album_name": 1,
    "artist_infos": 1,
    "track_duration": 5,
    "track_popularity": 5,
    "emotion": 1,
    "genre": 1,
    "genre_2": 1,
    "genre_3": 1
}

NUMERICAL_TAGSET_TYPES = {
    "track_duration": 5,
    "track_popularity": 5
}

ALPHANUMERICAL_TAGSET_TYPES = {
    "track_name": 1,
    "album_name": 1,
    "artist_infos": 1,
    "emotion": 1,
    "genre": 1,
    "genre_2": 1,
    "genre_3": 1
}

# Define duration and popularity ranges
DURATION_RANGES = {
    "veryshort": (0, 20),
    "short": (21, 90),
    "medium": (91, 300),
    "long": (301, 600),
    "verylong": (601, 1200),
    "extralong": (1201, float('inf'))
}

POPULARITY_RANGES = {
    "veryunpopular": (0, 5),
    "unpopular": (6, 10),
    "mediumpopular": (11, 25),
    "popular": (26, 50),
    "verypopular": (51, 75),
    "extrapopular": (76, 100)
}

def get_duration_tag(duration):
    for tag, (low, high) in DURATION_RANGES.items():
        if low <= duration <= high:
            return tag
    return None

def get_popularity_tag(popularity):
    for tag, (low, high) in POPULARITY_RANGES.items():
        if low <= popularity <= high:
            return tag
    return None

def parse_data(path: str):
    """
    Description: This function reads the data from the CSV file and creates tagsets and tags for each row.

    Arguments:
    ----------------
    path: The path to the CSV file.

    Returns:
    ----------------
    tag_manager: The tag manager object that contains the tagsets, tags, and medias.
    """
    df = CSV_to_DF(path)
    tag_manager = ClassManager()

    # Create tagsets
    for name, type_ in TAGSET_TYPES.items():
        tag_manager.get_or_create_tagset_id(name, type_)

    start_time = time.time()
    times = []
    rows_processed = []

    # Add tags to tagsets with progress bar
    for i, row in tqdm(df.iterrows(), total=len(df), desc="Processing rows", unit="row"):
        file_uri = f"https://open.spotify.com/track/{row['uri']}"
        tags = set()

        for name in ALPHANUMERICAL_TAGSET_TYPES.keys():
            tag_value = row[name]
            if pd.notna(tag_value):
                tag_id, new_id = tag_manager.get_or_create_tag_id(tag_value, name)
                if new_id:
                    tagset_id = tag_manager.get_or_create_tagset_id(name, 1)
                    tag = {"id": tag_id, "value": tag_value}
                    tag_manager.add_tag_to_tagset(tagset_id, tag)
                tags.add(tag_id)

        for name in NUMERICAL_TAGSET_TYPES.keys():
            tag_value = row[name]
            if pd.notna(tag_value):
                if name == "track_duration":
                    duration_tag = get_duration_tag(tag_value)
                    if duration_tag:
                        tag_id, new_id = tag_manager.get_or_create_tag_id(duration_tag, name)
                        if new_id:
                            tagset_id = tag_manager.get_or_create_tagset_id(name, 5)
                            tag = {"id": tag_id, "value": duration_tag}
                            tag_manager.add_tag_to_tagset(tagset_id, tag)
                        tags.add(tag_id)
                elif name == "track_popularity":
                    popularity_tag = get_popularity_tag(tag_value)
                    if popularity_tag:
                        tag_id, new_id = tag_manager.get_or_create_tag_id(popularity_tag, name)
                        if new_id:
                            tagset_id = tag_manager.get_or_create_tagset_id(name, 5)
                            tag = {"id": tag_id, "value": popularity_tag}
                            tag_manager.add_tag_to_tagset(tagset_id, tag)
                        tags.add(tag_id)

        tag_manager.add_media(file_uri, list(tags))

        if i % 100 == 0:
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
