import os
import requests
import time
import json
import csv
import argparse
from urllib.parse import urlparse
import pandas as pd

import googleapiclient.discovery
import googleapiclient.errors

# OMDB api needs an api key
from local_settings import omdb_apikey

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "client_secrets.json"

# Queries omdb api for film
def get_film_details(title, omdb_apikey):
    query = {"apikey": omdb_apikey, "plot": "full", "type": "movie", "t": title}
    try:
        r = requests.get("http://www.omdbapi.com/?", params=query, timeout=10)
        time.sleep(0.5)
        return r.json()
    except Exception:
        with open("./database/log.csv", "r") as log:
            writer = csv.writer(log)
            writer.writerow(title, Exception)


# Gets Youtube trailer link from Youtube API (if it has one)
def get_youtube_link(title):
    api_service_name = "youtube"
    api_version = "v3"

    youtube = googleapiclient.discovery.build(api_service_name, api_version)

    request = (
        youtube.search()
        .list(part="snippet", maxResults=1, q=title + "trailer")
        .execute()
    )
    # Only taking the first result from Youtube
    if request.get("pageInfo").get("totalResults") > 0:
        response = request.get("items")[0].get("id").get("videoId")
        trailer_link = "https://youtube.com/watch?v=" + response
        return trailer_link
    else:
        return "None"


# Loops through a csv to get_film_details then outputs to csv
def main(file):
    with open("./database/" + file, "r") as file:
        reader = csv.reader(file, delimiter=",")
        for row in reader:
            print(row[0])
            omdb = get_film_details(row[0], omdb_apikey)
            trailer = get_youtube_link(row[0])
            row.append(trailer)
            row = pd.DataFrame([row])
            omdb_df = pd.DataFrame([omdb])
            combined = row.join(omdb_df)

            with open("./database/films-omdb.csv", "a", newline="") as output:
                combined.to_csv(output, mode="a", header=output.tell() == 0)
    print("Converted Films")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run films through OMDB API")
    parser.add_argument("file", type=str, help="CSV file in /database/ to use.")
    args = parser.parse_args()
    main(args.file)
