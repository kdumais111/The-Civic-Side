import json
import re

def clean(json_file, clean_file):
    """
    Takes a json file of campaign contributions data (json_file), cleans the data,
    and saves it to a new json file (clean_file).
    """
    with open(json_file) as jf:
        contributions = json.load(jf)
    
    for contribution in contributions:
        contribution["donor_info"] = contribution["donor_info"].replace(contribution["donor_name"], "")
        contribution["donor_name"] = contribution["donor_name"].title()
        contribution["donor_info"] = contribution["donor_info"].strip()
        if re.search(",\s+\D{2}\s+\d{5}", contribution["donor_info"]):
            state_zip = re.search(",\s+\D{2}\s+\d{5}", contribution["donor_info"]).group()
            contribution["state"] = re.search("[A-Z]{2}", state_zip).group()
            contribution["zip"] = re.search("\d{5}", state_zip).group()
        else:
            contribution["state"] = None
            contribution["zip"] = None
        contribution["amount"] = float(contribution["amount"].replace("$", "").replace(",", ""))
        
    with open(clean_file, "w") as cf:
        json.dump(contributions, cf, indent=1) 

# Reference
# https://www.geeksforgeeks.org/pattern-matching-python-regex/

