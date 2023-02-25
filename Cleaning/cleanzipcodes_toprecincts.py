import geopandas
import pathlib
filename= pathlib.Path("cleanzipcodes_toprecincts.py").parent /"Datasets/Shape Files/Boundaries - Ward Precincts (2012-2022)/geo_export_c1120613-195d-4306-86e8-8406a30ee539.shp"
precincts = geopandas.read_file(filename)
zipfile = pathlib.Path("cleanzipcodes_toprecincts.py").parent /"Datasets/Shape Files/Boundaries - ZIP Codes/geo_export_332ca498-ebe6-474b-a4a4-174998ba8dba.shp"
zips= geopandas.read_file(zipfile)
overlap= geopandas.sjoin(precincts, zips)
trimmed_overlap = overlap[["ward","precinct","zip"]]
trimmed_overlap.to_csv("clean_zipcode_precinct.csv", index=False)
#how do I make sure these relationships are unique?
#how do I pick shape files? Any way to look without doing a full import?