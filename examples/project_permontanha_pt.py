import os
# download era5 data climate data

os.chdir("../src/")
import era5
os.chdir("../examples/")


# ERA5
# enter coordinates
latitude = 37.134986
longitude = -8.853894

# set start and end date (end date will be included
# in the time period for which data is downloaded)
start_date, end_date = '2020-12-31', '2021-12-31'  # time in UTC choose start date one day before time of interest
# for position east of 0° meridian for covering all hours of interest

# set variable set to download

variable = "wefesiteanalyst"
target_file = 'ERA5_wefesiteanalyst.nc'

ds = era5.get_era5_data_from_datespan_and_position(
    variable=variable,
    start_date=start_date, end_date=end_date,
    latitude=latitude, longitude=longitude,
    target_file=target_file)


# plot irradiance
# import matplotlib.pyplot as plt
# weather_df.loc[:, ['BHI', 'DHI']].plot(title='Irradiance')
# plt.xlabel('Time')
# plt.ylabel('Irradiance in $W/m^2$')

# Alternative: Load existing existing climate data file
# import pandas as pd
