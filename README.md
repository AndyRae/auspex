# Predicting box office data

MVP workflow is:

* transform_vista.py - `Takes Vista EOD PDF reports, turns them into box_office data in csv.`
* transform_box_office.py - `Tranforms box_office data, rolling up individual screening days into single films with cumulative box office.`
* film_details.py - `Adds IMDB data and trailer link to each film.`

* upcoming_releases.py - `Scrapes a popular film UK release date website for upcoming titles + release dates.`

---

* trailers_download.py - `Adds Youtube trailers for each film to Google Cloud`
* trailers_analyze.py - `Analyzes Youtube trailers for annotations - using Google Video AI`


---

### Local_settings.py - Contains:

* omdb_apikey = "" `API key for OMDB`
* upcoming_url = "" `URL of UK cinema release website`
* cloud_bucket = "" `Name of Google Cloud storage bucket`

---
