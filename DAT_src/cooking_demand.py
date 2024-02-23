#%% Dummy dict of cooking demands

cooking_demand_dict = {
    'low_income_hh': {
        'num_users': 20,
        'months_present': [1, 2, 3, 4, 7, 8, 9, 10, 11, 12],  # months at which this user is present in the settlement
        'working_days': [0, 1, 2, 3, 4, 5, 6],  # days at which this user uses his appliances
        'cooking_demands': {
            'lunch':
                {
                    'stove': 'three_stone_fire',  # stove used for this cooking demand -> to match metadata
                    'fuel': 'firewood',  # fuel type used -> to match meta data
                    'fuel_amount': 0.3,  # amount of fuel used for this demand [kg, l, kWh]
                    'cooking_window_start': 5,  # start of time window of this cooking demand [h]
                    'cooking_window_end': 8,  # end of time window of this cooking demand [h]
                    'cooking_time': 1.5,  # average duration of this meal preparation
                 },
            'dinner':
                {
                    'stove': 'three_stone_fire',  # stove used for this cooking demand -> to match metadata
                    'fuel': 'firewood',  # fuel used -> to match meta data
                    'fuel_amount': 0.3,  # amount of fuel used for this demand [unit depending on fuel -> metadata]
                    'cooking_window_start': 17,  # start of time window of this cooking demand [h]
                    'cooking_window_end': 20,  # end of time window of this cooking demand [h]
                    'cooking_time': 1.5,  # average duration of this meal preparation
                },
        }
    }
}
