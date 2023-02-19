import sys
import requests
import lxml.html
import json

# 2019 Chicago Mayoral Election Candidates
# Lori Lightfoot
# Toni Preckwinkle
# Bill Daley
# Willie Wilson
# Susana Mendoza
# Amara Enyia 
# Jerry Joyce 
# Gery Chico
# Paul Vallas

# Step 1: Use Committee Search to identify relevant committee(s)
    # https://www.elections.il.gov/CampaignDisclosure/CommitteeSearch.aspx
# Step 2: Search Contributions by Committee using committee ID
    # https://www.elections.il.gov/CampaignDisclosure/ContributionSearchByCommittees.aspx

# Committee Contributions
lightfoot = "https://www.elections.il.gov/CampaignDisclosure/ContributionSearchByCommittees.aspx?txtCmteName=qdCXN%2bWEQVzcbMUcLdISNaZwV0sGyXpQBXmBGD8YxPvNaBdp%2bVkmi3ohvhDwn4X5&ddlCmteNameSearchType=%2fOm8zAJ7f4ioTTB90BLGGijKP5NjRbIx&ddlVendorState=Ry707kcsXsM%3d&ddlContributionType=wOGh3QTPfKqV2YWjeRmjTeStk426RfVK&ddlState=Ry707kcsXsM%3d&ddlFiledDateTime=Ry707kcsXsM%3d&ddlFiledDateTimeThru=Ry707kcsXsM%3d"
preckwinkle = "https://www.elections.il.gov/CampaignDisclosure/ContributionSearchByCommittees.aspx?txtCmteID=lvxI1oriDX%2fNCtJ%2bxXEGOQ%3d%3d&ddlVendorState=Ry707kcsXsM%3d&ddlContributionType=wOGh3QTPfKqV2YWjeRmjTeStk426RfVK&ddlState=Ry707kcsXsM%3d&ddlFiledDateTime=Ry707kcsXsM%3d&ddlFiledDateTimeThru=Ry707kcsXsM%3d"
daley = "https://www.elections.il.gov/CampaignDisclosure/ContributionSearchByCommittees.aspx?txtCmteID=IQzjndNn%2fRXmTukG876bSQ%3d%3d&ddlVendorState=Ry707kcsXsM%3d&ddlContributionType=wOGh3QTPfKqV2YWjeRmjTeStk426RfVK&ddlState=Ry707kcsXsM%3d&ddlFiledDateTime=Ry707kcsXsM%3d&ddlFiledDateTimeThru=Ry707kcsXsM%3d"
wilson = "https://www.elections.il.gov/CampaignDisclosure/ContributionSearchByCommittees.aspx?txtCmteID=Qtlm%2fWgGpfXWLRtdOkw2pg%3d%3d&ddlVendorState=Ry707kcsXsM%3d&ddlContributionType=wOGh3QTPfKqV2YWjeRmjTeStk426RfVK&ddlState=Ry707kcsXsM%3d&ddlFiledDateTime=Ry707kcsXsM%3d&ddlFiledDateTimeThru=Ry707kcsXsM%3d"
mendoza = "https://www.elections.il.gov/CampaignDisclosure/ContributionSearchByCommittees.aspx?txtCmteID=eWtTbCTKYHT231hljVf3xg%3d%3d&ddlVendorState=Ry707kcsXsM%3d&ddlContributionType=wOGh3QTPfKqV2YWjeRmjTeStk426RfVK&ddlState=Ry707kcsXsM%3d&ddlFiledDateTime=Ry707kcsXsM%3d&ddlFiledDateTimeThru=Ry707kcsXsM%3d"
enyia = "https://www.elections.il.gov/CampaignDisclosure/ContributionSearchByCommittees.aspx?txtCmteID=Ekfpg7pb8tLqFA9CzmCxdQ%3d%3d&ddlVendorState=Ry707kcsXsM%3d&ddlContributionType=wOGh3QTPfKqV2YWjeRmjTeStk426RfVK&ddlState=Ry707kcsXsM%3d&ddlFiledDateTime=Ry707kcsXsM%3d&ddlFiledDateTimeThru=Ry707kcsXsM%3d"
joyce = "https://www.elections.il.gov/CampaignDisclosure/ContributionSearchByCommittees.aspx?txtCmteID=qY2cPeWqHz1dftBZWCXIyQ%3d%3d&ddlVendorState=Ry707kcsXsM%3d&ddlContributionType=wOGh3QTPfKqV2YWjeRmjTeStk426RfVK&ddlState=Ry707kcsXsM%3d&ddlFiledDateTime=Ry707kcsXsM%3d&ddlFiledDateTimeThru=Ry707kcsXsM%3d"
chico = "https://www.elections.il.gov/CampaignDisclosure/ContributionSearchByCommittees.aspx?txtCmteID=2kUSbsNeCpF%2bI%2fN%2faOXDlg%3d%3d&ddlVendorState=Ry707kcsXsM%3d&ddlContributionType=wOGh3QTPfKqV2YWjeRmjTeStk426RfVK&ddlState=Ry707kcsXsM%3d&ddlFiledDateTime=Ry707kcsXsM%3d&ddlFiledDateTimeThru=Ry707kcsXsM%3d"
vallas = "https://www.elections.il.gov/CampaignDisclosure/ContributionSearchByCommittees.aspx?txtCmteID=%2bFNNULG1ToBmbnvIwDP25A%3d%3d&ddlVendorState=Ry707kcsXsM%3d&ddlContributionType=wOGh3QTPfKqV2YWjeRmjTeStk426RfVK&ddlState=Ry707kcsXsM%3d&ddlFiledDateTime=Ry707kcsXsM%3d&ddlFiledDateTimeThru=Ry707kcsXsM%3d"


def get_contributions(url):
    """
    Takes a URL to a committee contributions page and returns
    a list of dictionaries (one dictionary per contribution).
    """
    response = requests.get(url, verify=False)
    root = lxml.html.fromstring(response.text)
    rows = root.cssselect("#ContentPlaceHolder1_gvContributions tr")
    del rows[0] # 1st row is header --> drop

    contributions = []

    for row in rows:
        contribution = {}
        cells = row.cssselect("td") # some cells have <br> --> use text_content()
        contribution["donor"] = str(cells[0].text_content()) # name & address
        contribution["amount"] = cells[1].text
        contribution["received_date"] = cells[2].text
        contribution["reported_date"] = cells[3].text
        contribution["contribution_type"] = cells[4].text
        contribution["received_by"] = cells[4][1].text
        # TODO: add Description, Vendor Name, and Vendor Address
        # once I've figured out how to access records with those fields

# Selector for "Page Size" > "All" - is there a way to have my scraper "click" this?
#ContentPlaceHolder1_gvContributions_pnlLeft_phPagerTemplate_gvContributions_PageSize > option:nth-child(7)

# Notes:
# Contributions can be flagged a refunds in the description column - how should we handle refunds?