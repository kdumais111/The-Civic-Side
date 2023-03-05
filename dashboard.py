from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import geopandas as gpd
from urllib.request import urlopen
import json

# Figures are represented as trees with named nodes called "attributes". 
# The root node of the tree has three top-level attributes: data, layout and frames.

#Import idea taken from Stephania and Project APWhy
zip_url = "https://data.cityofchicago.org/api/geospatial/gdcf-axmw?method=export&format=GeoJSON"
with urlopen(zip_url) as response:
    zipcodes = json.load(response)

app = Dash(external_stylesheets=[dbc.themes.YETI])

df = pd.read_csv("merged.csv")
shape_file = "Cleaning/Datasets/zip_geojson.geojson"

# fig = px.choropleth(df, geojson=shape_file, locations="zip", 
#                     featureidkey="properties.zip", 
#                     color="votingrates", 
#                     projection="mercator")



fig = px.choropleth_mapbox(df, geojson=zipcodes, locations="zip", featureidkey="properties.zip",
                           color="votingrates", mapbox_style="carto-positron", center={"lat":41.8, "lon": -87.75, }
                   )

fig.update_geos(fitbounds="locations", visible=False)

button1 =  dict(method = "restyle",
                args = [{'z': [ df["votingrates"] ] }],
                label = "Voting Rates")
button2 =  dict(method = "restyle",
                args = [{'z': [ df["complaintcounts"] ]}],
                label = "3-1-1 Complaints")
button3 =  dict(method = "restyle",
                args = [{'z': [ df["2019avprice"] ]}],
                label = "Average Housing Prices")

fig.update_layout(width=700,
                  coloraxis_colorbar_thickness=23,
                  coloraxis_colorbar_title_text=None,   
                  updatemenus=[dict(y=0.9,
                                    x=0.275,
                                    xanchor='right',
                                    yanchor='top',
                                    active=0,
                                    buttons=[button1, button2, button3],
                                    )
                              ])

app.layout = html.Div(
    [html.H1("THE CIVIC SIDE"),
     html.H3("By Katherine Dumais and Francesca Vescia"),
     html.P("We began this project to look at..."),
     dbc.Row([dcc.Dropdown(['NYC', 'MTL', 'SF'], 'NYC', id='demo-dropdown')]),
     dbc.Row(
    [
    dbc.Col(
        dcc.Graph(id="1", figure=fig)),
    dbc.Col(
        dcc.Graph(id="2", figure=fig))
    ]),
    dbc.Row(),
     ]
)
#@app.callback(
#    Output('dd-output-container', 'children'),
#    Input('demo-dropdown', 'value')
#)
#def update_table():
#    pass

app.run_server(debug=False)

# https://plotly.com/python/choropleth-maps/#using-geopandas-data-frames
# https://plotly.com/python/mapbox-county-choropleth/
# https://community.plotly.com/t/creating-a-dropdown-slider-for-a-choropleth-map-with-plotly-express/49370
# https://plotly.com/python/hover-text-and-formatting/