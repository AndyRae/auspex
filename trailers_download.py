import os
import csv
import time
from local_settings import cloud_bucket

from pytube import YouTube
from google.cloud import storage

# Run through a list of films, with trailer links (youtube)
# Download them via Pytube
# Then upload them to Google Cloud Storage, for analyzing.


os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "client_secrets.json"

# uses pytube here to download video to /trailers
def download_video(title, link):
    print(link)
    try:
        trailer = YouTube(link).streams.first().download("./trailers/")
        os.rename(trailer, "./trailers/" + title + ".mp4")
    except KeyError:
        print(title + " returns key error.")
    # want to return the path to the file in the bucket


# upload to cloud function
def upload_video(bucket_name, source_file_name, destination_blob_name):

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print("File {} uploaded to {}.".format(source_file_name, destination_blob_name))


# loops through files in /trailers/ and uploads them to google cloud storage
def csv_upload():
    for file in os.listdir("./trailers/"):
        if file.endswith(".mp4"):
            print(cloud_bucket, "./trailers/" + file, file)
            upload_blob(cloud_bucket, "./trailers/" + file, file)
    print("Uploaded Trailers")


# runs through list of csv calling the download_video function
def main(file):
    with open("./database/" + file, "r") as file:
        reader = csv.reader(file, delimiter=",")
        for row in reader:
            print(row[0])
            download_video(
                row[0], row[4]
            )  # Assuming this is where a trailer link is...
            upload_video(
                cloud_bucket, "./trailers/" + row[0] + ".mp4",
            )
            # then upload it in here....
    print("Downloaded Trailers")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Downloads trailers to Google Cloud")
    parser.add_argument(
        "file", type=str, help="CSV list of films to use in /database/."
    )
    args = parser.parse_args()
    main(args.file)
