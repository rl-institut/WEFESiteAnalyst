#%% Household electricity demand
# Dummy dict of households with electrical appliances
# Will be read from surveys
households_dict = {
    'low_income_hh': {
        'num_users': 20,
        'months_present': [1, 2, 3, 4, 7, 8, 9, 10, 11, 12],  # months at which this user is present in the settlement
        'working_days': [0, 1, 2, 3, 4, 5],  # days at which this user uses his appliances
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
        'num_users': 30,
        'months_present': [1, 2, 3, 4, 7, 8, 9, 10, 11, 12],  # months at which this user is present in the settlement
        'working_days': [0, 1, 2, 3, 4, 5],  # days at which this user uses his appliances
        'appliances': {
            'indoor_lights':
                {
                    'num_app': 3,  # number of appliances
                    'power': 10,  # power in W
                    'usage_window_1': [5, 7],  # usage window [start, end] in h of the day
                    'usage_window_2': [20, 23],  # usage window [start, end] in h of the day
                    'daily_usage_time': 2,  # daily time of use in h
                    'func_cycle': 10  # minimal duration of switch on event in min
                 }
        }

    },

    'high_income_hh': {
        'num_users': 10,
        'months_present': [1, 2, 3, 4, 7, 8, 9, 10, 11, 12],  # months at which this user is present in the settlement
        'working_days': [0, 1, 2, 3, 4, 5],  # days at which this user uses his appliances
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