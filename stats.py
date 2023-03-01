import pandas as pd
import json
import datetime

def process_df(json_file, period_start, period_end):
    """
    Takes a JSON file of clean campaign contributions data,
    loads it into a Pandas data frame, converts dates from strings,
    and drops contributions received outside the specified period.

    Inputs:
        json_file: clean candidate contributions data
        period_start (str): "MM/DD/YYYY"
        period_end (str): "MM/DD/YYYY"

    Returns:
        df (Pandas dataframe): campaign contributions from the specified period
    """
    start = pd.to_datetime(period_start)
    end = pd.to_datetime(period_end)

    df = pd.read_json(json_file)
    df["received_date"] = pd.to_datetime(df["received_date"])

    outside_period = df[ (df["received_date"] < start) |
    df["received_date"] > end].index
    df.drop(outside_period, inplace=True)

    return df

def summary_stats(df, zips, stats_file):
    """
    Genereates summary statistics for the specified zip codes and
    saves them to a JSON file.

    Inputs:
        df (Pandas dataframe): data to generate summary stats from
        zips (lst of strs): zip codes to generate summary stats for
        stats_file (str): JSON filename (e.g., "summary-stats.JSON")
    """
    stats = []

    for zip in zips:
        # Is making a new, zip-specific dataframe the best way to go here?
        # It would take more code to tell Pandas just to do operations for rows 
        # with a certain zip value...
        zip_data = df["zip"] == zip
        zip_stats = {}
        zip_stats["zip"] = zip_data
        zip_stats["num_donations"] = len(zip_data)
        zip_stats["total_donated"] = zip_data["amount"].sum()
        zip_stats["min_donation"] = zip_data["amount"].min()
        zip_stats["max_donation"] = zip_data["amount"].max()
        zip_stats["avg_donation"] = zip_data["amount"].mean()
        stats.append(zip_stats)
    
    with open(stats_file, "w") as sf:
        json.dump(stats, sf, indent=1)
        

# References (process_df):
# https://sparkbyexamples.com/pandas/pandas-change-string-object-to-date-in-dataframe/
# https://www.geeksforgeeks.org/drop-rows-from-the-dataframe-based-on-certain-condition-applied-on-a-column/

# Reference (summary_stats):
# https://stackoverflow.com/questions/13784192/creating-an-empty-pandas-dataframe-and-then-filling-it
