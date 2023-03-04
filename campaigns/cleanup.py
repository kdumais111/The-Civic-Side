import json
import re
import datetime
import pandas as pd


def clean(json_file):
    """
    Takes a JSON file of campaign contributions data (json_file), cleans the data,
    and saves it to a new JSON file. (The new file name is the file name from json_file
    with "_clean" added as a suffix.)
    """
    clean_file = json_file.split(".")[0] + "_clean.json"

    with open(json_file) as jf:
        contributions = json.load(jf)
    
    for contribution in contributions:
        contribution["donor_info"] = contribution["donor_info"].replace(contribution["donor_name"], "")
        contribution["donor_name"] = contribution["donor_name"].title()
        contribution["donor_info"] = contribution["donor_info"].strip()
        if re.search(",\s+\D{2}\s+\d{5}", contribution["donor_info"]):
            state_zip = re.search(",\s+\D{2}\s+\d{5}", contribution["donor_info"]).group()
            contribution["state"] = re.search("[A-Z]{2}", state_zip).group()
            contribution["zip"] = re.search("\d{5}", state_zip).group()
        else:
            contribution["state"] = None
            contribution["zip"] = None
        contribution["amount"] = float(contribution["amount"].replace("$", "").replace(",", ""))

    with open(clean_file, "w") as cf:
        json.dump(contributions, cf, indent=1)


def merge_candidates(candidates):
    """
    Takes a list of clean campaign contributions data filenames (one per candidate)
    and returns a dataframe with contributions for all of the specified candidates.

    Inputs:
        candidates (lst of file names): e.g., ["candidate1_clean.json", "candidate2_clean.json"]

    Returns:
        contributions (Pandas data frame)
    """
    dfs = []
    for candidate in candidates:
        df = pd.read_json(candidate, dtype=False)
        dfs.append(df)
    
    contributions = pd.concat(dfs)

    return contributions

def process_contributions(df, period_start, period_end):
    """
    Takes a Pandas dataframe of clean campaign contributions data (df),
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

    df["received_date"] = pd.to_datetime(df["received_date"])
    df["zip_num"] = df["zip"].astype("Int64")
    outside_period = df[ (df["received_date"] < start) | 
        (df["received_date"] > end) ].index
    df.drop(outside_period, inplace=True)
    
    return df


# Reference (clean)
# https://www.geeksforgeeks.org/pattern-matching-python-regex/

# References (process_contributions):
# https://sparkbyexamples.com/pandas/pandas-change-string-object-to-date-in-dataframe/
# https://www.geeksforgeeks.org/drop-rows-from-the-dataframe-based-on-certain-condition-applied-on-a-column/
# https://stackoverflow.com/questions/36921951/truth-value-of-a-series-is-ambiguous-use-a-empty-a-bool-a-item-a-any-o
