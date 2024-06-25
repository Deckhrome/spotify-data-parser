import pandas as pd

def clean_data(df):
    print(f"Number of rows before cleaning: {df.shape[0]}")

    # Convert 'sp_track_popularity' to numeric and handle missing values
    df['sp_track_popularity'] = pd.to_numeric(df['sp_track_popularity'], errors='coerce').astype('Int64')

    # Convert emotion columns to percentage, round and convert to integer
    emotion_columns = ['happiness_percentage', 'sadness_percentage', 'fear_percentage', 'anger_percentage']
    for col in emotion_columns:
        df[col] = (pd.to_numeric(df[col] * 100, errors='coerce').round()).astype('Int64')

    # Convert 'sp_track_duration' to seconds, round and convert to integer
    df['sp_track_duration'] = (pd.to_numeric(df['sp_track_duration'], errors='coerce') / 1000).round().astype('Int64')

    # Strip leading/trailing whitespace from all relevant columns
    strip_columns = ['sp_uri', 'sp_track_name', 'sp_album_name', 'sp_artist_infos', 'genre_1', 'genre_2', 'genre_3']
    df[strip_columns] = df[strip_columns].apply(lambda col: col.str.strip())

    # Drop rows with missing values in essential columns
    essential_columns = ['sp_track_name', 'sp_album_name', 'sp_artist_infos', 'sp_uri']
    df.dropna(subset=essential_columns, inplace=True)

    # Drop rows with duplicate 'sp_uri' values
    df.drop_duplicates(subset='sp_uri', keep='first', inplace=True)

    # Replace missing values in genre_2 and genre_3 with genre_1
    df['genre_2'].fillna(df['genre_1'], inplace=True)
    df['genre_3'].fillna(df['genre_1'], inplace=True)

    # Ensure 'emotion_code' is a string, filter by valid emotion codes
    df['emotion_code'] = df['emotion_code'].astype(str)
    df = df[df['emotion_code'].isin(['0', '1', '2', '3'])]

    # Convert 0 to hapiness, 1 to sadness, 2 to anger, 3 to fear
    df.loc[:, 'emotion_code'] = df['emotion_code'].replace({'0': 'happiness', '1': 'sadness', '2': 'anger', '3': 'fear'})

    

    # Change name of the columns
    df.columns = [
        'id', 'uri', 'track_name', 'track_duration', 'track_popularity', 'album_name', 'artist_infos',
        'x', 'y', 'z', 'color', 'happiness_percentage', 'sadness_percentage', 'anger_percentage',
        'fear_percentage', 'emotion', 'genre', 'genre_2', 'genre_3'
    ]

    print(f"Number of rows after cleaning: {df.shape[0]}")
    return df

def CSV_to_DF(path):
    try:
        df = pd.read_csv(path, sep='\t', encoding='utf-8')
        if not path.endswith('_clean.csv'):
            df = clean_data(df)
            df.to_csv(path.replace('.csv', '_clean.csv'), sep='\t', encoding='utf-8', index=False)
        df.info()
    except Exception as e:
        print(f"Error: {e}")
        df = pd.DataFrame()  # Return an empty DataFrame in case of an error
    return df
