#%% Complete input data dict
# Dummy dict of households with electrical appliances
# Will be read from surveys
input_dict = {
    'low_income_hh': {
        'num_users': 20,
        'months_present': [1, 2, 3, 4, 7, 8, 9, 10, 11, 12],  # months at which this user is present in the settlement
        'working_days': [0, 1, 2, 3, 4, 5],  # days at which this user uses his appliances
        'appliances':  # electrical appliances that this user owns
            {
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
        },
        'cooking_demands':
            {
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
        'drinking_water_demand':
            {
                    'daily_demand': 50,  # daily drinking water demand [l]
                    'water_window_1': [10, 12],
                    'water_window_2': [16, 18]
            },
        'service_water_demands':
            {},
        'agro_processing_machines':
            {}
    },

    'medium_farm':
        {
        'num_users': 2,
        'months_present': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
        'working_days': [0, 1, 2, 3, 4, 5],
        'appliances':  # electrical appliances that this user owns
            {
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
        },
        'cooking_demands':
            {
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
        'drinking_water_demand':
            {
                    'daily_demand': 50,  # daily drinking water demand [l]
                    'water_window_1': [10, 12],
                    'water_window_2': [16, 18]
            },
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

        'agro_processing_machines': {
            'husking_mill':
                {
                    'fuel': 'diesel',  # fuel used -> to match meta data
                    'crop_processed_per_fuel': 200,  # crop processed [kg] per unit of fuel [l, kWh ...]
                    'throughput': 500,  # [kg] of crop processed per [h] of machine operation
                    'crop_processed_per_run': 100,  # [kg] of crop processed typically per switch-on of the machine

                    'usage_window_1': [8, 12],  # usage window [start, end] in h of the day
                    'usage_window_2': [13, 17],  # usage window [start, end] in h of the day
                    'crop_processed_per_day': {  # Crop processed on a typical working day
                        1: 400, 2: 300, 3: 100, 4: 100, 5: 0, 6: 400, 7: 800, 8: 1000, 9: 800, 10: 600, 11: 500, 12: 400
                    }
                 },
            'oil_press':
                {
                    'fuel': 'diesel',  # fuel used -> to match meta data
                    'crop_processed_per_fuel': 200,  # crop processed [kg] per unit of fuel [l, kWh ...]
                    'throughput': 500,  # [kg] of crop processed per [h] of machine operation
                    'crop_processed_per_run': 100,  # [kg] of crop processed typically per switch-on of the machine

                    'usage_window_1': [8, 12],  # usage window [start, end] in h of the day
                    'usage_window_2': [13, 17],  # usage window [start, end] in h of the day
                    'crop_processed_per_day': {  # Crop processed on a typical working day
                        1: 400, 2: 300, 3: 100, 4: 100, 5: 0, 6: 400, 7: 800, 8: 1000, 9: 800, 10: 600, 11: 500, 12: 400
                    }
                 },
        }
    },
}