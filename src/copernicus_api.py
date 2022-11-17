import cdsapi

c = cdsapi.client()

c.retrieve(
    'cams-solar-radiation-timeseries',
    {
        'sky_type': 'observed_cloud',
        'location': {
            'latitude': 47.853,
            'longitude': 9.136,
        },
        'altitude': '-999.',
        'date': '2017-01-01/2018-12-31',
        'time_step': '1hour',
        'time_reference': 'universal_time',
        'format': 'csv',
    },
    'download.csv')

# source: copernicus data store; https://ads.atmosphere.copernicus.eu/cdsapp#!/dataset/cams-solar-radiation-timeseries?tab=form
