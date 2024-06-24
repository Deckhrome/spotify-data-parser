import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
# import clean_CSV
from clean_CSV import CSV_to_DF

# Read the CSV file

def explore_data():
    try:
        df = pd.read_csv('../data/full_table_27_aug.csv', sep='\t', encoding='utf-8')
        print("File read successfully")
    except Exception as e:
        print(f"Error reading the file: {e}")
        df = pd.DataFrame()  # Return an empty DataFrame in case of an error

    if not df.empty:
        # Convert 'sp_track_duration' to seconds, round and convert to integer
        df.loc[:, 'sp_track_duration'] = (pd.to_numeric(df['sp_track_duration'], errors='coerce') / 1000).round().astype('Int64')

        # Convert 'sp_track_popularity' to numeric and handle missing values
        df.loc[:, 'sp_track_popularity'] = pd.to_numeric(df['sp_track_popularity'], errors='coerce').astype('Int64')

        # Count unique values for each 'sp_track_duration' and 'sp_track_popularity'
        track_duration_count = df['sp_track_duration'].value_counts().sort_index()
        track_popularity_count = df['sp_track_popularity'].value_counts().sort_index()

        # Print min and max track duration
        print(f"Min track popularity: {track_popularity_count.index.min()} seconds")
        print(f"Max track popularity: {track_popularity_count.index.max()} seconds")
        print(f"Total number of unique track popularity: {len(track_popularity_count)}")

        # convert to numpy array
        track_duration_count = np.array(track_duration_count)

        # Plot the result
        plt.figure(figsize=(10, 6))
        plt.plot(track_duration_count, label='Track Duration Count')
        plt.xlabel('Track Duration (seconds)')
        plt.ylabel('Count')
        plt.title('Track Duration Count')
        plt.legend()
        plt.grid(True)

        # Save the plot
        plt.savefig('../build/track_duration_count.png')

        # Plot the result
        plt.figure(figsize=(10, 6))
        plt.plot(track_popularity_count, label='Track Popularity Count')
        plt.xlabel('Track Popularity')
        plt.ylabel('Count')
        plt.title('Track Popularity Count')
        plt.legend()
        plt.grid(True)

        # Save the plot
        plt.savefig('../build/track_popularity_count.png')

    else:
        print("DataFrame is empty. No operations performed.")


if __name__ == '__main__':
    explore_data()