    import pandas as pd
    import pathlib
    filename = pathlib.Path("zillowcleaning.py").parent /"datasets/ZillowHousing.csv"
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
    
    clean_zipfile= pathlib.Path("zillowcleaning.py").parent /"datasets/Chicago Precinct and Ward Names by Zip Code.csv"
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
    clean_data.to_csv("datasets/zillow_cleaned_complete.csv")


    #    Chicago_Zipcodes= [60601,60602,60603,60604,60605,60606,60607,60608,60609,60610,60611,60612,60613,60614,60615,60616,60617,60618,60619,60620,60621,60622,60623,60624,60625,60626,60628,60629,60630,60631,60632,60633,60634,60636,60637,60638,60639,60640,60641,60642,60643,60644,60645,60646,60647,60649,60651,60652,60653,60654,60655,60656,60657,60659,60660,60661,60706,60707,60827]
