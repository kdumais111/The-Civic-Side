from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import geopandas as gpd
import pathlib
from urllib.request import urlopen
import json
import plotly.graph_objects as go
from Merging_clean_datasets import execute_data_merge
import numpy as np

# execute_data_merge()

#Import idea taken from Stephania and Project APWhy
zip_url = "https://data.cityofchicago.org/api/geospatial/unjd-c2ca?method=export&format=GeoJSON"
with urlopen(zip_url) as response:
    zipcodes = json.load(response)

app = Dash(external_stylesheets=[dbc.themes.YETI])

#merged dataframe
df = pd.read_csv(pathlib.Path(__file__).parent /"merged.csv")
df = df.round(decimals=2)

#dataframe excluding 60612
df_revised = pd.read_csv(pathlib.Path(__file__).parent /"merged.csv")
df_revised["per1000_complaint"][df_revised["zip"] == 60612] = 0
df_revised = df_revised.round(decimals=2)

def make_cloropleth(color, default):
    '''
    Creates a cloropleth map that is customizable by color 
    Inputs
        color (str) - color scheme to use
        default (str) - Default view for map
    Returns figure
    '''
    fig = px.choropleth_mapbox(df, geojson=zipcodes, locations="zip", featureidkey="properties.zip",
                            color=default, mapbox_style="carto-positron", custom_data=["zip"],
                            center={"lat":41.8, "lon": -87.75,}, color_continuous_scale=color)

    fig.update_geos(fitbounds="locations", visible=False)
    if default == "votingrates":
        button1 =  dict(method = "restyle",
                    args = [{'z': [ df["votingrates"] ], }],
                    label = "Voting Rates (Percentages)")
        button2 = dict(method = "restyle",
                    args = [{'z': [ df["avg_donation"] ]}],
                    label = "Average Donations")
    else:
        button2 =  dict(method = "restyle",
                    args = [{'z': [ df["votingrates"]],
                             'tickformat': ',.0%' }],
                    label = "Voting Rates (Percentages)")
        button1 = dict(method = "restyle",
                    args = [{'z': [ df["avg_donation"] ],
                             'text' : "hello"}],
                    label = "Average Donations")

    button3 =  dict(method = "restyle",
                    args = [{'z': [ df["per1000_complaint"] ]}],
                    label = "311 Complaints per thousand residents")
    button4 = dict(method = "restyle",
                    args = [{'z': [ df_revised["per1000_complaint"] ]}],
                    label = "311 Complaints excluding 60612")

    button5 =  dict(method = "restyle",
                    args = [{'z': [ df["2019avprice"] ]}],
                    label = "Average Housing Prices")
    
    button6 = dict(method = "restyle",
                    args = [{'z': [ df["num_donations"] ]}],
                    label = "Number of Donations")


    
    fig.update_traces(hovertemplate='<br>Zip=%{customdata[0]}<br>Count=%{z}')

    fig.update_layout(width=700, height=700,
                    coloraxis_colorbar_thickness=23,
                    coloraxis_colorbar_title_text=None,   
                    updatemenus=[dict( y=0.9,
                                        x=0.275,
                                        xanchor='right',
                                        yanchor='top',
                                        active=0,
                                        buttons=[button1, button2,
                                                 button3, button4, 
                                                 button5, button6],
                                        )
                                ])
    return fig

def make_top_5(zipcode=None):
    '''
    Creates a table with the top 5 complaints per zipcode
    '''
    top5=pd.read_csv( pathlib.Path(__file__).parent\
                      /"the_polis/311_topcomplaints_byzip.csv")
    if zipcode == None:
        data = top5.groupby("SR_TYPE").sum().sort_values(
            by='complaintcounts', ascending=False).iloc[0:5].reset_index()
    else:
        data = top5[top5["ZIP_CODE"] == zipcode]
    complaints = go.Figure(go.Bar(
                    x=list(data["SR_TYPE"]),
                    y=list(data["complaintcounts"]),
                    orientation='v'))
    complaints.update_traces(marker_color="lightblue")

    return complaints

def make_complaint_counts(zipcode=None):
    '''
    Build a table of total complaint counts per zip.
    '''
    if zipcode == None:
        data = df.complaintcounts.sum()
    else: 
        data = df.complaintcounts[df.zip == zipcode]
    
    complaints_count = go.Figure(data=[go.Table(
    header=dict(values=["2019 311 Calls"],
                line_color='white',
                fill_color='lightblue',
                align=['left','center'],
                font=dict(color='black', size=16),
                ),
    cells=dict(values=[data],
            font = dict(color ='black', size = 16),
            fill_color='white',
            align='center'
            )),
    ])
    complaints_count.update_layout(height=int(400))
    return complaints_count

def make_wards_precincts(zipcode=None):
    '''
    Give a list of wards per zipcode
    '''
    wards = pd.read_csv(pathlib.Path(__file__).parent\
                         /"the_polis/clean_zipcode_precinct.csv")
    data = wards.sort_values(by=["ward","precinct"])
    if zipcode == None:
        data = data[["ward","precinct"]].drop_duplicates()
    else:    
        data = data[["ward","precinct"]][data["zip"] == zipcode]
    
    wards = go.Figure(data=[go.Table(
    header=dict(values=["Wards", "Precincts"],
                line_color='white',
                fill_color='lightgrey',
                align=['left','center'],
                font=dict(color='black', size=16),
                ),
    cells=dict(values=[data["ward"],data["precinct"]],
            font = dict(color ='black', size = 13),
            fill_color='white',
            align='center'
            )),
    ])
    wards.update_layout(height=int(400))
    return wards


def contributions_table(zipcode = None):
    '''
    Creates a table with campaign contributions data 
    '''
    by_zip = pd.read_json(pathlib.Path(__file__).parent\
                           /"campaigns/contributions/contributions_by_zip.json")

    if zipcode == None:
        total_donated = round(by_zip["total_donated"].sum(), 2)
        num_donations = by_zip["num_donations"].sum()
        avg_donation = round((total_donated / num_donations), 2)
        min_donation =  0.01
        max_donation = by_zip["max_donation"].max()
    else:
        total_donated = round(by_zip["total_donated"][by_zip.zip == zipcode], 2)
        num_donations = by_zip["num_donations"][by_zip.zip == zipcode]
        avg_donation = round(by_zip["avg_donation"][by_zip.zip == zipcode], 2)
        min_donation =  by_zip["min_donation"][by_zip.zip == zipcode]
        max_donation = by_zip["max_donation"][by_zip.zip == zipcode]

    col_labels = ["Total Donated", "Number of Donations", "Average Donation", 
                "Smallest Donation", "Largest Donation"]
        
    contributions = go.Figure(data = [go.Table(
        header = dict(values = col_labels,
                    line_color = 'white',
                    fill_color = 'darkseagreen',
                    align = ['center','center'],
                    font = dict(color ='black', size = 16),
                    ),
        cells = dict(values = [[total_donated], [num_donations], [avg_donation],
                                [min_donation], [max_donation]],
                fill_color = 'white',
                align = 'center')) 
        ])
    return contributions

app.layout = html.Div(
    [
    dbc.Row([html.H1("THE CIVIC SIDE")]),
    dbc.Row([html.H3("By Katherine Dumais and Francesca Vescia")]),
    dbc.Row([html.P([html.Br(), " The Civic Side dashboard visualizes civic engagement across Chicago,"
            " specifically how election engagement and civic service utilization,"
            " measured here by ",
            html.A("311 calls for non-emergency city services", 
               href="https://www.chicago.gov/city/en/depts/311.html"),
            ", vary by zip code and income (as proxied by housing prices)."
            " We analyzed 2019 data to look at these relationships during the last completed "
            " mayoral election cycle. Explore our findings below!",html.Br()])]),
    dbc.Row([html.P(        
        [ "Questions? Comments? ",
        html.A("Drop us a note!", 
               href="mailto:kdumais@uchicago.edu,fvescia@uchicago.edu")])]),
    dbc.Row([html.H3("Compare how Chicago residents engage with government across zip codes:")]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(id="cloropleth1", figure=make_cloropleth("blues","votingrates")),
            html.H6("Note: 60612 contains the largest conglomeration of hospitals downtown", style={'textAlign': ['top', 'center'], 'margin-left' : '150px', 'margin-top': '0px', 'font-size': "8"})]),
        dbc.Col(
            dcc.Graph(id="cloropleth2", figure=make_cloropleth("greens","avg_donation")))
            ]),
    dbc.Row([html.H3("Learn more about Chicago and its zip codes!")]),
    dbc.Row([html.P("Tables default to city-wide statistics. Select a zip code from the drop-down to narrow results.")]),
    dbc.Row([html.Br()]),
    dbc.Row([dcc.Dropdown(['City of Chicago'] + list(df["zip"].unique()),'City of Chicago', id='dropdown')]),

    dbc.Row(
            dcc.Graph(id="total complaints", figure=make_complaint_counts(zipcode=None))),
    dbc.Row([
        dbc.Col(
            dcc.Graph(id="top5", figure=make_top_5(zipcode=None))),
        dbc.Col(
            dcc.Graph(id="wards", figure=make_wards_precincts(zipcode=None) )),
    ]),
    dbc.Row(
            dcc.Graph(id="campaigns", figure=contributions_table(zipcode = None))),
    ],
    style={
        'margin-left' : '60px',
        'width' : '90%',
        'height' : '60px',
        'borderWidth' : '1px',
        'borderRadius' : '5px',
        'textAlign' : 'left'}
)

@app.callback(
     [Output("total complaints", 'figure'),
      Output("top5", 'figure'),
      Output("campaigns", 'figure'),
      Output("wards", 'figure')],
     Input('dropdown', 'value')
 )
def update_table(value):
    if value != "City of Chicago":
        return (make_complaint_counts(value), make_top_5(value),
                contributions_table(value), make_wards_precincts(value))
    else:
        return (make_complaint_counts(), make_top_5(), 
                contributions_table(), make_wards_precincts())
    

app.run_server(debug=True, port=8070)

# https://plotly.com/python/choropleth-maps/#using-geopandas-data-frames
# https://plotly.com/python/mapbox-county-choropleth/
# https://community.plotly.com/t/creating-a-dropdown-slider-for-a-choropleth-map-with-plotly-express/49370
# https://plotly.com/python/hover-text-and-formatting/
# https://community.plotly.com/t/dash-html-a-tags-within-html-p-tags/18367
# https://medium.com/codex/how-to-create-a-dashboard-with-a-contact-form-using-python-and-dash-ee3aacffd349