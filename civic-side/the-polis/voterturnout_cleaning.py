import pandas as pd
import pathlib

#Written By Katherine Dumais

def clean_voter_turnout():
    '''
    Load voter turnout csv containing 50 individual tables on
    turnout on the precinct level. Integrate into one dataset. 
    Return integrated dataset as a csv.
    '''
    #load file
    filename = pathlib.Path(__file__).parent /"Datasets/voting rates.csv"
    df = pd.read_csv(filename, header=None, skiprows=[0, 1, 2, 3, 4, 5, 6, 7])
    
    #set column numbers to know where individual pieces of 
    #the individual tables are without classifying
    df = df[[0, 1, 2, 3, 4]]

    #find start and end of tables and key values.
    wardheaders = df[df[0].str.match(r"WARD", na=False)]
    tableend = df[df[0].str.match(r"Total", na=False)]
    headers = df[df[0].str.match(r"Precinct", na=False)]
    counter = 0

    #integrate individual tables to one, drop unneeded rows
    for ward in wardheaders.index:
        counter += 1
        for end in tableend.index:
            df.loc[ward:end,4] = counter
    df.loc[1,4] = "ward"

    #delete unnecessary header rows, clean and export
    df = df.drop(wardheaders.index)
    df = df.drop(tableend.index)
    df = df.drop(headers.index[1:])
    df[3] = df[3].str.replace(r'[ %]',"")
    df = df.dropna()
    df.iloc[0,0]= "precinct"
    df.to_csv(pathlib.Path(__file__).parent /"voterturnout.csv",
              index=False, header=False)
    return print("Voter turnout csv complete")

