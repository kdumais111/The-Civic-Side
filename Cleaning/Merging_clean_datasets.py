import pandas as pd
import pathlib

from ._311_Dataset_Cleaning import create_311_clean_csvs
from .cleanzipcodes_toprecincts import build_zip_precinct_csv
from .voterturnout_cleaning import clean_voter_turnout
from .zillowcleaning import clean_zillow_to_csv

#Code written by Katherine Dumais


def execute_data_merge():
    '''
    Clean all non-campaign finance data and merge it together.
    '''
    #Create Clean Datasets
    create_311_clean_csvs()
    build_zip_precinct_csv()
    clean_voter_turnout()
    clean_zillow_to_csv()
   

    #Combine datasets
    voting_zipcode = voting_to_zipcode()
    zillow= pathlib.Path(__file__
                ).parent /"zillow_cleaned_complete.csv"
    voting_housing = combine_data_zip(voting_zipcode, zillow, "Zipcode")
    complaints= pathlib.Path(__file__
                ).parent /"311_complaint_count.csv"
    add_complaints = combine_data_zip(voting_housing, complaints, "zipcode")
    complete = add_complaints.drop(add_complaints.columns[3], axis=1)

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
    voters= pathlib.Path(__file__).parent /"voterturnout.csv"
    voting_df = pd.read_csv(voters)
    districts_df = pd.read_csv(districts)
    voting_df["precinct"]=voting_df["precinct"].astype(int)
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
    new_data = pd.read_csv(filename)
    merged_set = pd.merge(df, new_data, left_on = "zip", 
                    right_on = column, how = "left").drop(columns = [column])
    merged_set = merged_set.dropna()
    return merged_set





# def combine_zillow_data(df):
#     '''
#     Takes a dataframe and combines the 2019 average housing price data csv
#     ("zillow_cleaned_complete.csv") and adds it to the dataframe by zip.
#     '''
#     #combine zillow dataset- housing prices
#     zillow= pathlib.Path("Merging_clean_datasets.py"
#                     ).parent /"Cleaning/zillow_cleaned_complete.csv"
#     housing = pd.read_csv(zillow)
#     voting_housing = pd.merge(df,housing, left_on = "zip", 
#                     right_on = "Zipcode", how = "left").drop(columns = ['Zipcode'])
#     return voting_housing

# def combine_complaints_data(df):
#     '''
#     Combine Count of Complaints by Dataset into the CSV 
#     '''
#     complaints= pathlib.Path("Merging_clean_datasets.py"
#                     ).parent /"Cleaning/311_complaint_count.csv"
#     complaints = pd.read_csv(complaints)
#     add_complaints = pd.merge(df, complaints,
#                             left_on = "zip", right_on = "zipcode", how = "left"
#                             ).drop(columns = ['zipcode', 'Unnamed: 0'])
#     add_complaints = add_complaints.dropna()
#     return add_complaints





