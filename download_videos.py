import os

from pytube import YouTube
from google.cloud import storage

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "client_secrets.json"

title = "0001"
link = "https://www.youtube.com/watch?v=koxRDhAQOpw"

trailer = YouTube(link).streams.first().download('./trailers/')
os.rename(trailer, './trailers/'+title+'.mp4')

buckets = "video-api-bucket"
source = "0001.mp4"
destination = title+".mp4"


def upload_blob(bucket_name, source_file_name, destination_blob_name):

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print("File {} uploaded to {}.".format(source_file_name, destination_blob_name))


upload_blob(buckets, source, destination)
