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

tagset_types = {
    "sp_track_name": 1,
    "sp_album_name": 1,
    "sp_artist_infos": 1,
    # "sp_track_duration": 5,
    # "sp_track_popularity": 5,
    # "happiness_percentage": 5,
    # "sadness_percentage": 5,
    # "anger_percentage": 5,
    # "fear_percentage": 5,
    "genre_1": 1,
    "genre_2": 1,
    "genre_3": 1
}

alphanumerical_tagset_types = {
}

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
        file_uri = f"https://open.spotify.com/track/{row['sp_uri']}"
        tags = set()
        for name in tagset_types.keys():
            tag_value = row[name]
            if pd.notna(tag_value):
                tag_id, new_id = tag_manager.get_or_create_tag_id(tag_value, name)
                # If the tag is new, add it to the tagset
                if new_id:
                    tagset_id = tag_manager.get_or_create_tagset_id(name, tagset_types[name])
                    tag = {"id": tag_id, "value": tag_value}
                    tag_manager.add_tag_to_tagset(tagset_id, tag)
                tags.add(tag_id)
        # for name in alphanumerical_tagset_types.keys():
        #     tag_value = row[name]
        #     if pd.notna(tag_value):
        #         # Get the first letter of the name
        #         tag_value = tag_value[0].lower()
        #         tag_value = f"{name}_{tag_value}"
        #         tag_id = tag_manager.get_or_create_tag_id(tag_value, name)
        #         tagset_id = tag_manager.get_or_create_tagset_id(name, alphanumerical_tagset_types[name])
        #         tag = {"id": tag_id, "value": tag_value}
        #         tag_manager.add_tag_to_tagset(tagset_id, tag)
        #         tags.add(tag_id)
        # Eliminate any duplicate tags
        #tags = list(set(tags))
        
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
