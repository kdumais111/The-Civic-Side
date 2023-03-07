import warnings
import pandas as pd
import pathlib
import plotly.express as px
import plotly.graph_objects as go

#Graphs
#This Module Creates our Civic Side Dashboard Graphs
#Campaigns function written by Francesca Vescia
#Other functions written by Katherine Dumais

warnings.simplefilter("ignore")



def make_cloropleth(df, df_revised, zipcodes, color, default):
    '''
    Creates a cloropleth map that is customizable by color
    Inputs:
        df- Pandas dataframe containing data to visualize
        df_revised- pandas dataframe without hospital zips
        color (str) - color scheme to use
        default (str) - Default view for map

    Returns figure
    '''
    fig = px.choropleth_mapbox(df, geojson=zipcodes, locations="zip",
                               featureidkey="properties.zip", color=default,
                               mapbox_style="carto-positron", custom_data=["zip"],
                                center={"lat":41.8, "lon": -87.75,},
                                color_continuous_scale=color)


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
                    args = [{'z': [ df["avg_donation"] ]}],
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

    fig.update_traces(hovertemplate = '<br>Zip=%{customdata[0]}<br>Count=%{z}')

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
                                                 button5, button6],)])
    return fig


def make_top_5(zipcode=None):
    '''
    Creates a table with the top 5 complaints per zipcode
    Inputs:
    Zipcode- String of Chicago Zipcode
    Returns Figure
    '''
    top5 = pd.read_csv( pathlib.Path(__file__).parent\
                      /"the_polis/311_topcomplaints_byzip.csv")
    if zipcode is None:
        data = top5.groupby("SR_TYPE").sum().sort_values(
            by='complaintcounts', ascending=False).iloc[0:5].reset_index()
    else:
        data = top5[top5["ZIP_CODE"] == zipcode]

    complaints = go.Figure(go.Bar(
                    x=list(data["SR_TYPE"]),
                    y=list(data["complaintcounts"]),
                    orientation='v'))
    complaints.update_traces(marker_color="lightblue")
    complaints.update_layout(title="Top Five 311 Complaints")

    return complaints


def make_complaint_counts(df, zipcode=None):
    '''
    Build a table of total complaint counts per zip.
    Inputs:
    df- dataframe that contains complaint counts
    zipcode- string zipcode value
    Returns: chart with complaint counts by zipcode and
    in aggregate
    '''
    if zipcode is None:
        data = df.complaintcounts.sum()
    else:
        data = df.complaintcounts[df.zip == zipcode]

    complaints_count = go.Figure(data = [go.Table(
    header=dict(values=["2019 311 Calls"],
                line_color = 'white',
                fill_color = 'lightblue',
                align = ['left','center'],
                font=dict(color = 'black', size = 16),
                ),
    cells=dict(values=[data],
            font = dict(color ='black', size = 16),
            fill_color = 'white',
            align = 'center'
            )),
    ])
    complaints_count.update_layout(height=int(250))
    return complaints_count


def make_wards_precincts(zipcode=None):
    '''
    Give a list of wards per zipcode
    '''
    wards = pd.read_csv(pathlib.Path(__file__).parent\
                         /"the_polis/clean_zipcode_precinct.csv")
    data = wards.sort_values(by=["ward","precinct"])
    if zipcode is None:
        data = data[["ward","precinct"]].drop_duplicates()
    else:
        data = data[["ward","precinct"]][data["zip"] == zipcode]

    wards = go.Figure(data=[go.Table(
    header = dict(values=["Wards", "Precincts"],
                line_color='white',
                fill_color='lightgrey',
                align=['left','center'],
                font=dict(color='black', size=16),
                ),
    cells = dict(values=[data["ward"],data["precinct"]],
            font = dict(color ='black', size = 13),
            fill_color = 'white',
            align = 'center'
            )),
    ])
    wards.update_layout(height = int(400),
                        title = "What are the Voting Districts represented?")
    return wards


def contributions_table(zipcode = None):
    '''
    Creates a table with campaign contributions data
    '''
    by_zip = pd.read_json(pathlib.Path(__file__).parent\
                           /"campaigns/contributions/contributions_by_zip.json")

    if zipcode is None:
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
    contributions.update_layout(height=int(400), 
                                title="2019 Mayoral Campaign Contributions")
    return contributions
