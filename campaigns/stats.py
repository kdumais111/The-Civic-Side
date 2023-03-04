import pandas as pd
import json

def zip_stats(df, zips, stats_file):
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
        zip_data = df[df["zip"] == zip]
        zip_stats = {}
        zip_stats["zip"] = zip
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

def chi_stats(stats_file, chi_file):
    """
    Takes a JSON file of statistics by Chicago zip code (stats_file), aggregates
    the statistics to the city level, and saves the aggregated data to a JSON file
    (chi_file).
    """
    with open(stats_file) as sf:
        by_zip = pd.read_json(sf)

    chi = {}
    # Pandas methods return numpy.float64 objects, which are not JSON serializable -->
    # cast to float
    chi["num_donations"] = float(by_zip["num_donations"].sum())
    chi["avg_num_donations_per_zip"] = (chi["num_donations"] / len(by_zip)) # Is this useful?
    chi["total_donated"] = float(by_zip["total_donated"].sum())
    chi["avg_donated_per_zip"] = float(chi["total_donated"] / len(by_zip)) # Is this useful?
    chi["min_donation"] = float(by_zip["min_donation"].min())
    chi["max_donation"] = float(by_zip["max_donation"].max())
    chi["avg_donation"] = float((chi["total_donated"] / chi["num_donations"]))

    with open(chi_file, "w") as cf:
        json.dump(chi, cf, indent=1)


# References (summary_stats):
# https://stackoverflow.com/questions/13784192/creating-an-empty-pandas-dataframe-and-then-filling-it
# https://stackoverflow.com/questions/47333227/pandas-valueerror-cannot-convert-float-nan-to-integer
