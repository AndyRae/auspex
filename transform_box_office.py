import csv
import argparse
import pandas as pd

# Takes a csv of film screenings, rolls them up into single entries per film
# Filters for Week 1, at least 6 screenings
# TODO: Need to ensure box office + admissions columns are integers

# load the csv
def main(file: str) -> None:
    df_screenings: pd.DataFrame = pd.read_csv("./database/" + file)

    # filter so we only have week one data and drop screenings column
    is_week_one = df_screenings["week"] == "Week 1"
    df_week_one = df_screenings[is_week_one].drop(columns="screenings")
    df_week_one.tail()

    # filter so we only have films that played 6+ times (did a whole run)
    df_films = df_week_one.groupby("film").filter(lambda L: len(L) >= 6)
    df_films.tail()

    # combine the individual screenings of a film into summary row each
    df_summary = df_films.drop(columns="week_year").groupby(["film"]).sum()

    dates = []
    distributors = []
    week_years = []

    for i in df_summary.index:
        dates.append(df_films["date"][df_films["film"] == i].iloc[0])
        distributors.append(df_films["distributor"][df_films["film"] == i].iloc[0])
        week_years.append(df_films["week_year"][df_films["film"] == i].iloc[0])

    df_output = df_summary
    df_output.insert(0, "dates", dates)
    df_output.insert(0, "distributors", distributors)
    df_output.insert(0, "week_years", week_years)

    # export to csv
    df_output.to_csv("./database/films.csv", header=True)
    print(df_output.head())
    print("Films transformed.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Transform box office data")
    parser.add_argument("file", type=str, help="CSV file in /database/ to use.")
    args = parser.parse_args()
    main(args.file)
