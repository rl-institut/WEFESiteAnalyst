import os
from datetime import datetime, timedelta
from tempfile import mkstemp
import logging
import numpy as np
import xarray as xr
import cdsapi

def _format_cds_request_area(
    latitude_span=None, longitude_span=None, grid=None
):
    """
    Format the area between two given latitude and longitude spans in order
    to submit a CDS request
    The grid convention of the era5 HRES is used with a native resolution of
    0.28125 deg. For NetCDF format, the data is interpolated to a regular
    lat/lon grid with 0.25 deg resolution.
    In this grid the earth is modelled by a sphere with radius
    R_E = 6367.47 km. Latitude values in the range [-90, 90] relative to the
    equator and longitude values in the range [-180, 180]
    relative to the Greenwich Prime Meridian [1].
    References:
    [1] https://confluence.ecmwf.int/display/CKB/ERA5%3A+What+is+the+spatial+reference
    [2] https://confluence.ecmwf.int/display/UDOC/Post-processing+keywords
    :param latitude_span: (list of float) formatted as [N,S]. The span is
        between North and South latitudes (relative to the equator). North
        corresponds to positive latitude [2].
    :param longitude_span: (list of float) formatted as [W,E]. The span is
        between East and West longitudes (relative to the Greenwich meridian).
        East corresponds to positive longitude [2].
    :param grid: (list of float) provide the latitude and longitude grid
        resolutions in deg. It needs to be an integer fraction of 90 deg [2].
    :return: a dict containing the grid and, if `latitude_span` and/or
        `longitude_span` were specified, the area formatted for a CDS request
    """

    answer = {}

    # Default value of the grid
    if grid is None:
        grid = [0.25, 0.25]

    if latitude_span is not None and longitude_span is not None:
        area = [
            latitude_span[0],
            longitude_span[0],
            latitude_span[1],
            longitude_span[1],
        ]
    elif latitude_span is None and longitude_span is not None:
        area = [90, longitude_span[0], -90, latitude_span[1]]
    elif latitude_span is not None and longitude_span is None:
        area = [latitude_span[0], -180, latitude_span[1], 180]
    else:
        area = []

    # Format the 'grid' keyword of the CDS request as
    # lat_resolution/lon_resolution
    answer["grid"] = "%.2f/%.2f" % (grid[0], grid[1])

    # Format the 'area' keyword of the CDS request as N/W/S/E
    if area:
        answer["area"] = "/".join(str(e) for e in area)

    return answer


def _format_cds_request_position(latitude, longitude, grid=None):
    """
    Reduce the area of a CDS request to a single GIS point on the earth grid
    Find the closest grid point for the given longitude and latitude.
    The grid convention of the era5 HRES is used here with a native
    resolution of 0.28125 deg. For NetCDF format the data is interpolated to a
    regular lat/lon grid with 0.25 deg resolution. In this grid the earth is
    modelled by a sphere with radius R_E = 6367.47 km. latitude values
    in the range [-90, 90] relative to the equator and longitude values in the
    range [-180, 180] relative to the Greenwich Prime Meridian [1].
    References:
    [1] https://confluence.ecmwf.int/display/CKB/ERA5%3A+What+is+the+spatial+reference
    [2] https://confluence.ecmwf.int/display/UDOC/Post-processing+keywords
    :param latitude: (number) latitude in the range [-90, 90] relative to the
        equator, north correspond to positive latitude.
    :param longitude: (number) longitude in the range [-180, 180] relative to
        Greenwich Meridian, east relative to the meridian correspond to
        positive longitude.
    :param grid: (list of float) provide the latitude and longitude grid
        resolutions in deg. It needs to be an integer fraction of 90 deg [2].
    :return: a dict containing the grid and the area formatted for a CDS
        request
    """

    # Default value of the grid
    if grid is None:
        grid = [0.25, 0.25]

# Find the nearest point on the grid corresponding to the given latitude
    # and longitude
    grid_point = xr.Dataset(
        {
            "lat": np.arange(90, -90, -grid[0]),
            "lon": np.arange(-180, 180.0, grid[1]),
        }
    ).sel(lat=latitude, lon=longitude, method="nearest")

    # Prepare an area which consists of only one grid point
    lat, lon = [float(grid_point.coords[s]) for s in ("lat", "lon")]
    return _format_cds_request_area(
        latitude_span=[lat, lat], longitude_span=[lon, lon], grid=grid
    )

    # recycled from https://github.com/oemof/feedinlib/blob/dev/feedinlib/cds_request_tools.py