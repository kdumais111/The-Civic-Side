import geopandas
import pathlib

# Create Zipcode to Ward and Precinct
# Written By Katherine Dumais


def build_zip_precinct_csv():
    """
    Runs cleaning function written below to take shape files of zipcode
    and precinct and join them to find overlap between wards, their
    individual precincts and zipcodes.
    Creates a csv with this info.
    """
    filename = (
        pathlib.Path(__file__).parent / "Datasets/Shape Files/Boundaries"
        " - Ward Precincts (2012-2022)/"
        "geo_export_c1120613-195d-4306-"
        "86e8-8406a30ee539.shp"
    )
    zipfile = (
        pathlib.Path(__file__).parent / "Datasets/Shape Files/Boundaries "
        "- ZIP Codes/geo_export_332ca498-"
        "ebe6-474b-a4a4-174998ba8dba.shp"
    )
    Map_Zip_to_Precinct(filename, zipfile)
    return "zip precinct csv complete"


def Map_Zip_to_Precinct(filename, zipfile):
    """
    Creates file path for Map_Zip_to_Precinct function
    """
    precincts = geopandas.read_file(filename)
    zipfile = (
        pathlib.Path(__file__).parent / "Datasets/Shape Files/Boundaries"
        " - ZIP Codes/geo_export_332ca498-"
        "ebe6-474b-a4a4-174998ba8dba.shp"
    )
    zips = geopandas.read_file(zipfile)
    overlap = geopandas.sjoin(precincts, zips)
    trimmed_overlap = overlap[["ward", "precinct", "zip"]]
    return trimmed_overlap.to_csv(
        pathlib.Path(__file__).parent / "clean_zipcode_precinct.csv", index=False
    )
