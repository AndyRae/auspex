# Predicting box office data

MVP workflow is:

* transform_vista.py - `Takes Vista EOD PDF reports, turns them into box_office data in csv.`
* transform_box_office.py - `Tranforms box_office data, rolling up individual screening days into single films with cumulative box office.`
* film_details.py - `Adds IMDB data and trailer link to each film.`

* trailers_download.py - `Adds Youtube trailers for each film to Google Cloud`
* trailers_analyze.py - `Analyzes Youtube trailers for annotations - using Google Video AI`

* upcoming_releases.py - `Scrapes a popular film UK release date website for upcoming titles + release dates.`

* modelling_box_office.py - `For modelling box office data using Tensorflow.` 
* predicting_box_office.py - `For predicting upcoming releases box office, accessing the Tensorflow model.`
* clustering_films.py - `For clustering films, finding comparables and reccommendations.`

* Local_settings.py - Contains:

omdb_apikey = "" `API key for OMDB`
upcoming_url = "" `URL of UK cinema release website`
cloud_bucket = "" `Name of Google Cloud storage bucket`

---
