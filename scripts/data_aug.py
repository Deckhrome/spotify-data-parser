import requests
from bs4 import BeautifulSoup
import datetime
import pandas as pd
from tqdm import tqdm
import argparse
import threading

NUMBER_OF_THREADS = 18

"""
This script adds image URIs and Timestamps to a CSV file. And also downloads the images to the local directory.
"""

lock = threading.Lock()

def get_album_image_url(track_url):
    """
    Fetch the album image URL from the Spotify track page.
    """
    try:
        response = requests.get(track_url)
        soup = BeautifulSoup(response.text, features="html.parser")
        album_img_tag = soup.find("meta", property="og:image")
        if album_img_tag:
            return album_img_tag["content"]
    except Exception as e:
        print(f"Error fetching image URL from {track_url}: {e}")
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

def process_row(uri, image_uris_set, index, image_uris):
    """
    Process a single row, adding the image URI and downloading the image.
    """
    track_url = f"https://open.spotify.com/track/{uri.split(':')[-1]}"
    image_url = get_album_image_url(track_url)
    # If image URL is found
    if image_url:
        # Extract the image URI from the URL
        # https://i.scdn.co/image/
        image_uri = image_url[24:]
        with lock:
            # Check if the image URI is already in the set
            if image_uri in image_uris_set:
                image_uris[index] = image_uri
                return
            image_uris_set.add(image_uri)
        image_name = f"../data/album_images/{image_uri}.jpg"
        # Download the image and save the URI
        download_image(image_url, image_name)
        image_uris[index] = image_uri
    else:
        image_uris[index] = ""

def add_image_uri_to_df(df, start, end):
    """
    Add album image URIs to the DataFrame and download the image to the local directory. (../data/album_images/)
    """
    image_uris_set = set()
    image_uris = df["image_uri"].tolist()  # Copy existing values

    threads = []
    for idx, uri in tqdm(enumerate(df["sp_uri"][start:end]), total=end-start):
        thread = threading.Thread(target=process_row, args=(uri, image_uris_set, start + idx, image_uris))
        threads.append(thread)
        thread.start()

        if len(threads) >= NUMBER_OF_THREADS:
            for t in threads:
                t.join()
            threads = []

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
    df["Timestamp UTC"] = timestamps
    return df

def main(start, end):
    # Load CSV file
    path = "../data/csv_file/full_table_aug"
    df = pd.read_csv(f"{path}.csv", sep="\t", encoding="utf-8")

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
