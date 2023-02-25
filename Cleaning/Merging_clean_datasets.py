import pandas as pd
import pathlib

#combine voting datasets and zipcode
districts = pathlib.Path("Merging_clean_datasets.py"
                    ).parent /"Cleaning/clean_zipcode_precinct.csv"
voters= pathlib.Path("Merging_clean_datasets.py").parent /"Cleaning/voterturnout.csv"
voting_df = pd.read_csv(voters)
districts_df = pd.read_csv(districts)
voting_df["precinct"]=voting_df["precinct"].astype(int)
voting_district = pd.merge(districts_df, voting_df, 
                on=["ward","precinct"], how='inner')
#voting_district=voting_district[["zip", "precinct","ward","Turnout"]]
voting_combined = voting_district.groupby(["zip"]).sum().reset_index()
voting_combined["votingrates"]= voting_district["Ballots Cast"]/voting_district["Register Voters"]
voting_combined = voting_combined[['zip', "votingrates"]]

#combine zillow dataset- housing prices
zillow= pathlib.Path("Merging_clean_datasets.py"
                ).parent /"Cleaning/zillow_cleaned_complete.csv"
housing = pd.read_csv(zillow)
voting_housing = pd.merge(voting_combined,housing, left_on="zip", 
                right_on="Zipcode", how="left").drop(columns = ['Zipcode'])

# add in complaint counts
complaints= pathlib.Path("Merging_clean_datasets.py"
                ).parent /"Cleaning/311_complaint_count.csv"
complaints = pd.read_csv(complaints)
add_complaints= pd.merge(voting_housing, complaints, left_on="zip", 
                right_on="zipcode", how="left").drop(columns = ['zipcode', 'Unnamed: 0'])

# Make csv
pd.to_csv(add_complaints)


