from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import geopandas as gpd
from urllib.request import urlopen
import json
import plotly.graph_objects as go

# Figures are represented as trees with named nodes called "attributes". 
# The root node of the tree has three top-level attributes: data, layout and frames.

#Import idea taken from Stephania and Project APWhy
zip_url = "https://data.cityofchicago.org/api/geospatial/gdcf-axmw?method=export&format=GeoJSON"
with urlopen(zip_url) as response:
    zipcodes = json.load(response)

app = Dash(external_stylesheets=[dbc.themes.YETI])

df = pd.read_csv("merged.csv")

# fig = px.choropleth(df, geojson=shape_file, locations="zip", 
#                     featureidkey="properties.zip", 
#                     color="votingrates", 
#                     projection="mercator")

def make_cloropleth(color):
    '''
    Creates a cloropleth map that is customizable by color 
    Color- colorscheme to use
    returns figure
    '''
    fig = px.choropleth_mapbox(df, geojson=zipcodes, locations="zip", featureidkey="properties.zip",
                            color="votingrates", mapbox_style="carto-positron", center={"lat":41.8, "lon": -87.75,}, color_continuous_scale=color)

    fig.update_geos(fitbounds="locations", visible=False)

    button1 =  dict(method = "restyle",
                    args = [{'z': [ df["votingrates"] ] }],
                    label = "Voting Rates")
    button2 =  dict(method = "restyle",
                    args = [{'z': [ df["per1000_compaint"] ]}],
                    label = "3-1-1 Complaints")
    button3 =  dict(method = "restyle",
                    args = [{'z': [ df["2019avprice"] ]}],
                    label = "Average Housing Prices")
    
    button4 = dict(method = "restyle",
                    args = [{'z': [ df["num_donations"] ]}],
                    label = "Number of Donations")
    
    button4 = dict(method = "restyle",
                    args = [{'z': [ df["num_donations"] ]}],
                    label = "Number of Donations")
    button5 = dict(method = "restyle",
                args = [{'z': [ df["avg_donation"] ]}],
                label = "Average Donations")
    

    fig.update_layout(width=700,
                    coloraxis_colorbar_thickness=23,
                    coloraxis_colorbar_title_text=None,   
                    updatemenus=[dict( y=0.9,
                                        x=0.275,
                                        xanchor='right',
                                        yanchor='top',
                                        active=0,
                                        buttons=[button1, button2, button3, button4, button5],
                                        )
                                ])
    return fig

def make_top_5(zipcode=None):
    '''
    Creates a table with the top 5 complaints per zipcode
    '''

    complaints = go.Figure(data=[go.Table(
        header=dict(values=["Top 5 311 Complaints"],
                    line_color='white',
                    fill_color='lightgrey',
                    align=['left','center'],
                    font=dict(color='black', size=16),
                    ),
        cells=dict(values=[df.complaintcounts],
                fill_color='white',
                align='left')) 
    ])
    return complaints

def make_complaint_counts(zipcode=None):
    '''
    Build a table of total complaint counts per zip
    '''
    if zipcode == None:
        data = df.complaintcounts.sum()
    else: 
        data = df.complaintcounts[df.zip == zipcode]
    
    complaints_count = go.Figure(data=[go.Table(
    header=dict(values=["Number of 311 Complaints"],
                line_color='white',
                fill_color='lightgrey',
                align=['left','center'],
                font=dict(color='black', size=16),
                ),
    cells=dict(values=[data],
            fill_color='white',
            align='left')) 
    ])
    return complaints_count
    

app.layout = html.Div(
    [html.H1("THE CIVIC SIDE"),
     html.H3("By Katherine Dumais and Francesca Vescia"),
     html.P("We began this project to look at..."),
     dbc.Row([dcc.Dropdown(['NYC', 'MTL', 'SF'], 'NYC', id='demo-dropdown')]),
     dbc.Row([
     dbc.Col(
        dcc.Graph(id="cloropleth1", figure=make_cloropleth("blues"))),
     dbc.Col(
        dcc.Graph(id="cloropleth2", figure=make_cloropleth("greens")))
     ]),
     dbc.Row([dcc.Dropdown(['NYC', 'MTL', 'SF'], 'NYC', id='demo-dropdown')]),

     dbc.Row([
        dbc.Col(
            dcc.Graph(id="top5", figure=make_top_5(zipcode=None))),
        dbc.Col(
            dcc.Graph(id="total complaints", figure=make_complaint_counts(zipcode=None)))
     ])
     ]
)
#@app.callback(
#    Output('dd-output-container', 'children'),
#    Input('demo-dropdown', 'value')
#)
#def update_table():
#    pass

app.run_server(debug=True, port=8070)

# https://plotly.com/python/choropleth-maps/#using-geopandas-data-frames
# https://plotly.com/python/mapbox-county-choropleth/
# https://community.plotly.com/t/creating-a-dropdown-slider-for-a-choropleth-map-with-plotly-express/49370
# https://plotly.com/python/hover-text-and-formatting/