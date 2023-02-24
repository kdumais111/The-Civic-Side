import pandas as pd
import pathlib
filename = pathlib.Path("zillowcleaning.py").parent /"Datasets/ZillowHousing.csv"
df = pd.read_csv(filename)

fields = df[["State", "City", "CountyName","RegionName","1/31/19","2/28/19","3/31/19","4/30/19","5/31/19","6/30/19","7/31/19","8/31/19","9/30/19","10/31/19","11/30/19","12/31/19"]]
fields.State= fields.State.astype("string")
fields.State = fields.State.str.lower()
fields= fields.loc[fields.State == 'il']
fields= fields.loc[fields.CountyName == 'Cook County']
fields= fields.rename(columns={'RegionName': 'Zipcode'})
fields.Zipcode = fields.Zipcode.astype("string")
fields.Zipcode = fields.Zipcode.str.replace(r"d{4}", r"0$&")
fields.City = fields.City.str.lower()

clean_zipfile= pathlib.Path("zillowcleaning.py").parent /"datasets/Chicago Precinct by Zip Code.csv"
clean_zip = pd.read_csv(clean_zipfile)
zip_clean=set(clean_zip["Zipcode"])
gov_zips = list(zip_clean)

for i, val in enumerate(gov_zips):
    gov_zips[i]=str(val)
real_zip= set(fields.Zipcode[fields.City=="chicago"])

missingzip= []
for val in gov_zips:
    if val not in real_zip:
        print(val)
        missingzip.append(str(val))

for missing in missingzip:
    fields.City[fields.Zipcode == missing]= "chicago"
fields = fields.loc[fields.City == "chicago"]
fields["2019avprice"]= fields.loc[:,["1/31/19","2/28/19","3/31/19","4/30/19","5/31/19","6/30/19","7/31/19","8/31/19","9/30/19","10/31/19","11/30/19","12/31/19"]].agg("mean",axis=1)
clean_data = fields[["Zipcode","2019avprice"]]
clean_data.to_csv("zillow_cleaned_complete.csv")

