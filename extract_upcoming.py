import requests
import argparse
from datetime import datetime
import csv
from bs4 import BeautifulSoup

# Keeping the site off version control
from local_settings import upcoming_url


def main(month: str, year: str) -> None:
    query: dict = {"sort": "date", "startmonth": month, "startyear": year}
    soup = BeautifulSoup(
        requests.get(upcoming_url, params=query).content, "html.parser"
    )

    films_list: list = []
    for row in soup.find_all("div", {"class": "sche-row"}):
        film = []
        title_element = row.find("div", {"class": "schedule-film-name--title"})
        distributor_element = row.find("span", {"class": "mobile-only distributor"})
        date_element = row.find("h4", {"class": ""})

        # Because how the elements are structured, taking a date row, and the films below it
        if date_element:
            date = datetime.strptime(date_element.text, "%A %d %B %Y").strftime(
                "%d/%m/%Y"
            )
            week_year = datetime.strptime(date, "%d/%m/%Y").isocalendar()[1]
        if title_element:
            title = title_element.text
            distributor = distributor_element.text if distributor_element else ""
            film.append(title.strip("\n").strip("\t"))
            film.append(week_year)
            film.append(distributor)
            film.append(date)
            if "EVENT CINEMA:" in film[0]:
                continue
            else:
                films_list.append(film)

    with open("./database/upcoming.csv", "a") as csv_output:
        writer = csv.writer(csv_output)
        header = ["title", "week_year", "distributor", "lf_release_date"]

        if csv_output.tell() == 0:
            writer.writerow(header)

        for item in films_list:
            writer.writerow(item)
        print("Fetched films")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Gets upcoming films from online source"
    )
    parser.add_argument("month", type=str, help="Month to use. eg. 03")
    parser.add_argument("year", type=str, help="Year to use. eg. 2020")
    args = parser.parse_args()
    main(args.month, args.year)
