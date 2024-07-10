import requests
from bs4 import BeautifulSoup
import datetime
import pandas as pd
from tqdm import tqdm
import argparse
import threading
import os

NUMBER_OF_THREADS = 100

"""
This script adds image URIs and Timestamps to a CSV file.
"""

lock = threading.Lock()

def get_album_image_url(track_url):
    """
    Fetch the album image URL from the Spotify track page.
    """
    response = requests.get(track_url)
    soup = BeautifulSoup(response.text, features="html.parser")
    album_img_tag = soup.find("meta", property="og:image")
    if album_img_tag:
        return album_img_tag["content"]
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

def process_row(uri, image_uris_set):
    """
    Process a single row, adding the image URI and downloading the image.
    """
    track_url = f"https://open.spotify.com/track/{uri.split(':')[-1]}"
    image_url = get_album_image_url(track_url)
    if image_url:
        short_url = image_url[24:]
        with lock:
            if short_url in image_uris_set:
                return short_url
            image_uris_set.add(short_url)
        # Uncomment the following lines to enable image downloading
        # image_name = f"../data/album_images/{short_url}.jpg"
        # download_image(image_url, image_name)
        return short_url
    return ""

def add_image_uri_to_df(df, start, end):
    """
    Add album image URIs to the DataFrame and download the image to the local directory. (../data/album_images/)
    """
    image_uris_set = set()
    image_uris = []

    threads = []
    for uri in tqdm(df["sp_uri"][start:end]):
        # Create and start a new thread for each URI
        thread = threading.Thread(target=lambda q, arg1, arg2: q.append(process_row(arg1, arg2)), args=(image_uris, uri, image_uris_set))
        threads.append(thread)
        thread.start()

        # Limit the number of active threads to NUMBER_OF_THREADS
        if len(threads) >= NUMBER_OF_THREADS:
            for t in threads:
                t.join()
            threads = []

    # Wait for any remaining threads to finish
    for t in threads:
        t.join()

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

def main(start, end):
    # Load CSV file
    path = "../data/csv_file/full_table"
    df = pd.read_csv(f"{path}.csv", sep="\t", encoding="utf-8", skiprows=range(1, start + 1))

    if end == -1:
        end = len(df)
    # Add image links to data
    df = add_image_uri_to_df(df, start, end)

    # Add timestamp to data
    df = add_timestamp_to_df(df, datetime.datetime(2024, 8, 7, 10, 0, 0))

    # Save updated data to CSV
    df.to_csv(f"{path}_aug.csv", sep="\t", index=False, encoding="utf-8")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--start", type=int, default=0)
    parser.add_argument("--end", type=int, default=-1)
    args = parser.parse_args()
    main(args.start, args.end)
