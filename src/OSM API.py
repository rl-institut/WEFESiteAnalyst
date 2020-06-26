'''
The Overpass API of OSM uses Overpass QL or Overpass XML language.
Python packages have been developed to work as wrapper/ interface and to automatically download data

########OSMNX##########
OSMNX: https://geoffboeing.com/2016/11/osmnx-python-street-networks/
    https://github.com/gboeing/osmnx
    https://wiki.openstreetmap.org/wiki/Overpass_API/Language_Guide
it is a package specifically developed for downloading streets networks from OSM

drive - get drivable public streets (but not service roads)
drive_service - get drivable streets, including service roads
walk - get all streets and paths that pedestrians can use (this network type ignores one-way directionality)
bike - get all streets and paths that cyclists can use
all - download all non-private OSM streets and paths
all_private - download all OSM streets and paths, including private-access ones
'''
import osmnx as ox
import geopandas as gpd
# get the streets network from the name of a place
# place = 'Piedmont, California, USA'
# G = ox.graph_from_place(place, network_type='drive')
# ox.save_graph_shapefile(G, filepath='Output/piedmont')

# get the streets network from a bounding box
Area=gpd.read_file('Input/Namajavira_4326.shp')
minx, miny, maxx, maxy = Area.geometry.total_bounds
G = ox.graph_from_bbox(miny, maxy, minx, maxx, network_type='drive')
ox.save_graph_shapefile(G, filepath='Output/streets')

############ Requests from query ###########

import requests
import json
overpass_url = "http://overpass-api.de/api/interpreter"
overpass_query = """
[out:json];
area["ISO3166-1"="DE"][admin_level=2];
(node["amenity"="biergarten"](area);
 way["amenity"="biergarten"](area);
 rel["amenity"="biergarten"](area);
);
out center;
"""
response = requests.get(overpass_url,
                        params={'data': overpass_query})
data = response.json()

import numpy as np
import matplotlib.pyplot as plt
# Collect coords into list
coords = []
for element in data['elements']:
  if element['type'] == 'node':
    lon = element['lon']
    lat = element['lat']
    coords.append((lon, lat))
  elif 'center' in element:
    lon = element['center']['lon']
    lat = element['center']['lat']
    coords.append((lon, lat))
# Convert coordinates into numpy array
X = np.array(coords)
plt.plot(X[:, 0], X[:, 1], 'o')
plt.title('Biergarten in Germany')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.axis('equal')
plt.show()


#download power lines ####
# https://wiki.openstreetmap.org/wiki/Power
# https://towardsdatascience.com/loading-data-from-openstreetmap-with-python-and-the-overpass-api-513882a27fd0
# https://openinframap.org/#2/26/12 where data are rendered

from pandas.io.json import json_normalize
overpass_query = """
[out:json];
[bbox:50.6,7.0,50.8,7.3];
(
 way["power"="line"];
  way["power"="cable"];
  way["power"="minor_line"];
);
out geom;
"""
response = requests.get(overpass_url,
                        params={'data': overpass_query})
data = response.json()
df = json_normalize(data['elements'])
for element in data['elements']:
  if element['type'] == 'node':
    lon = element['lon']
    lat = element['lat']
    coords.append((lon, lat))



import numpy as np
import matplotlib.pyplot as plt
# Collect coords into list
coords = []
for element in data['elements']:
  if element['type'] == 'node':
    lon = element['lon']
    lat = element['lat']
    coords.append((lon, lat))
  elif 'center' in element:
    lon = element['center']['lon']
    lat = element['center']['lat']
    coords.append((lon, lat))
# Convert coordinates into numpy array
X = np.array(coords)
plt.plot(X[:, 0], X[:, 1], 'o')
plt.title('Biergarten in Germany')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.axis('equal')
plt.show()

