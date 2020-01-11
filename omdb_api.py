from local_settings import apikey
import requests
import time
import json
import csv
from urllib.parse import urlparse
import pandas as pd

apikey = apikey
title = urlparse("downton abbey")

#queries omdb api for film
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
        continue


#loops through a csv to pass to get_film_details then outputs to csv
def csv_download():
    with open("./database/films.csv", "r") as file:
        reader = csv.reader(file, delimiter=",")
        for row in reader:
            response = get_film_details(row[1], apikey)
            df = pd.DataFrame([response])
            
            with open("./database/films-omdb.csv", "a", newline='') as output:
                df.to_csv(output, mode = 'a', header=output.tell()==0)
    print("Converted Films")
