## Predicting box office data

MVP workflow is:

* vista_eod_tabula.py - Takes Vista EOD PDF reports, turns them into box office data in csv.
* transform_daily.py - Tranforms box office data, rolling up individual screening days into single films with cumulative box office.
* omdb_api.py - Adds IMDB data to each film 

* download_videos.py - adds youtube trailers for each film to google cloud
* analyze_videos.py - analyzes youtube trailers for annotations - using google video api

* future_films.py - Scrapes a popular film UK release date website for upcoming titles + release dates

* modelling_box_office.py - For modelling box office data