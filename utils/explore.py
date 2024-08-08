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

# Open file showing speed (rows processed over time) in ../build/rows_processed_good(bad).png
def plot_speed():
    data = pd.read_csv('../build/rows_processed_good.csv', sep=', ', encoding='utf-8')
    df = pd.DataFrame(data)
    rows_processed_1 = np.array(df['Rows Processed'])
    time_1 = np.array(df['Time (seconds)'])

    data2 = pd.read_csv('../build/rows_processed_bad.csv', sep=', ', encoding='utf-8')
    df2 = pd.DataFrame(data2)
    rows_processed_2 = np.array(df2['Rows Processed'])
    time_2 = np.array(df2['Time (seconds)'])

    plt.figure(figsize=(10, 6))
    plt.plot(rows_processed_1, time_1, label='Exponential')
    plt.plot(rows_processed_2, time_2, label='Linear')
    plt.title('Rows Processed vs Time')
    plt.xlabel('Rows Processed')
    plt.ylabel('Time (seconds)')
    plt.grid(True)

    # Add a legend
    plt.legend()

    # Save the plot to a file
    plt.savefig('output_plot.png')

    # Show the plot (optional)
    plt.show()

def plot_stats():
    df = pd.read_csv('stats.csv', sep='\t', encoding='utf-8')

    sample_length = np.array(df['sample_length'])
    rows_count = np.array(df['rows_count'])

    # Plot number of rows depeding of the value of the first column which is sample_lenght
    plt.figure(figsize=(10, 6))
    plt.plot(sample_length, rows_count, label='Number of Rows')
    plt.xlabel('Sample Length')
    plt.ylabel('Number of Rows')
    plt.title('Number of Rows vs Sample Length')
    plt.legend()
    plt.grid(True)
    plt.show()

    # Get the equation of the line 
    m, b = np.polyfit(sample_length, rows_count, 1)
    print(f"Equation of the line: y = {m}x + {b}")
    print(f"Number of rows for all data: {m * 436000 + b}")

def get_unique_values(df, column):
    """Get unique values from a column in a DataFrame."""
    return df[column].unique()

def show_duplicates(df, column):
    """Show duplicate rows based on a column in a DataFrame."""
    return df[df.duplicated(subset=column, keep=False)].sort_values(by=column)

if __name__ == '__main__':
    plot_speed()
    # df = pd.read_csv('../data/csv_file/full_table_aug_clean.csv', sep='\t', encoding='utf-8')
    # print(show_duplicates(df, 'uri'))
    # plot_stats()
    #explore_data()