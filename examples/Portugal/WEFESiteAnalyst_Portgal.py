# imports
# import os
# import pandas as pd
import folium
import geopandas as gpd
# import files from source
# os.chdir("../../src/")
# import era5
# os.chdir("../examples/Portugal")
# initiate earth engine
# import ee

# Trigger the authentication flow.
# ee.Authenticate()

# Initialize the library.
# ee.Initialize()

# provide case study name
name = 'permontanha'
# coordinates
lat = 37.134986
lon = -8.853894
# set center of maps and zoom level
center = [lat, lon]
zoom = 13
# create a folium elevation map
elv_map = folium.Map(location=center, zoom_start=zoom)

# Load the shapefile / better: create shapefile from points
shpfile = gpd.read_file('pp_geometry.shp')
geometry = shpfile.to_file('pp_geometry.geojson', driver='GeoJSON')

# Add the shapefile to the map
folium.GeoJson(geometry, name='geojson').add_to(elv_map)

print(elv_map)

# Add the elevation layer to the map
elevation = ee.Image('USGS/GMTED2010').visualize(min=0, max=4000, palette=['yellow', 'red'])
map_id = elevation.getMapId()
folium.TileLayer(
    tiles=ee.data.getTileUrl(map_id, lon, lat, zoom),
    attr='Google Earth Engine',
    overlay=True,
    name='Elevation'
).add_to(elv_map)


