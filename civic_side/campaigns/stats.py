# By Francesca Vescia
import pandas as pd
import json
def contribution_stats(df, zips, stats_file):
    """
    Genereates campaign contribution summary statistics by city zip code (zips)
    and saves the stats to a JSON file (stats_file).

    Inputs:
        df (Pandas dataframe): data to generate summary stats from
        zips (lst of strs): zip codes to generate summary stats for
        stats_file (str) JSON filename (e.g., "contributions_by_zip.json")

    """
    stats = []

    # get zip-level stats
    for zp in zips:
        zip_data = df[df["zip"] == zp]
        zip_stats = {}
        zip_stats["zip"] = zp
        zip_stats["num_donations"] = len(zip_data)
        zip_stats["total_donated"] = zip_data["amount"].sum()
        if zip_stats["num_donations"] == 0:
            zip_stats["min_donation"] = 0
            zip_stats["max_donation"] = 0
            zip_stats["avg_donation"] = 0
        else:
            zip_stats["min_donation"] = zip_data["amount"].min()
            zip_stats["max_donation"] = zip_data["amount"].max()
            zip_stats["avg_donation"] = zip_data["amount"].mean()

        stats.append(zip_stats)
    
    with open(stats_file, "w") as sf:
        json.dump(stats, sf, indent=1)


# References:
# https://stackoverflow.com/questions/13784192/creating-an-empty-pandas-dataframe-and-then-filling-it
# https://stackoverflow.com/questions/47333227/pandas-valueerror-cannot-convert-float-nan-to-integer
