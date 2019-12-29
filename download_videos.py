import os
import csv
import time

from pytube import YouTube
from google.cloud import storage

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "client_secrets.json"


def download_video(title, link):
    print(link)
    try:
        trailer = YouTube(link).streams.first().download("./trailers/")
        os.rename(trailer, "./trailers/" + title + ".mp4")
    except KeyError:
        print(title + " returns key error.")
    time.sleep(10.0)


def upload_blob(bucket_name, source_file_name, destination_blob_name):

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print("File {} uploaded to {}.".format(source_file_name, destination_blob_name))


def csv_download():
    with open("./database/films.csv", "r") as file:
        reader = csv.reader(file, delimiter=",")
        for row in reader:
            print(row[0], row[4])
            download_video(row[0], row[4])
    print("Downloaded Trailers")


def csv_upload():
    bucket = "video-api-bucket"
    for file in os.listdir("./trailers/"):
        if file.endswith(".mp4"):
            print(bucket, "./trailers/" + file, file)
            upload_blob(bucket, "./trailers/" + file, file)
    print("Uploaded Trailers")


# csv_download()
csv_upload()