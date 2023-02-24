import pandas as pd
import pathlib

filename = pathlib.Path("Voter_Counts.py").parent /"Datasets/voting rates.csv"
df = pd.read_csv(filename, header=None, skiprows=[0,1,2,3,4,5,6,7])
df=df[[0,1,2,3,4]]
wardheaders= df[df[0].str.match(r"WARD", na= False)]
tableend= df[df[0].str.match(r"Total", na= False)]
headers= df[df[0].str.match(r"Precinct", na= False)]
counter=0
for ward in wardheaders.index:
    counter+=1
    for end in tableend.index:
        df.loc[ward:end,4]= counter
df.loc[1,4]="ward"
df=df.drop(wardheaders.index)
df=df.drop(tableend.index)
df=df.drop(headers.index[1:])
df.to_csv("voterturnout.csv")
df.dropna(axis=1, how='any')
