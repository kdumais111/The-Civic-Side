import pandas as pd
import pathlib

#Code Written By Katherine Dumais

def create_311_clean_csvs():
    '''
    Creates a CSV for complaint counts per 1,000 people by zipcode
    and a CSV documenting the top complaints for each zipcode using
    the related functions below
    '''
    df = make_311dataframe()
    complaints = complaint_counts(df)
    population_vals = read_clean_pop_data()
    complaints_csv(complaints, population_vals)
    find_top_five(df, population_vals)


def make_311dataframe():
    '''
    Downloads and filters the 311 data to solely look at location and 
    complaint type.
    Returns filtered dataset
    '''
    # Data downloaded exclusively for 2019 
    df = pd.read_csv("https://30122-public.s3.amazonaws.com/311_2019.csv")
    df = df[["SR_TYPE", "ZIP_CODE", "WARD", "PRECINCT"]]
    df["ZIP_CODE"] = pd.to_numeric(df["ZIP_CODE"], errors = 'coerce')
    return df


def complaint_counts(df):
    '''
    Finds the count of 311 complaints by zipcode
    Returns a dataframe of counts by zipcode.
    '''
    zip = df["ZIP_CODE"].value_counts(dropna=True).to_frame('complaintcounts'
                                                            ).reset_index()
    zip = zip.rename(columns = {'index':'zipcode'})
    zip["zipcode"] = zip["zipcode"].astype(int)
    return zip


def read_clean_pop_data():
    '''
    Reads and cleans a set of population data by zipcode provided by the city. 
    Returns a dataframe of zipcodes and population numbers.
    '''
    # Import population numbers for 2019 
    f = pathlib.Path(__file__).parent /"Datasets/Chicago_Population_Counts.csv"
    pop = pd.read_csv(f)
    pop = pop[pop['Year'] == 2019]

    # Make into integers and clean out non-number characters
    # Geography is what 311 calls zipcode.
    pop = pop[['Geography','Population - Total']]
    pop['Geography'] = pd.to_numeric(pop['Geography'], errors = 'coerce')
    pop['Population - Total'] = pop['Population - Total'].str.replace(
        '[^0-9]', '', regex=True).astype('int64')
    pop = pop.dropna()
    pop['Geography'] = pop['Geography'].astype(int)
    pop = pop.rename(columns = {'Geography':"zipcode"})
    return pop


def complaints_csv(zip, pop):
    '''
    Takes population to zipcode and 311 complaint count data.
    - Narrows 311 zipcodes to exclusively Chicago/ Cleans out typo'ed zipcodes.
    - Merges dataframes
    - Finds Complaint Counts per 100,000 people
    - Creates a CSV for complaint counts 
    '''

    zip = zip[zip['zipcode'].isin (pop['zipcode'])]
    zip = zip.merge(pop, how = 'left', on = 'zipcode')
    zip['per1000_compaint'] = (zip['complaintcounts'] /
                                zip["Population - Total"] * 1000)
    
    zip.to_csv(pathlib.Path(__file__).parent /'_311_complaint_count.csv',
                index= False)
    return print('311 data csv created')

def find_top_five(df, pop):
    '''
    Uses 311 dataframe (df) and dataframe of population to zipcode (pop) to
    find top 5 complaints by zipcode. Creates a CSV of top 5 complaints by zip.
    '''
    df = df.dropna()
    df["ZIP_CODE"] = df["ZIP_CODE"].astype(int)
    df = df[df["ZIP_CODE"].isin (pop['zipcode'])]
    comp_by_zip = []
    for _ , zipcodegroup in df[["SR_TYPE","ZIP_CODE"]].groupby("ZIP_CODE"):
        comp_by_zip.append(zipcodegroup.value_counts(
        sort = True, dropna = True).to_frame('complaintcounts').iloc[0:5])
    complaints = pd.concat(comp_by_zip) 
    complaints.to_csv(pathlib.Path(__file__).parent /'311_topcomplaints_byzip.csv'\
                      , header = True)
    return print( '311_top complaints data created')


