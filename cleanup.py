import json
import re
# import datetime

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
        # month, day, year = contribution["received_date"].split("/")
        # contribution["datetime_date"] = datetime.date(int(year), int(month), int(day))
        # TypeError: Object of type date is not JSON serializable --> TODO: decide how to handle dates

    with open(clean_file, "w") as cf:
        json.dump(contributions, cf, indent=1) 

# Reference
# https://www.geeksforgeeks.org/pattern-matching-python-regex/
# https://www.educative.io/answers/how-to-convert-a-string-to-a-date-in-python
# https://www.programiz.com/python-programming/datetime/strptime
# https://docs.python.org/3/library/datetime.html?highlight=datetime#strftime-strptime-behavior

