import pandas as pd
from tqdm import tqdm
from scripts import ClassManager, CSV_to_DF
import matplotlib.pyplot as plt
import time

# tag types
# 1 - alphanumerical
# 2 - Timestamp UTC
# 3 - time
# 4 - date
# 5 - numerical

# Define tagset types
TAGSET_TYPES = {
    # "uri": 1,
    "track_name": 1,
    "album_name": 1,
    "artist_infos": 1,
    "track_duration": 1,
    "track_popularity": 1,
    "emotion": 1,
    "genre": 1,
    "genre_2": 1,
    "genre_3": 1,
    "Timestamp UTC": 2,
}

NUMERICAL_TAGSET_TYPES = {"track_duration": 1, "track_popularity": 1}

ALPHANUMERICAL_TAGSET_TYPES = {
    # "uri": 1,
    "track_name": 1,
    "album_name": 1,
    "artist_infos": 1,
    "emotion": 1,
    "genre": 1,
    "genre_2": 1,
    "genre_3": 1,
    "Timestamp UTC": 2,
}

# Define ranges for duration and popularity
RANGES = {
    "track_duration": {
        "veryshort": (0, 20),
        "short": (21, 90),
        "medium": (91, 300),
        "long": (301, 600),
        "verylong": (601, 1200),
        "extralong": (1201, float("inf")),
    },
    "track_popularity": {
        "veryunpopular": (0, 5),
        "unpopular": (6, 10),
        "mediumpopular": (11, 25),
        "popular": (26, 50),
        "verypopular": (51, 75),
        "extrapopular": (76, 100),
    },
}


def get_tag(value, ranges):
    for tag, (low, high) in ranges.items():
        if low <= value <= high:
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
        thumbnail = f"{row['image_uri']}.jpg"
        file_uri = f"{row['uri']}"
        tags = set()
        # Process alphanumerical tags
        for name in ALPHANUMERICAL_TAGSET_TYPES.keys():
            tag_value = row[name]
            if pd.notna(tag_value):
                tag_id, new_id = tag_manager.get_or_create_tag_id(tag_value, name)
                if new_id:
                    tagset_id = tag_manager.get_or_create_tagset_id(name, 1)
                    tag = {"id": tag_id, "value": tag_value}
                    tag_manager.add_tag_to_tagset(tagset_id, tag)
                tags.add(tag_id)

        # Process numerical tags by ranges
        for name in NUMERICAL_TAGSET_TYPES.keys():
            tag_value = row[name]
            if pd.notna(tag_value):
                tag_name = get_tag(tag_value, RANGES[name])
                if tag_name:
                    tag_id, new_id = tag_manager.get_or_create_tag_id(tag_name, name)
                    if new_id:
                        tagset_id = tag_manager.get_or_create_tagset_id(name, 1)
                        tag = {"id": tag_id, "value": tag_name}
                        tag_manager.add_tag_to_tagset(tagset_id, tag)
                    tags.add(tag_id)

        tag_manager.add_media(file_uri, thumbnail, list(tags))

        if i % 100 == 0:
            current_time = time.time()
            times.append(current_time - start_time)
            rows_processed.append(i + 1)

    # Plotting the results
    plt.figure(figsize=(10, 6))
    plt.plot(rows_processed, times, label="Rows Processed")
    plt.xlabel("Rows Processed")
    plt.ylabel("Time (seconds)")
    plt.title("Rows Processed Over Time")
    plt.legend()
    plt.grid(True)

    # Save the plot figure
    plt.savefig("../build/rows_processed_good.png")

    # Save data of the plot in a file
    with open("../build/rows_processed_good.txt", "w") as f:
        f.write("Rows Processed, Time (seconds)\n")
        for i in range(len(rows_processed)):
            f.write(f"{rows_processed[i]}, {times[i]}\n")

    return tag_manager
