import requests
from bs4 import BeautifulSoup
import datetime
import pandas as pd
from tqdm import tqdm

"""
This script adds image URIs and Timestamps to a CSV file.
"""

def get_album_image_url(track_url):
    """
    Fetch the album image URL from the Spotify track page.
    """
    response = requests.get(track_url)
    html = response.text
    soup = BeautifulSoup(html, features="html.parser")
    album_img_url = soup.find("meta", property="og:image")["content"]
    return album_img_url

def download_image(image_url, image_name):
    """
    Download the image from the given URL to the local directory.
    """
    with open(image_name, "wb") as f:
        f.write(requests.get(image_url).content)

def add_image_uri_to_df(df):
    """
    Add album image URIs to the DataFrame. And download the image to the local directory. (../data/album_images/)
    """
    image_uris = []
    for uri in tqdm(df["sp_uri"]):
        track_url = f"https://open.spotify.com/track/{uri.split(':')[-1]}"
        image_url = get_album_image_url(track_url)
        if image_url:
            # Download the image to the local directory
            short_url = image_url[24:]
            image_name = f"../data/album_images/{short_url}.jpg"
            #download_image(image_url, image_name)
            # Remove https://i.scdn.co/image/ from the first part of uri
            image_uris.append(short_url)
        else:
            image_uris.append("")  # Or any default value if image URL is not found
    df["image_uri"] = image_uris
    return df

def add_timestamp_to_df(df, starting_date):
    """
    Add timestamps to the DataFrame, starting from the given date.
    """
    timestamps = []
    for _ in range(len(df)):
        timestamps.append(starting_date.strftime("%Y-%m-%d %H:%M:%S"))
        starting_date += datetime.timedelta(minutes=1)
    df["timestamp"] = timestamps
    return df

def main():
    # Load CSV file
    path = "../data/csv_file/sample_table"
    df = pd.read_csv(f"{path}.csv", sep="\t", encoding="utf-8")

    # Add image links to data
    df = add_image_uri_to_df(df)

    # Add timestamp to data
    df = add_timestamp_to_df(df, datetime.datetime(2024, 8, 7, 10, 0, 0))

    # Save updated data to CSV
    df.to_csv(f"{path}_aug.csv", sep="\t", index=False, encoding="utf-8")

if __name__ == "__main__":
    main()
