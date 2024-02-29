#%% Dummy dict of cooking demands

agro_processing_dict = {
    'ms_victor': {
        'num_users': 1,
        'working_days': [0, 1, 2, 3, 4, 5],  # days at which this user uses his appliances
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
    }
}
