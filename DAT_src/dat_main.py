"""
Temporary main file for the automatized demand assessment tool (DAT) developed in WP2 of the OptiMG project
"""

#%% Import packages

import ramp
import pandas as pd
import numpy as np
import copy
from  time import perf_counter


#%% Read survey results from Kobo

# Connect to Kobo Rest API

# Save results in dataframe

#%% Create RAMP input

"""
Based on each survey response, an instance of the RAMP user class for each relevant demand will be generated

In the OptiMG DAT we generate timeseries for the following demands:
1. Household electrical appliances [kWh_elec]
- one load profile of electrical energy demand caused by household devices
2. Business electrical appliances [kWh_elec]
3. Cooking energy demand [kWh_therm]
4. Agro-processing energy demand [kWh_mech]
5. Drinking water demand [l]
6. Service water demand [l]

"""

#%% Create RAMP use cases

"""
The modeling of the 6 timeseries is performed separately in independent RAMP use cases
- Analog to my (Johann's) masters thesis, we generate one RAMP use case for every day. 
- RAMPs function of looping through all the days defined for a multi-day UseCase is not used.
- This gives more flexibility in modeling weekly variation and seasonality:
    o By default, RAMP can only model if an appliance is or is not used during a weekday, or weekend day
    -> this approach gives the flexibility to specify if an appliance has a different usage time or usage windows on 
    certain weekdays
    o The change of use of an appliance due to seasonal variation (most relevant for agro-processing and irrigation 
    water)
"""

# Define timeseries for which demand profiles will be generated
days_nr = 3  # Number of days
timeseries = pd.date_range("2018-01-01", periods=days_nr * 24 * 60, freq="Min")  # 2018 starts on Monday
days_timeseries = pd.date_range("2018-01-01", periods=days_nr, freq="D")

# Household electricity demand
# Dummy dict of households with electrical appliances
# Will be read from surveys
households_dict = {
    'low_income_hh': {
        'num_users': 20,
        'appliances': {
            'indoor_lights':
                {
                    'num_app': 3,  # number of appliances
                    'power': 10,  # power in W
                    'usage_window_1': [5*60, 7*60],  # usage window [start, end] in min of the day
                    'usage_window_2': [20*60, 23*60],  # usage window [start, end] in min of the day
                    'daily_usage_time': 2*60,  # daily time of use in min
                    'func_cycle': 10  # minimal duration of switch on event in minutes
                 },
            'outdoor_lights':
                {
                    'num_app': 3,  # number of appliances
                    'power': 15,  # power in W
                    'usage_window_1': [5*60, 7*60],  # usage window [start, end] in min of the day
                    'usage_window_2': [20*60, 23*60],  # usage window [start, end] in min of the day
                    'daily_usage_time': 2*60,  # daily time of use in min
                    'func_cycle': 10  # minimal duration of switch on event in minutes
                 }
        }


    },
    'medium_income_hh': {
        'num_users': 40,
        'appliances': {
            'indoor_lights':
                {
                    'num_app': 3,  # number of appliances
                    'power': 10,  # power in W
                    'usage_window_1': [5*60, 7*60],  # usage window [start, end] in min of the day
                    'usage_window_2': [20*60, 23*60],  # usage window [start, end] in min of the day
                    'daily_usage_time': 2*60,  # daily time of use in min
                    'func_cycle': 10  # minimal duration of switch on event in minutes
                 }
        }

    },

    'high_income_hh': {
        'num_users': 40,
        'appliances': {
            'indoor_lights':
                {
                    'num_app': 3,  # number of appliances
                    'power': 10,  # power in W
                    'usage_window_1': [5 * 60, 7 * 60],  # usage window [start, end] in min of the day
                    'usage_window_2': [20 * 60, 23 * 60],  # usage window [start, end] in min of the day
                    'daily_usage_time': 2 * 60,  # daily time of use in min
                    'func_cycle': 10  # minimal duration of switch on event in minutes
                }
        }
    },
}



# Dummy dict of metadata input provided by the admin and not read from surveys
# Includes data on random variability of model parameters specific to certain appliances
admin_input = {
    'appliance_metadata': {  # metadata specific to "standard" appliances (reported by select in survey)
        'indoor_lights': {
            'daily_use_variability': 0.2,
            'usage_window_variability': 0.2
        }
    }
}

#%%
start= perf_counter()
# Create dict to store generated RAMP user instances
ramp_users_dict = {}
# Loop through every household survey respondent.
for household_name, household_data in households_dict.items():
    # Create user instance for this household survey respondent
    new_user = ramp.User(
        user_name=household_name,
        num_users=household_data['num_users']
    )

    # Add appliances to this user.
    for appliance_name, appliance_data in household_data['appliances'].items():  # Loop through user's appliances

        # Get appliance's metadata
        # TODO consider merging appliance's metadata earlier into the household->appliances dict? Decide.
        appliance_metadata = admin_input['appliance_metadata'][appliance_name]

        # Get appliance's usage windows
        # Definition of usage windows is extremely messy. Propose to RAMP core to define usage windows in list?
        usage_windows = [  # Create list of usage windows
            appliance_data['usage_window_1'] if 'usage_window_1' in appliance_data.keys() else None,
            appliance_data['usage_window_2'] if 'usage_window_2' in appliance_data.keys() else None,
            appliance_data['usage_window_3'] if 'usage_window_3' in appliance_data.keys() else None,
        ]
        num_usage_windows = sum(x is not None for x in usage_windows)  # Count how many windows are not none

        # Add appliance to user instance
        new_user.add_appliance(
            name=appliance_name,  # Name of the appliance as specified in survey response
            number=appliance_data['num_app'],  # Number of identical appliances of this type that this user owns
            power=appliance_data['power'],  # Power of the appliance (actual power drawn, not nominal power)

            func_time=appliance_data['daily_usage_time'],  # Total time of use per day
            time_fraction_random_variability=appliance_metadata['daily_use_variability'],  # Fraction of daily usage time which is subject to random variability
            func_cycle=appliance_data['func_cycle'],

            # Check if windows are given and set them
            # If no windows are specified,
            num_windows = num_usage_windows,
            window_1=usage_windows[0],
            window_2=usage_windows[1],
            window_3=usage_windows[2],

            random_var_w=appliance_metadata['usage_window_variability']
        )

    # Add deepcopy of user instance to ramp_user_dict
    ramp_users_dict[household_name] = copy.deepcopy(new_user)

# Create RAMP use_case
hh_elec_use_case = ramp.UseCase(
    name='household_elec',
    users=list(ramp_users_dict.values())
)

print('Time to generate one use_case: ' + str(perf_counter()-start))

#%% Run the use case

# Dict to store generated load profiles
hh_load_profiles = {}

# Calculate peak time range of this use case
peak_time_range = hh_elec_use_case.calc_peak_time_range()

# Loop through all days of this use_case
day_counter = 0
for day in days_timeseries:

    # Loop through all user instances (= user types)
    for user in hh_elec_use_case.users:
        # Create dict entry for every user
        hh_load_profiles[user.user_name] = {}

        # Loop through each user of this user type
        for _ in range(user.num_users):

            # Loop through user's appliances
            for appliance in user.App_list:
                # Check if there is no dict entry for this appliance yet in the load profiles dict
                if appliance.name not in hh_load_profiles[user.user_name]:  #
                    # Create dict entry for this appliance with pre-allocated 2D numpy array
                    # 1440 (minute) timesteps for each day to be simulated
                    hh_load_profiles[user.user_name][appliance.name] = np.zeros((days_nr, 1440))

                # --- Generate appliance load profile ---
                # Generate a daylong profile with 1-min resolution (1440 time steps) for this appliance
                # Load profile is not returned but saved in the appliance's daily_use attribute
                appliance.generate_load_profile(
                    prof_i=0,  # Day of the year in RAMP core. Not used here, thus always 0
                    peak_time_range=peak_time_range,
                    day_type=0,  # Day type in RAMP core. Not used here, thus always 0 (weekday)
                    # -> different days are represented by different use_cases.
                    power=appliance.power  # Power of the appliance. Used to consider seasonal variation in RAMP core.
                )

                # Add this appliance load profile to the day's load profile
                hh_load_profiles[user.user_name][appliance.name][day_counter] += appliance.daily_use

    # Increase day counter
    day_counter += 1
    print(day_counter)


#%% Create dataframe from dict
# Loop through all users for which load profiles where generated
for user, user_lp in hh_load_profiles.items():
    # Loop through every appliance
    for app, app_lp in user_lp.items():
        # Turn 2D numpy array: [day_of_timeframe, min_of_day] into 1D numpy array: [min_of_timeframe]
        user_lp[app] = app_lp.reshape(1, len(app_lp) * 1440).squeeze()

    # Create dataframe of load profiles of this user's appliances
    hh_load_profiles[user] = pd.DataFrame(user_lp)

# Concat dataframe of each user in multi-column dataframe
hh_lp_df = pd.concat(hh_load_profiles, axis=1)

#%%
print(hh_lp_df.head())

#%% Analysis of results:
# Aggregate by appliances (column index level 1)
app_lp = hh_lp_df.T.groupby(level=1).sum().T  # (groupby axis=1 is deprecated-> therefore the double transpose)

# Aggregate by user types (column index level 0)
users_lp = hh_lp_df.T.groupby(level=0).sum().T

