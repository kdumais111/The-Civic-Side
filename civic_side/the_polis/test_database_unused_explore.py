import pandas as pd
import pathlib
import sqlite3

# Exploratory Code to Create a Database that Compares Precinct
# to Zipcode and Ward to zipcode spreadsheets
# By Katherine Dumais

# Create connection and table
connection = sqlite3.connect("presinctsward.db")
connection.row_factory = sqlite3.Row
cursor = connection.cursor()
# https://datatofish.com/pandas-dataframe-to-sql/

# Add in precinct data
cursor.execute("CREATE TABLE IF NOT EXISTS presincts(Zipcode text, PRECINCT_NAME text)")
csvfile = (
    pathlib.Path("zillowcleaning.py").parent
    / "Datasets/Chicago Precinct by Zip Code.csv"
)
df = pd.read_csv(csvfile)
df.to_sql("presincts", connection, if_exists="replace", index=False)
cursor.execute("SELECT Zipcode from presincts")

# Add in wards
cursor.execute("CREATE TABLE IF NOT EXISTS wards(Zip text, ward text)")
wardfile = (
    pathlib.Path("zillowcleaning.py").parent
    / "Datasets/Chicago Ward Names by Zip Code.csv"
)
wardpd = pd.read_csv(wardfile)
wardpd.to_sql("wards", connection, if_exists="replace", index=False)
cursor.execute("SELECT * from wards")
cursor.execute(
    "SELECT presincts.Zipcode, presincts.PRECINCT_NAME, wards.ward"
    "FROM presincts JOIN wards ON presincts.Zipcode = wards.Zip"
)
parks = []
for row in cursor.fetchall():
    parks.append(row)
    for d in row:
        print(d)
