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
            }
        }
    }
}