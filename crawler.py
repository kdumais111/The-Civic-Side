import sys
import requests
import lxml.html
import json


def get_contributions(url):
    """
    Takes a URL to a committee contributions page and returns
    a list of dictionaries (one dictionary per contribution).
    """
    # open & read file
    saved_page = "enyia.html"
    with open(saved_page) as sp:
        root = lxml.html.fromstring(sp.read())
    
    rows = root.cssselect("#ContentPlaceHolder1_gvContributions tr")
    
    header = rows[0]
    col_names = []
    for col in header:
        col_names.append(col.text_content())
    del rows[0]

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