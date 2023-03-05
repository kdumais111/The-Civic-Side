from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import geopandas as gpd
from urllib.request import urlopen
import json
import plotly.graph_objects as go

# We need to make sure all libraries above are in Poetry plus jupiter notebooks



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

def make_cloropleth(color, default):
    '''
    Creates a cloropleth map that is customizable by color 
    Inputs
        color (str) - color scheme to use
        default (str) - Default view for map
    Returns figure
    '''
    fig = px.choropleth_mapbox(df, geojson=zipcodes, locations="zip", featureidkey="properties.zip",
                            color=default, mapbox_style="carto-positron", 
                            center={"lat":41.8, "lon": -87.75,}, color_continuous_scale=color)

    fig.update_geos(fitbounds="locations", visible=False)
    if default == "votingrates":
        button1 =  dict(method = "restyle",
                    args = [{'z': [ df["votingrates"] ] }],
                    label = "Voting Rates")
        button5 = dict(method = "restyle",
                    args = [{'z': [ df["avg_donation"] ]}],
                    label = "Average Donations")
    else:
        button5 =  dict(method = "restyle",
                    args = [{'z': [ df["votingrates"] ] }],
                    label = "Voting Rates")
        button1 = dict(method = "restyle",
                    args = [{'z': [ df["avg_donation"] ]}],
                    label = "Average Donations")

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
    

    fig.update_layout(width=700, height=700,
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
    top5=pd.read_csv("Cleaning/311_topcomplaints_byzip.csv")
    if zipcode == None:
        data = top5["SR_TYPE"]
    else: 
        data = top5["SR_TYPE"][top5["ZIP_CODE"] == zipcode]
    complaints = go.Figure(data=[go.Table(
        header=dict(values=["Top 5 311 Complaints"],
                    line_color='white',
                    fill_color='lightgrey',
                    align=['left','center'],
                    font=dict(color='black', size=16),
                    ),
        cells=dict(values=[top5["SR_TYPE"]],
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
    header=dict(values=["2019 311 Calls"],
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
    [
    dbc.Row([html.H1("THE CIVIC SIDE")]),
    dbc.Row([html.H3("By Katherine Dumais and Francesca Vescia")]),
    dbc.Row([html.P([html.Br(),"We began this project to look at civic engagement across Chicago."
            " We wanted to access whether housing price and income, thereby"
            " contributing to the government, and campaign finance contributions"
            " led individuals to engage with city instutions."
            " We analyzed data from 2019 to look at these relationships during the last"
            " election cycle. Our results are shown below!",html.Br()])]),
    dbc.Row([html.P(        
        [ "Any Questions? ",
        html.A("Feel free to drop us a note!", 
               href="mailto:kdumais@uchicago.edu,fvescia@uchicago.edu")])]),
    dbc.Row([html.H3("Compare how residents are engaging with government across zipcodes!")]),
    dbc.Row([
        dbc.Col(
            dcc.Graph(id="cloropleth1", figure=make_cloropleth("blues","votingrates"))),
        dbc.Col(
            dcc.Graph(id="cloropleth2", figure=make_cloropleth("greens","avg_donation")))
    ]),
    dbc.Row([html.H3("Learn more about the individual zipcodes,"
                      " or the city in aggregate!")]),
    dbc.Row([html.Br()]),
    dbc.Row([dcc.Dropdown(['City of Chicago', 'MTL', 'SF'],'City of Chicago', id='dropdown')]),

    dbc.Row([
        dbc.Col(
            dcc.Graph(id="top5", figure=make_top_5(zipcode=None))),
        dbc.Col(
            dcc.Graph(id="total complaints", figure=make_complaint_counts(zipcode=None)))
    ])
    ],
    style={
        'margin-left' : '60px',
        'width' : '90%',
        'height' : '60px',
        'borderWidth' : '1px',
        'borderRadius' : '5px',
        'textAlign' : 'left'}
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
# https://community.plotly.com/t/dash-html-a-tags-within-html-p-tags/18367
# https://medium.com/codex/how-to-create-a-dashboard-with-a-contact-form-using-python-and-dash-ee3aacffd349