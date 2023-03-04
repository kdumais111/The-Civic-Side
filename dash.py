import plotly.express as px
import geopandas as gpd


# Plotly example
# df = px.data.election() WHAT IS .election() ???
# geo_df = gpd.GeoDataFrame.from_features(
#     px.data.election_geojson()["features"]
# ).merge(df, on="district").set_index("district")

# fig = px.choropleth(geo_df,
#                    geojson=geo_df.geometry,
#                    locations=geo_df.index,
#                    color="Joly",
#                    projection="mercator")
# fig.update_geos(fitbounds="locations", visible=False)
# fig.show()


# https://plotly.com/python/choropleth-maps/#using-geopandas-data-frames
# https://plotly.com/python/mapbox-county-choropleth/
# https://community.plotly.com/t/creating-a-dropdown-slider-for-a-choropleth-map-with-plotly-express/49370
# https://plotly.com/python/hover-text-and-formatting/
