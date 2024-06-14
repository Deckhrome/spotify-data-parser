import pandas as pd

def clean_data(df):
    print(f"Number of rows before cleaning: {df.shape[0]}")

    # Convert 'sp_track_popularity' to numeric
    df['sp_track_popularity'] = pd.to_numeric(df['sp_track_popularity'], errors='coerce')

    # Convert emotion columns to percentage, round and convert to string
    emotion_columns = ['happiness_percentage', 'sadness_percentage', 'fear_percentage', 'anger_percentage']
    for col in emotion_columns:
        df[col] = pd.to_numeric(df[col] * 100, errors='coerce').round().astype('Int64').astype(str)

    # Convert 'sp_track_duration' to seconds, round and convert to integer
    df['sp_track_duration'] = (pd.to_numeric(df['sp_track_duration'], errors='coerce') / 1000).round().astype('Int64')

    # Strip leading/trailing whitespace from all relevant columns
    strip_columns = ['sp_uri', 'sp_track_name', 'sp_album_name', 'sp_artist_infos', 'genre_1', 'genre_2', 'genre_3']
    for col in strip_columns:
        df[col] = df[col].str.strip()

    # Drop rows with missing values in essential columns
    essential_columns = ['sp_track_name', 'sp_album_name', 'sp_artist_infos', 'sp_uri']
    df.dropna(subset=essential_columns, inplace=True)

    # Drop rows with duplicate 'sp_uri' values
    df.drop_duplicates(subset='sp_uri', keep='first', inplace=True)

    # Replace missing values in genre_2 and genre_3 with genre_1
    df['genre_2'].fillna(df['genre_1'], inplace=True)
    df['genre_3'].fillna(df['genre_1'], inplace=True)

    # Ensure 'emotion_code' is a string and filter by valid emotion codes
    df['emotion_code'] = df['emotion_code'].astype(str)
    df = df[df['emotion_code'].isin(['0', '1', '2', '3'])]

    # Drop rows with any missing values in remaining columns (if needed)
    df.dropna(inplace=True)

    print(f"Number of rows after cleaning: {df.shape[0]}")

    return df

def CSV_to_DF(path):
    try:
        df = pd.read_csv(path, sep='\t', encoding='utf-8')
        df.info()
        df = clean_data(df)
    except Exception as e:
        print(f"Error: {e}")
        df = pd.DataFrame()  # Return an empty DataFrame in case of an error
    return df
