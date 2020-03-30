# Auspex

**Data pipeline for predicting box office data.**

A data extraction and transforming pipeline for machine learning. Extracting data from source, adding features (country, director, trailer annotations etc.) through APIs. Also extracts upcoming films for predictions.

Essentially used with Vista box office data, and extracting from [UK Box Office](https://github.com/AndyRae/uk-box-office).

MVP workflow is:

* extract_vista.py - `Extracts box office data from Vista EOD PDF reports.`
* transform_box_office.py - `Tranforms Vista box office data, grouping + filtering screenings.`
* transform_imdb.py - `Adds IMDB data and trailer links.`
* extract_upcoming.py - `Scrapes a popular film UK release date website for upcoming titles + release dates.`

---

* transform_trailers.py - `Adds Youtube trailers for each film to Google Cloud`
* transform_trailers_analysis.py - `Analyzes Youtube trailers for annotations - using Google Video API`

---
