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
        },
    'agro_processing_metadata': {
        'agro_processing_fuels': {
            'diesel': {
                'energy_content': 10,  # energy content in kWh per unit of fuel
                'unit': 'l'
            },
            'electricity': {
                'energy_content': 1,
                'unit': 'kWh'
            }
        },
        'husking_mill': {
            'daily_use_variability': 0.2,
            'usage_window_variability': 0.2,
            'processed_per_run_variability': 0.2,
        }
    },
    'service_water_metadata': {
        'irrigation': {
            'daily_demand_variability': 0.2,
            'demand_window_variability': 0.2
        }
    }
}