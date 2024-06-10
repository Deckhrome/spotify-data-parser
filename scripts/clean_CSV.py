import pandas as pd

def clean_data(df):
    print(f"Number of rows before cleaning: {df.shape[0]}")
    df['sp_track_popularity'] = pd.to_numeric(df['sp_track_popularity'], errors='coerce')

    emotion_columns = ['happiness_percentage', 'sadness_percentage', 'fear_percentage', 'anger_percentage']
    for col in emotion_columns:
        df[col] = pd.to_numeric(df[col] * 100, errors='coerce').round().astype('Int64').astype(str)
    
    df['sp_track_duration'] = (pd.to_numeric(df['sp_track_duration'], errors='coerce') / 1000).round().astype('Int64')

    df.dropna(subset=['sp_track_name', 'sp_album_name', 'sp_artist_infos'], inplace=True)
    df['emotion_code'] = df['emotion_code'].astype(str)
    df = df[df['emotion_code'].isin(['0', '1', '2', '3'])]

    df['sp_uri'] = df['sp_uri'].str.strip()    
    df['sp_track_name'] = df['sp_track_name'].str.strip()
    df['sp_album_name'] = df['sp_album_name'].str.strip()
    df['sp_artist_infos'] = df['sp_artist_infos'].str.strip()
    df['genre_1'] = df['genre_1'].str.strip()
    df['genre_2'] = df['genre_2'].str.strip()
    df['genre_3'] = df['genre_3'].str.strip()

    print(f"Number of rows after cleaning: {df.shape[0]}")
    
    return df

def CSV_to_DF(path):
    try:
        df = pd.read_csv(path, sep='\t', encoding='utf-8')
        df = clean_data(df)
    except Exception as e:
        print(f"Error : {e}")
    return df
