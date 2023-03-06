
# HTML from BOE website
chico_page = "civic_side/campaigns/saved_pages/chico.html"
daley_page = "civic_side/campaigns/saved_pages/daley.html"
enyia_page = "civic_side/campaigns/saved_pages/enyia.html"
joyce_page = "civic_side/campaigns/saved_pages/joyce.html"
lightfoot_page = "civic_side/campaigns/saved_pages/lightfoot.html"
mendoza_page = "civic_side/campaigns/saved_pages/mendoza.html"
preckwinkle_page = "civic_side/campaigns/saved-pages/preckwinkle.html"
vallas_page = "civic_side/campaigns/saved_pages/vallas.html"
wilson_page = "civic_side/campaigns/saved_pages/wilson.html"

# Destination files for raw scraped data
chico_raw = "/civic_side/campaigns/contributions/chico.json"
daley_raw = "/civic_side/campaigns/contributions/daley.json"
enyia_raw = "/civic_side/campaigns/contributions/enyia.json"
joyce_raw = "/civic_side/campaigns/contributions/joyce.json"
lightfoot_raw = "/civic_side/campaigns/contributions/lightfoot.json"
mendoza_raw = "/civic_side/campaigns/contributions/mendoza.json"
preckwinkle_raw = "/civic_side/campaigns/contributions/preckwinkle.json"
vallas_raw = "/civic_side/campaigns/contributions/vallas.json"
wilson_raw = "/civic_side/campaigns/contributions/wilson.json"

PAGES_TO_SCRAPE = [
    (chico_page, chico_raw),
    (daley_page, daley_raw),
    (enyia_page, enyia_raw),
    (joyce_page, joyce_raw),
    (lightfoot_page, lightfoot_raw),
    (mendoza_page, mendoza_raw),
    (preckwinkle_page, preckwinkle_raw),
    (vallas_page, vallas_raw),
    (wilson_page, wilson_raw)
]

START = "11/26/2018" # Start of 2019 candidate filing period
END = "12/31/2019" # End of 2019 election cycle

ZIP_INTS = [60647, 60622, 60642, 60611, 60610, 60654, 60614, 60615, 60653,
    60616, 60609, 60605, 60604, 60649, 60619, 60637, 60621, 60620,
    60617, 60628, 60827, 60643, 60633, 60608, 60632, 60629, 60638,
    60636, 60652, 60655, 60623, 60644, 60624, 60612, 60607, 60639,
    60651, 60661, 60634, 60707, 60618, 60641, 60657, 60625, 60630,
    60606, 60602, 60603, 60601, 60656, 60646, 60659, 60645, 60626,
    60660, 60640, 60631, 60706, 60613]

ZIP_STRS = ['60647','60622','60642', '60611', '60610', '60654', '60614', '60615', '60653',
    '60616', '60609', '60605', '60604', '60649', '60619', '60637', '60621', '60620',
    '60617', '60628', '60827', '60643', '60633', '60608', '60632', '60629', '60638',
    '60636', '60652', '60655', '60623', '60644', '60624', '60612', '60607', '60639',
    '60651', '60661', '60634', '60707', '60618', '60641', '60657', '60625', '60630',
    '60606', '60602', '60603', '60601', '60656', '60646', '60659', '60645', '60626',
    '60660', '60640', '60631', '60706', '60613']


# References (relevant dates):
# Illinois State Board of Elections 2019 Election and Campaign Finance Calendar
# available at https://www.elections.il.gov/Main/Publications.aspx
# 10 ILCS 5/9-1.9 available at https://www.ilga.gov/legislation/ilcs/fulltext.asp?DocName=001000050K9-1.9