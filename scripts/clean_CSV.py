import pandas as pd


def clean_data(df):
    """
    Description: This function cleans the input DataFrame by performing the following operations:
    - Convert 'sp_track_popularity' to numeric and handle missing values
    - Convert emotion columns to percentage, round and convert to integer
    - Convert 'sp_track_duration' to seconds, round and convert to integer
    - Strip leading/trailing whitespace from all relevant columns
    - Drop rows with missing values in essential columns
    - Drop rows with duplicate 'sp_uri' values
    - Replace missing values in genre_2 and genre_3 with genre_1
    - Ensure 'emotion_code' is a string, filter by valid emotion codes
    - Convert emotion codes to emotion names
    - Rename columns

    Args:
    ----------------
    df: The input DataFrame.

    Returns:
    ----------------
    df: The cleaned DataFrame.
    """

    print(f"Number of rows before cleaning: {df.shape[0]}")

    # Convert 'sp_track_popularity' to numeric and handle missing values
    df["sp_track_popularity"] = pd.to_numeric(
        df["sp_track_popularity"], errors="coerce"
    ).astype("Int64")

    # Convert emotion columns to percentage, round and convert to integer
    emotion_columns = [
        "happiness_percentage",
        "sadness_percentage",
        "fear_percentage",
        "anger_percentage",
    ]
    for col in emotion_columns:
        df[col] = (
            (pd.to_numeric(df[col], errors="coerce") * 100).round().astype("Int64")
        )

    # Convert 'sp_track_duration' to seconds, round and convert to integer
    df["sp_track_duration"] = (
        (pd.to_numeric(df["sp_track_duration"], errors="coerce") / 1000)
        .round()
        .astype("Int64")
    )

    # Strip leading/trailing whitespace from all relevant columns
    strip_columns = [
        "sp_uri",
        "sp_track_name",
        "sp_album_name",
        "sp_artist_infos",
        "genre_1",
        "genre_2",
        "genre_3",
    ]
    df[strip_columns] = df[strip_columns].apply(lambda col: col.str.strip())

    # Drop rows with missing values in essential columns
    essential_columns = ["sp_track_name", "sp_album_name", "sp_artist_infos", "sp_uri"]
    df.dropna(subset=essential_columns, inplace=True)

    # Change uri value with the correct format : https://open.spotify.com/track/uri
    df["sp_uri"] = df["sp_uri"].apply(lambda x: f"https://open.spotify.com/track/{x}")

    # Drop rows with duplicate 'sp_uri' values
    df.drop_duplicates(subset="sp_uri", keep="first", inplace=True)

    # Replace missing values in genre_2 and genre_3 with genre_1
    df["genre_2"].fillna(df["genre_1"], inplace=True)
    df["genre_3"].fillna(df["genre_1"], inplace=True)

    # Ensure 'emotion_code' is a string, filter by valid emotion codes
    df["emotion_code"] = df["emotion_code"].astype(str)
    valid_emotion_codes = ["0", "1", "2", "3"]
    df = df[df["emotion_code"].isin(valid_emotion_codes)]

    # Convert emotion codes to emotion names
    emotion_mapping = {"0": "happiness", "1": "sadness", "2": "anger", "3": "fear"}
    df["emotion_code"] = df["emotion_code"].replace(emotion_mapping)

    # Print unique value for color
    print(df["color"].unique())

    # Rename columns
    column_mapping = {
        "sp_uri": "uri",
        "sp_track_name": "track_name",
        "sp_track_duration": "track_duration",
        "sp_track_popularity": "track_popularity",
        "sp_album_name": "album_name",
        "sp_artist_infos": "artist_infos",
        "emotion_code": "emotion",
        "genre_1": "genre",
    }
    df.rename(columns=column_mapping, inplace=True)

    print(f"Number of rows after cleaning: {df.shape[0]}")
    return df


def CSV_to_DF(path: str):
    """
    Description: This function reads the data from the CSV file and cleans it if necessary.

    Args:
    ----------------
    path: The path to the CSV file.

    Returns:
    ----------------
    df: The DataFrame containing the data from the CSV file.
    """
    try:
        print(path)
        df = pd.read_csv(path, sep="\t", encoding="utf-8")
        if not path.endswith("_clean.csv"):
            df = clean_data(df)
            df.to_csv(
                path.replace(".csv", "_clean.csv"),
                sep="\t",
                encoding="utf-8",
                index=False,
            )
        df.info()
    except Exception as e:
        print(f"Error: {e}")
        df = pd.DataFrame()  # Return an empty DataFrame in case of an error
    return df
