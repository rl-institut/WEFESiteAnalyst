"""
Temporary main file for the automatized demand assessment tool (DAT) developed in WP2 of the OptiMG project
"""

#%% Import packages

import pandas as pd
from DAT_src.ramp_control import RampControl


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
        'months_present': [1, 2, 3, 4, 7, 8, 9, 10, 11, 12],  # months at which this user is present in the settlement
        'working_days': [0, 1, 2, 3, 4, 5, 6],  # days at which this user uses his appliances
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
        'months_present': [1, 2, 3, 4, 7, 8, 9, 10, 11, 12],  # months at which this user is present in the settlement
        'working_days': [0, 1, 2, 3, 4, 5, 6],  # days at which this user uses his appliances
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
        'months_present': [1, 2, 3, 4, 7, 8, 9, 10, 11, 12],  # months at which this user is present in the settlement
        'working_days': [0, 1, 2, 3, 4, 5, 6],  # days at which this user uses his appliances
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
        },
        'outdoor_lights': {
            'daily_use_variability': 0.3,
            'usage_window_variability': 0.1
        }
    }
}

#%%
ramp_control = RampControl(365, '2018-01-01')
use_cases_list = ramp_control.generate_electric_appliances_use_cases(households_dict, admin_input)
app_lp = ramp_control.run_use_cases(use_cases_list, households_dict)


#%% Analysis of results:
# Aggregate by appliances (column index level 1)
app_lp.head()

