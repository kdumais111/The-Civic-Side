# By Francesca Vescia
import json
import lxml.html

def get_contributions(saved_page):
    """
    Takes an HTML file saved from a committee contributions page and returns
    a list of dictionaries (one dictionary per contribution).
    """
    with open(saved_page) as sp:
        root = lxml.html.fromstring(sp.read())

    rows = root.cssselect("#ContentPlaceHolder1_gvContributions tr")

    del rows[0] # header
    del rows[-2:] # page numbers

    contributions = []

    for row in rows:
        contribution = {}
        cells = row.cssselect("td")
        # .text only returns the first line of text if a cell has breaks
        # .text_content() returns a lxml.etree._ElementUnicodeResult
        contribution["donor_name"] = cells[0].text
        # donor_info is name, address, and sometimes occupation and employer
        # clean() in cleanup.py deletes name and extracts address
        contribution["donor_info"] = str(cells[0].text_content())
        contribution["amount"] = str(cells[1].text_content())
        contribution["received_date"] = str(cells[2].text_content())
        contribution["reported_date"] = str(cells[3].text_content())
        contribution["contribution_type"] = cells[4].text
        contribution["received_by"] = cells[4][1].text
        contribution["description"] = str(cells[5].text_content())
        contribution["vendor_name"] = str(cells[6].text_content())

        contributions.append(contribution)

    return contributions


def save_contributions(contributions, file_name):
    """
    Takes a list of contribution dictionaries and saves them to a JSON file.

    Inputs:
        contributions: lst of strs
        file_name: str
    """
    with open(file_name, "w") as f:
        json.dump(contributions, f, indent=4)
