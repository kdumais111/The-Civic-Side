import pathlib
import pandas as pd


# Clean Zillow Data into 2019 Average Prices CSV
#Written by Katherine Dumais

def clean_zillow_to_csv():
    '''
    Runs all functions used to build a clean zillow datasets
    Outputs a CSV with related data
    '''
    fields = clean_zillow_data()
    mapped_fields = map_city_data(fields)
    complete_data = housingprice_mean_2019(mapped_fields)
    filepath = pathlib.Path(__file__).parent /"zillow_cleaned_complete.csv"
    complete_data.to_csv(filepath, index=False)
    return print("Zillow CSV Complete")


def clean_zillow_data():
    '''
    Load zillow housingdata as a pandas database.
    Segment to just 2019 data and to the City of Chicago
    Returns database of this data
    '''
    filename = pathlib.Path(__file__).parent /"Datasets/ZillowHousing.csv"
    df = pd.read_csv(filename)
    fields = df[["State", "City", "CountyName","RegionName", "1/31/19",
                 "2/28/19", "3/31/19", "4/30/19", "5/31/19", "6/30/19",
                 "7/31/19", "8/31/19", "9/30/19", "10/31/19",
                 "11/30/19", "12/31/19"]]
    fields.State = fields.State.astype("string")
    fields.State = fields.State.str.lower()
    fields = fields.loc[fields.State == 'il']
    fields = fields.loc[fields.CountyName == 'Cook County']
    fields = fields.rename(columns = {'RegionName': 'Zipcode'})
    fields.Zipcode = fields.Zipcode.astype("string")
    fields.Zipcode = fields.Zipcode.str.replace(r"d{4}", r"0$&")
    fields.City = fields.City.str.lower()
    return fields


def map_city_data(df):
    '''
    Imports a list of official zipcodes from the City of Chicago, matches
    the zipcodes in a dataframe to the official list.
    Takes any official zipcodes that may have a different city name listed
    reclassifies them to chicago and returns dataframe segmented to Chicago.
    '''
    clean_zipfile = pathlib.Path(__file__
                        ).parent /"Datasets/Chicago Precinct by Zip Code.csv"
    clean_zip = pd.read_csv(clean_zipfile)
    zip_clean = set(clean_zip["Zipcode"])
    gov_zips = list(zip_clean)

    for i, val in enumerate(gov_zips):
        gov_zips[i] = str(val)
    real_zip = set(df.Zipcode[df.City == "chicago"])

    missingzip = []
    for val in gov_zips:
        if val not in real_zip:
            missingzip.append(str(val))
    for missing in missingzip:
        df.City[df.Zipcode == missing] = "chicago"
    df = df.loc[df.City == "chicago"]
    return df


def housingprice_mean_2019(df):
    '''
    Take all 2019 median housing prices and average them, to avoid 
    impact of outliers.
    Returns dataframe of just zipcodes and average housing prices.
    '''
    df["2019avprice"] = df.loc[:,["1/31/19", "2/28/19", "3/31/19",
                                        "4/30/19", "5/31/19", "6/30/19", 
                                        "7/31/19","8/31/19", "9/30/19",
                                        "10/31/19", "11/30/19", "12/31/19"]
                                        ].agg("mean", axis=1)
    complete_data = df[["Zipcode","2019avprice"]]
    return complete_data


