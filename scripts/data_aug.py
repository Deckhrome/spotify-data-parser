import requests
from bs4 import BeautifulSoup
import datetime
import pandas as pd
from tqdm import tqdm
import os

"""
This script adds image URIs and Timestamps to a CSV file.
"""

def get_album_image_url(track_url):
    """
    Fetch the album image URL from the Spotify track page.
    """
    try:
        response = requests.get(track_url)
        html = response.text
        soup = BeautifulSoup(html, features="html.parser")
        album_img_url = soup.find("meta", property="og:image")["content"]
        return album_img_url
    except Exception as e:
        print(f"Error fetching album image URL: {e}")
        return None

def download_image(image_url, image_name):
    """
    Download the image from the given URL to the local directory.
    """
    try:
        with open(image_name, "wb") as f:
            f.write(requests.get(image_url).content)
    except Exception as e:
        print(f"Error downloading image: {e}")

def add_image_uri_to_df(df, image_dir="../data/album_images/"):
    """
    Add album image URIs to the DataFrame and download the image to the local directory.
    """
    if not os.path.exists(image_dir):
        os.makedirs(image_dir)

    image_uris = []
    downloaded_images = set(os.listdir(image_dir))
    
    for uri in tqdm(df["sp_uri"]):
        track_url = f"https://open.spotify.com/track/{uri.split(':')[-1]}"
        image_url = get_album_image_url(track_url)
        if image_url:
            # Remove https://i.scdn.co/image/ from the first part of uri
            short_url = image_url[24:]
            image_name = f"{image_dir}{short_url}.jpg"
            image_file_name = f"{short_url}.jpg"
            
            if image_file_name not in downloaded_images:
                download_image(image_url, image_name)
                downloaded_images.add(image_file_name)

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
