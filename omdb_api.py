import requests
import time
import json
import csv
import argparse
from urllib.parse import urlparse
import pandas as pd

# OMDB api needs an api key
from local_settings import apikey

# Queries omdb api for film
def get_film_details(title, apikey):
    query = {"apikey": apikey, "plot": "full", "type": "movie", "t": title}
    try:
        r = requests.get("http://www.omdbapi.com/?", params=query, timeout=10)
        time.sleep(0.5)
        return r.json()
    except Exception:
        with open("./database/log.csv", "r") as log:
            writer = csv.writer(log)
            writer.writerow(title, Exception)


# Loops through a csv to get_film_details then outputs to csv
def main(file):
    with open("./database/" + file, "r") as file:
        reader = csv.reader(file, delimiter=",")
        for row in reader:
            response = get_film_details(row[0], apikey)
            row = pd.DataFrame([row])
            df = pd.DataFrame([response])
            combined = row.join(df)

            with open("./database/films-omdb.csv", "a", newline="") as output:
                combined.to_csv(output, mode="a", header=output.tell() == 0)
    print("Converted Films")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run films through OMDB API")
    parser.add_argument("file", type=str, help="CSV file in /database/ to use.")
    args = parser.parse_args()
    main(args.file)
