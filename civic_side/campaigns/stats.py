import pandas as pd
import json

def contribution_stats(df, zips, zips_only, zips_and_city):
    """
    Genereates summary statistics by city zip code (zips) and for the city 
    as a whole, and writes them to two JSON files, one with zip-level data only
    (for choropleths) and one with zip- and city-level data (for tables).

    Inputs:
        df (Pandas dataframe): data to generate summary stats from
        zips (lst of strs): zip codes to generate summary stats for
        zip_only (str): JSON filename (e.g., "stats_by_zip.json")
        zip_and_city (str): JSON filename (e.g., "stats_by_zip_and_city.json")

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
    
    with open(zips_only, "w") as sf:
        json.dump(stats, sf, indent=1)

    # aggregate zip-level stats to city level
    with open(zips_only):
        by_zip = pd.read_json(zips_only)

    chi = {}
    chi["zip"] = "Chicago"
    chi["num_donations"] = float(by_zip["num_donations"].sum())
    chi["avg_num_donations_per_zip"] = (chi["num_donations"] / len(by_zip)) # Is this useful?
    chi["total_donated"] = float(by_zip["total_donated"].sum())
    chi["avg_donated_per_zip"] = float(chi["total_donated"] / len(by_zip)) # Is this useful?
    chi["min_donation"] = float(by_zip["min_donation"].min())
    chi["max_donation"] = float(by_zip["max_donation"].max())
    chi["avg_donation"] = float((chi["total_donated"] / chi["num_donations"]))

    stats.append(chi)

    with open(zips_and_city, "w") as zc:
        json.dump(stats, zc, indent=1)


# References:
# https://stackoverflow.com/questions/13784192/creating-an-empty-pandas-dataframe-and-then-filling-it
# https://stackoverflow.com/questions/47333227/pandas-valueerror-cannot-convert-float-nan-to-integer
