import pandas as pd
import pathlib
# Data downloaded exclusively for 2019 
df = pd.read_csv("https://30122-public.s3.amazonaws.com/311_2019.csv")
df= df[["SR_TYPE", "ZIP_CODE", "WARD", "PRECINCT"]]

#Narrow to Zip and find counts of 311 complaints 
df["ZIP_CODE"]= pd.to_numeric(df["ZIP_CODE"], errors='coerce')
zip=df["ZIP_CODE"].value_counts(dropna=True).to_frame('complaintcounts').reset_index()
zip=zip.rename(columns={'index' : 'zipcode'})
zip["zipcode"]=zip["zipcode"].astype(int)

# Import population numbers for 2019 
filename = pathlib.Path("311 Dataset Cleaning.py").parent /"Datasets/Chicago_Population_Counts.csv"
pop = pd.read_csv(filename)
pop = pop[pop['Year']==2019]

#Make numeric
pop = pop[['Geography','Population - Total']]
pop['Geography'] = pd.to_numeric(pop['Geography'], errors='coerce')
pop['Population - Total'] = pop['Population - Total'].str.replace('[^0-9]', '', regex=True).astype('int64')
pop = pop.dropna()
pop['Geography']= pop['Geography'].astype(int)

#search only actual chicago zipcodes provided by govt, merge tables. 
zip= zip[zip["zipcode"].isin (pop['Geography'])]
pop= pop.rename(columns= {'Geography':"zipcode"})
zip = zip.merge(pop, how='left', on='zipcode')
zip["per1000_compaint"]= zip["complaintcounts"]/zip['Population - Total']*1000
zip.to_csv("311_complaint_count.csv")


#Top 5 complaints
df = df.dropna()
df["ZIP_CODE"] = df["ZIP_CODE"].astype(int)
df= df[df["ZIP_CODE"].isin (pop['zipcode'])]
comp_by_zip=[]
for zipcode, zipcodegroup in df[["SR_TYPE","ZIP_CODE"]].groupby("ZIP_CODE"):
    comp_by_zip.append(zipcodegroup.value_counts(
    sort=True, dropna=True).to_frame('complaintcounts').iloc[0:5])

complaints= pd.concat(comp_by_zip) 
complaints.to_csv('311_topcomplaints_byzip.csv', header=True)



