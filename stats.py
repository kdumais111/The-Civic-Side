import pandas as pd
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

def summary_stats(df, zips):
    """
    Genereates summary statistics for the specified zip codes.

    Inputs:
        df (Pandas dataframe): data to generate summary stats from
        zips (lst of strs): zip codes to generate summary stats for

    Returns:
        stats (Pandas dataframe): summary stats by zip code
    """
    stats = [] # TODO: pass to pd.DataFrame

    for zip in zips:
        zip_stats = {}
        zip_stats["amt_donated"] = NONE
        zip_stats["num_donations"] = NONE
        zip_stats["min_donation"] = NONE
        zip_stats["max_donation"] = NONE
        zip_stats["avg_donation"] = NONE


# References (process_df):
# https://sparkbyexamples.com/pandas/pandas-change-string-object-to-date-in-dataframe/
# https://www.geeksforgeeks.org/drop-rows-from-the-dataframe-based-on-certain-condition-applied-on-a-column/

# References (summary_stats):
# https://stackoverflow.com/questions/13784192/creating-an-empty-pandas-dataframe-and-then-filling-it