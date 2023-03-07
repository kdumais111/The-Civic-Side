import warnings
import json
import pathlib
from urllib.request import urlopen
import pandas as pd
from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
from graphs import make_cloropleth, make_top_5,\
    make_complaint_counts, make_wards_precincts, contributions_table

#Dashboard Layout
#This Module Creates our Civic Side Dashboard
#This Code was completed by Katherine Dumais


warnings.simplefilter("ignore")

#Import idea taken from Stephania and Project APWhy
zip_url = "https://data.cityofchicago.org/api/geospatial/"\
            "unjd-c2ca?method=export&format=GeoJSON"
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

#App Layout

app.layout = html.Div(
    [
    dbc.Row([html.H1("THE CIVIC SIDE")]),
    dbc.Row([html.H3("By Katherine Dumais and Francesca Vescia")]),
    dbc.Row([html.P([html.Br(),
            " The Civic Side dashboard visualizes civic engagement across Chicago,"
            " specifically how election engagement and civic service utilization,"
            " measured here by "
            "311 calls for non-emergency city services"
            ", vary by zip code and income (as proxied by housing prices)."
            " We analyzed 2019 data to look at these relationships"
            " during the last completed"
            " mayoral election cycle.  ", 
            html.A("Read more about our data and methods",
                   href="https://github.com/uchicago-capp122-spring23/30122-project-the-civic-side/blob/main/README.md"),
            " and access",
            html.A(" detailed intstructions for interacting with the dashboard",
                   href="https://github.com/uchicago-capp122-spring23/30122-project-the-civic-side/blob/main/README.md"),            
            " in the Civic Side GitHub respository,"
            " or dive straight in and explore our findings below!",html.Br()])]),
    dbc.Row([html.P(
        [ "Questions? Comments? ",
        html.A("Drop us a note!",
               href="mailto:kdumais@uchicago.edu,fvescia@uchicago.edu")])]),
    dbc.Row([html.H3("Compare how Chicago residents engage with government "
                     "across zip codes:")]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(id="cloropleth1", figure=make_cloropleth(df, df_revised, zipcodes,
                                                                "blues","votingrates")),
            html.H6("Note: 60612 contains the largest conglomeration of hospitals downtown",
                    style={'textAlign': ['top', 'center'], 'margin-left' : '150px',
                           'margin-top': '0px', 'font-size': "8"}),html.Br(),html.Br()]),
        dbc.Col(
            dcc.Graph(id="cloropleth2", figure=make_cloropleth(df, df_revised, zipcodes,
                                                                "greens","avg_donation")))
            ]),
    dbc.Row([html.H3("Learn more about Chicago and its zip codes!")]),
    dbc.Row([html.P("Tables default to city-wide statistics."
                    " Select a zip code from the drop-down to narrow results.")]),
    dbc.Row([html.Br()]),
    dbc.Row([dcc.Dropdown(['City of Chicago'] + list(df["zip"].unique()),
                          'City of Chicago', id='dropdown')]),

    dbc.Row(
            dcc.Graph(id="total complaints", figure=make_complaint_counts(df))),
    dbc.Row([
        dbc.Col(
            dcc.Graph(id="top5", figure=make_top_5())),
        dbc.Col(
            dcc.Graph(id="wards", figure=make_wards_precincts())),
    ]),
    dbc.Row(
            dcc.Graph(id="campaigns", figure=contributions_table())),
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
    '''
    Update Graphs with the correct zipcode,
        zip(str) - zipcode
        City of Chicago is None.
    returns filtered graphs
    '''
    if value != "City of Chicago":
        return (make_complaint_counts(df, value), make_top_5(value),
                contributions_table(value), make_wards_precincts(value))
    return (make_complaint_counts(df), make_top_5(),
                contributions_table(), make_wards_precincts())


app.run_server(debug=True, port=8070)


# Resources Used:
# https://community.plotly.com/t/dash-html-a-tags-within-html-p-tags/18367
# https://medium.com/codex/how-to-create-a-dashboard-with-a-contact-form-using-python-and-dash-ee3aacffd349


