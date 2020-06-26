import zipfile
import os
import rasterio
from rasterio.plot import show #for plotting
from rasterio.warp import calculate_default_transform, reproject, Resampling #for reprojecting
import rasterio.mask
import fiona
from osgeo import gdal

#unzip files
with zipfile.ZipFile('Output/Elevation.zip', 'r') as zip_ref:
    zip_ref.extractall('Output/Elevation')
#find the name of the raster file related to elevation
file=os.listdir('Output/Elevation')
#open file with rasterio
dataset = rasterio.open('Output/Elevation/'+file[0])
#print dataset crs
print(dataset.crs)
#plot dataset
show(dataset)

######clip raster layer by mask layer#######
with fiona.open('Input/Namajavira_4326.shp', "r") as shapefile:
    shapes = [feature["geometry"] for feature in shapefile]
out_image, out_transform = rasterio.mask.mask(dataset, shapes, crop=True)
out_meta = dataset.meta

out_meta.update({"driver": "GTiff", #name of the desired format driver
                 "height": out_image.shape[1], #number of rows
                 "width": out_image.shape[2], #number of columns
                 "transform": out_transform}) #tranform is the affine transformation matrix, which associates pixels to locations

with rasterio.open("RGB.byte.masked.tif", "w", **out_meta) as dest: #to write the raster on a new file
    dest.write(out_image)

dataset = rasterio.open('RGB.byte.masked.tif')
show(dataset)


###########create regular mesh of points############
import numpy as np
import geopandas as gpd
import pandas as pd
# define the lower and upper limits for x and y
Area=gpd.read_file('Input/Namajavira_4326.shp')
minX, minY, maxX, maxY = Area.geometry.total_bounds
# create one-dimensional arrays for x and y
x = np.arange(minX, maxX, (maxX-minX)/200)
y = np.arange(minY, maxY, (maxY-minY)/200)
# create the mesh based on these arrays
X, Y = np.meshgrid(x, y)
X = X.reshape((np.prod(X.shape),))
Y = Y.reshape((np.prod(Y.shape),))
coords = zip(X, Y)
dataframe=pd.DataFrame(columns=['X','Y','Elevation'])
dataframe['X']=X
dataframe['Y']=Y
i=0
for val in dataset.sample(coords):
 dataframe.loc[i,'Elevation']=val
 i=i+1

#########reproject layer to a cartesian coordinate system#############
def reproject_et(inpath, outpath, new_crs):
    dst_crs = new_crs # CRS for web meractor

    with rasterio.open(inpath) as src:
        transform, width, height = calculate_default_transform(
            src.crs, dst_crs, src.width, src.height, *src.bounds)
        kwargs = src.meta.copy()
        kwargs.update({
            'crs': dst_crs,
            'transform': transform,
            'width': width,
            'height': height
        })

        with rasterio.open(outpath, 'w', **kwargs) as dst:
            for i in range(1, src.count + 1):
                reproject(
                    source=rasterio.band(src, i),
                    destination=rasterio.band(dst, i),
                    src_transform=src.transform,
                    src_crs=src.crs,
                    dst_transform=transform,
                    dst_crs=dst_crs,
                    resampling=Resampling.nearest)

reproject_et('Output/Elevation/'+file[0], 'Output/Elevation/reprojected.tif', 'EPSG:3857')


#########calculate slope#########
# using GDAL library https://gdal.org/programs/gdaldem.html: need to be in carteisna coordinate system
def calculate_slope(DEM):
    gdal.DEMProcessing('slope.tif', DEM, 'slope') #expressed in degrees (? need to check)
    with rasterio.open('slope.tif') as dataset:
        show(dataset)
        slope=dataset.read(1) #the read methods returns an array of all the pixel values
    return slope
slope=calculate_slope('Output/Elevation/reprojected.tif') #in this way an array is returned

#usign richDEM library. It could be useful also for computing river flow accumulation
# https://www.earthdatascience.org/tutorials/get-slope-aspect-from-digital-elevation-model/
# https://richdem.readthedocs.io

######road distance? #######