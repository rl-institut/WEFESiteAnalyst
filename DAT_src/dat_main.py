"""
Temporary main file for the automatized demand assessment tool (DAT) developed in WP2 of the OptiMG project
"""

# Create RAMP input

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


#%% Household electricity demand
# Dummy dict of households with electrical appliances
# Will be read from surveys
households_dict = {
    'low_income_hh': {
        'num_users': 1,
        'months_present': [1, 2, 3, 4, 7, 8, 9, 10, 11, 12],  # months at which this user is present in the settlement
        'working_days': [0, 1, 2, 3, 4, 5, 6],  # days at which this user uses his appliances
        'appliances': {
            'indoor_lights':
                {
                    'num_app': 3,  # number of appliances
                    'power': 10,  # power in W
                    'usage_window_1': [5, 7],  # usage window [start, end] in min of the day
                    'usage_window_2': [20, 23],  # usage window [start, end] in min of the day
                    'daily_usage_time': 2,  # daily time of use in min
                    'func_cycle': 10  # minimal duration of switch on event in minutes
                 },
            'outdoor_lights':
                {
                    'num_app': 3,  # number of appliances
                    'power': 15,  # power in W
                    'usage_window_1': [5, 7],  # usage window [start, end] in min of the day
                    'usage_window_2': [20, 23],  # usage window [start, end] in min of the day
                    'daily_usage_time': 2,  # daily time of use in min
                    'func_cycle': 10  # minimal duration of switch on event in minutes
                 }
        }


    },
    'medium_income_hh': {
        'num_users': 1,
        'months_present': [1, 2, 3, 4, 7, 8, 9, 10, 11, 12],  # months at which this user is present in the settlement
        'working_days': [0, 1, 2, 3, 4, 5, 6],  # days at which this user uses his appliances
        'appliances': {
            'indoor_lights':
                {
                    'num_app': 3,  # number of appliances
                    'power': 10,  # power in W
                    'usage_window_1': [5, 7],  # usage window [start, end] in min of the day
                    'usage_window_2': [20, 23],  # usage window [start, end] in min of the day
                    'daily_usage_time': 2,  # daily time of use in min
                    'func_cycle': 10  # minimal duration of switch on event in minutes
                 }
        }

    },

    'high_income_hh': {
        'num_users': 1,
        'months_present': [1, 2, 3, 4, 7, 8, 9, 10, 11, 12],  # months at which this user is present in the settlement
        'working_days': [0, 1, 2, 3, 4, 5, 6],  # days at which this user uses his appliances
        'appliances': {
            'indoor_lights':
                {
                    'num_app': 3,  # number of appliances
                    'power': 10,  # power in W
                    'usage_window_1': [5, 7],  # usage window [start, end] in min of the day
                    'usage_window_2': [20, 23],  # usage window [start, end] in min of the day
                    'daily_usage_time': 2,  # daily time of use in min
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
    },
    'cooking_metadata': {
            'cooking_time_variability': 0.2,
            'cooking_window_variability': 0.2,
            'cooking_fuels': {
                'firewood': {
                    'energy_content': 3,  # energy content per unit of this fuel
                    'unit': 'kg'
                },
                'charcoal': {
                    'energy_content': 5,
                    'unit': 'kg'
                },
                'biogas': {
                    'energy_content': 10,
                    'unit': 'l'
                }
            },
            'cooking_stoves': {
                'three_stone_fire': {
                    'efficiency': 0.1
                },
                'advanced_firewood_stove': {
                    'efficiency': 0.2
                }
            }
        }
}

#%%
import pandas as pd
from DAT_src.ramp_control import RampControl
from DAT_src.cooking_demand import cooking_demand_dict

# Create instance of RampControl class, define timeframe to model load profiles
ramp_control = RampControl(365, '2018-01-01')

# Create RAMP use cases

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

elec_use_cases_list = ramp_control.generate_electric_appliances_use_cases(households_dict, admin_input)
cooking_use_cases_list = ramp_control.generate_cooking_demand_use_cases(cooking_demand_dict, admin_input)


# Run load use_cases and create demand profiles
elec_lp = ramp_control.run_use_cases(elec_use_cases_list, households_dict, 'Household appliances')
cooking_dp = ramp_control.run_use_cases(cooking_use_cases_list, cooking_demand_dict, 'Cooking demand')


#%% Plot results
from DAT_src import plotting
from plotly.subplots import make_subplots

fig = make_subplots(2,1, shared_xaxes=True)

fig = plotting.plotly_high_res_df(fig, df=elec_lp, subplot_row=1)
fig = plotting.plotly_high_res_df(fig, df=cooking_dp, subplot_row=2)
fig.update_layout(height=600)

fig.show_dash(mode='external')
