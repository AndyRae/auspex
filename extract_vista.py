# TODO: Completely update this from 2016. Add Pandas, refactor.


import tabula
from datetime import datetime
import csv
import os


def convert(filename: str) -> None:
    pdf_path = "./database/" + filename
    tabula.convert_into(pdf_path, "data.csv", pages="all", output_format="csv")


def format() -> None:
    rows: list = []
    screeningsL list = []

    with open("./database/data.csv", mode="r") as file:
        reader = csv.reader(file, delimiter=",")
        dates = next(reader)
        # turns csv into lists
        for line in reader:
            row: list = []
            for cell in line:
                row.append(cell)
            rows.append(row)

    # removes dates rows
    for entry in rows:
        if "Screen No\nDistributor" in entry:
            rows.remove(entry)
            continue
        if "Total Attendance\nTotal Gross\nConc. Total Gross" in entry:
            rows.remove(entry)
            continue
    # removes summary rows
    del rows[-4:]

    for entry in rows:
        screening = []
        for i in range(2, 9):
            if entry[i]:
                # fills list + cleans up data
                screening = [
                    dates[i].split("\n")[1],  # date
                    datetime.strptime(
                        dates[i].split("\n")[1], "%d/%m/%Y"
                    ).isocalendar()[
                        1
                    ],  # dateweeknumber
                    entry[1].split("\n", 1)[1].replace("\n", " ").upper(),  # film
                    entry[0].split("\n")[0],  # screen
                    entry[1].split("\n")[0],  # week
                    entry[0].split("\n")[1],  # distributor
                    entry[i].split("\n")[0],  # admissions
                    entry[i].split("\n")[1].strip("£"),  # revenue
                ]
                screenings.append(screening)

    with open("input.csv", "a") as csv_output:
        # opens csv sheet
        writer = csv.writer(csv_output)

        screenings = sorted(screenings)
        # writes to both sheets
        for screening in screenings:
            writer.writerow(screening)


for filename in os.listdir(local_download_path):
    if filename.endswith("PDF"):
        print("database/eod/" + filename)
        convert(filename)
        format()
print("done")
