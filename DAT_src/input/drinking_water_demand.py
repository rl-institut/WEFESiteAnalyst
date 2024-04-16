drinking_water_dict = {
    'low_income_hh': {
        'num_users': 20,
        'months_present': [1, 2, 3, 4, 7, 8, 9, 10, 11, 12],
        'working_days': [0, 1, 2, 3, 4, 5],  # days at which this user uses his appliances
        'drinking_water_demand': {
            'daily_demand': 50,  # daily drinking water demand [l]
            'water_window_1': [10, 12],
            'water_window_2': [16, 18]
        }
    },
    'medium_income_hh': {
        'num_users': 1,
        'months_present': [1, 2, 3, 4, 7, 8, 9, 10, 11, 12],
        'working_days': [0, 1, 2, 3, 4, 5],  # days at which this user uses his appliances
        'drinking_water_demand': {
            'daily_demand': 50,  # daily drinking water demand [l]
            'water_window_1': [10, 12],
            'water_window_2': [16, 18]
        }
    }
}
