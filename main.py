import sqlite3
import os
import csv

DEFAULT_PATH = os.path.join(os.path.dirname(__file__), "./database/database.db")

# create a db
def db_create():
    conn = sqlite3.connect("./database/database.db")

    c = conn.cursor()

    c.execute(
        """CREATE TABLE films
             (id integer PRIMARY KEY, title text, box_office real, admissions real, trailer_link text)"""
    )

    c.execute(
        """CREATE TABLE trailer_labels
            (id integer PRIMARY KEY, entity_description text, start_time real, end_time real, confidence real)"""
    )

    conn.commit()
    conn.close()

# db connector
def db_connect(db_path=DEFAULT_PATH):
    con = sqlite3.connect(db_path)
    return con

# db feeding csv
def db_feed_csv(con):
    with open("./database/films.csv", "r") as films_list:
        dr = csv.DictReader(films_list)
        to_db = [
            (i["title"], i["box_office"], i["admissions"], i["trailer_link"])
            for i in dr
        ]
    con = db_connect()
    c = con.cursor()
    c.executemany(
        "INSERT INTO films (title, box_office, admissions, trailer_link) VALUES (?, ?, ?, ?);",
        to_db,
    )
    con.commit()
    con.close()

db_create()
db_feed_csv(db_connect)