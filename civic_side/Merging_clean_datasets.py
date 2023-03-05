import pandas as pd
import pathlib

from .the_polis._311_Dataset_Cleaning import create_311_clean_csvs
from .the_polis.cleanzipcodes_toprecincts import build_zip_precinct_csv
from .the_polis.voterturnout_cleaning import clean_voter_turnout
from .the_polis.zillowcleaning import clean_zillow_to_csv

from campaigns.crawler import get_contributions, save_contributions
from campaigns.cleanup import clean, merge_candidates, process_contributions
from campaigns.stats import zip_stats, chi_stats
from campaigns.utils import PAGES_TO_SCRAPE, START, END, ZIP_STRS


# Campaign cleaning functions written by Francesca Vescia
# Merging structure and csv cleaning functions written by Katherine Dumais

def execute_data_merge():
    '''
    Clean all non-campaign finance data and merge it together.
    '''
    #Create Clean Datasets
    create_311_clean_csvs()
    build_zip_precinct_csv()
    clean_voter_turnout()
    clean_zillow_to_csv()
    get_campaigns_data()
   

    #Combine datasets
    voting_zipcode = voting_to_zipcode()
    zillow= pathlib.Path(__file__
                ).parent /"zillow_cleaned_complete.csv"
    voting_housing = combine_data_zip(voting_zipcode, zillow, "Zipcode")
    complaints= pathlib.Path(__file__
                ).parent /"311_complaint_count.csv"
    add_complaints = combine_data_zip(voting_housing, complaints, "zipcode")
    campaign = pathlib.Path(__file__
                ).resolve().parents[1] /"campaigns/contributions/stats_by_zip.json"
    add_campaign = combine_data_zip(add_complaints, campaign, "zip")
    complete = add_campaign.drop(add_complaints.columns[3], axis=1)

    # Make csv
    complete.to_csv("merged.csv", index=False)
    return print("data clean and merge complete")

def voting_to_zipcode():
    '''
    Import Voting Turnout CSV and Zipcode to Precinct CSV to dataframe.
    Combine datasets by zipcode.
    '''
    districts = pathlib.Path(__file__
                        ).parent /"clean_zipcode_precinct.csv"
    voters = pathlib.Path(__file__).parent /"voterturnout.csv"
    voting_df = pd.read_csv(voters)
    districts_df = pd.read_csv(districts)
    voting_df["precinct"] = voting_df["precinct"].astype(int)
    voting_district = pd.merge(districts_df, voting_df, 
                    on=["ward","precinct"], how='inner')
    voting_combined = voting_district.groupby(["zip"]).sum().reset_index()
    voting_combined["votingrates"]= voting_district["Ballots Cast"]\
                                    / voting_district["Register Voters"]
    voting_combined = voting_combined[['zip', "votingrates"]]
    return voting_combined


def combine_data_zip(df, filename, column):
    '''
    Takes a dataframe and adds data from a CSV, joining by zipcode.
    Returns merged dataframe.
    '''
    if "json" in str(filename):
        new_data= pd.read_json(filename)
    else:
        new_data = pd.read_csv(filename)
    if column == "zip":
        merged_set = pd.merge(df, new_data, how='left', on="zip")   
    else:
        merged_set = pd.merge(df, new_data, left_on = "zip", 
                        right_on = column, how = "left").drop(columns = [column])
    merged_set = merged_set.dropna()
    return merged_set

def get_campaigns_data():
    clean_files = []
    for page, raw_data in PAGES_TO_SCRAPE:
        contributions = get_contributions(page)
        save_contributions(contributions, raw_data)
        clean(raw_data)
        clean_files.append(raw_data.split(".")[0] + "_clean.json")
    contributions = merge_candidates(clean_files)
    processed_contributions = process_contributions(contributions, START, END)
    contribution_stats(processed_contributions, ZIP_STRS, 
                       "civic_side/campaigns/contributions/contributions_by_zip.json")