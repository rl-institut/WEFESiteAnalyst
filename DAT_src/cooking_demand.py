#%% Import packages

import ramp
import pandas as pd
import numpy as np
import copy
from  time import perf_counter

# Define timeseries for which demand profiles will be generated
days_nr = 3  # Number of days
timeseries = pd.date_range("2018-01-01", periods=days_nr * 24 * 60, freq="Min")  # 2018 starts on Monday
days_timeseries = pd.date_range("2018-01-01", periods=days_nr, freq="D")

#%% Dummy dict of cooking demands

cooking_demand_dict = {
    'low_income_hh': {
        'num_users': 20,
        'cooking_demands': {
            'lunch':
                {
                    'fuel': 'firewood',
                    'fuel_amount': 0.3,
                    'cooking_window': [5, 7],  # usage window [start, end] in min of the day
                    'cooking_time': 1.5,  # average duration of this meal preparation
                 },
            'dinner':
                {
                    'fuel': 'firewood',
                    'fuel_amount': 0.5,
                    'cooking_window': [18, 20],  # usage window [start, end] in min of the day
                    'cooking_time': 2,  # average duration of this meal preparation
                 }
        }
    }
}

admin_input = {
    'cooking_metadata': {
        'cooking_fuels': {
            'firewood': {
                'energy_density': 3
            },
            'charcoal': {
                'energy_density': 5
            },
            'biogas': {
                'energy_density'
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

