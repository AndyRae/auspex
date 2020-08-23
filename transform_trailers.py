import os
import csv
import time
import argparse
from local_settings import cloud_bucket

from pytube3 import YouTube
from google.cloud import storage

# Run through a list of films, with trailer links (youtube)
# Download them via Pytube
# Then upload them to Google Cloud Storage, for analyzing.


os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "client_secrets.json"

# uses pytube here to download video to /trailers
def download_video(title: str, link: str) -> None:
    print(link)
    try:
        trailer = YouTube(link).streams.first().download("./trailers/")
        os.rename(trailer, "./trailers/" + title + ".mp4")
    except KeyError:
        print(title + " returns key error.")


# upload to cloud function
def upload_video(
    bucket_name: str, source_file_name: str, destination_blob_name: str
) -> str:

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print("File {} uploaded to {}.".format(source_file_name, destination_blob_name))
    return destination_blob_name + source_file_name


# loops through files in /trailers/ and uploads them to google cloud storage
def csv_upload() -> None:
    for file in os.listdir("./trailers/"):
        if file.endswith(".mp4"):
            print(cloud_bucket, "./trailers/" + file, file)
            upload_blob(cloud_bucket, "./trailers/" + file, file)
    print("Uploaded Trailers")


# runs through list of csv calling the download_video function
def main(file: str) -> None:
    with open("./database/" + file, "r") as file:
        reader = csv.reader(file, delimiter=",")
        for row in reader:
            print(row[0])
            download_video(row[0], row[4])
            # Assuming this is where a trailer link is...
            trailer_cloud_path = upload_video(
                cloud_bucket, "./trailers/" + row[0] + ".mp4",
            )
            row.append(trailer_cloud_path)
    print("Downloaded Trailers")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Downloads trailers to Google Cloud")
    parser.add_argument(
        "file", type=str, help="CSV list of films to use in /database/."
    )
    args = parser.parse_args()
    main(args.file)
