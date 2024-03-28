service_water_dict = {
    'medium_farm': {
        'num_users': 20,
        'months_present': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
        'working_days': [0, 1, 2, 3, 4, 5],  # days at which this user uses his appliances
        'service_water_demands': {
            'irrigation': {
                'daily_demand': {  # Water demand of typical day for each month [l]
                        1: 400, 2: 300, 3: 100, 4: 100, 5: 0, 6: 400, 7: 800, 8: 1000, 9: 800, 10: 600, 11: 500, 12: 400
                    },
                'usage_windows': [
                    [7, 10],
                    [14, 18],
                    None
                ],
                'demand_duration': 1,  # duration of this demand in [h]
                'pumping_head': 20  # [m]
            },
            'livestock': {
                'daily_demand': {  # Water demand of typical day for each month [l]
                        1: 400, 2: 300, 3: 100, 4: 100, 5: 0, 6: 400, 7: 800, 8: 1000, 9: 800, 10: 600, 11: 500, 12: 400
                    },
                'usage_windows': [
                    [7, 10],
                    [14, 18],
                    None
                ],
                'demand_duration': 1,  # duration of this demand in [h]
                'pumping_head': 20  # [m]
            }
        },
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
        },
    },
    'small_farm': {
        'num_users': 1,
        'months_present': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
        'working_days': [0, 1, 2, 3, 4, 5],  # days at which this user uses his appliances
        'service_water_demands': {
            'irrigation': {
                'daily_demand': {  # Water demand of typical day for each month [l]
                    1: 400, 2: 300, 3: 100, 4: 100, 5: 0, 6: 400, 7: 800, 8: 1000, 9: 800, 10: 600, 11: 500, 12: 400
                },
                'usage_windows': [
                    [7, 10],
                    [14, 18],
                    None
                ],
                'demand_duration': 1,  # duration of this demand in [h]
                'pumping_head': 20  # [m]
            },
            'livestock': {
                'daily_demand': {  # Water demand of typical day for each month [l]
                    1: 400, 2: 300, 3: 100, 4: 100, 5: 0, 6: 400, 7: 800, 8: 1000, 9: 800, 10: 600, 11: 500, 12: 400
                },
                'usage_windows': [
                    [7, 10],
                    [14, 18],
                    None
                ],
                'demand_duration': 1,  # duration of this demand in [h]
                'pumping_head': 20  # [m]
            }
        },
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
        },
    }
}