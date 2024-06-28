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
        },
        'radio': {
            'daily_use_variability': 0.3,
            'usage_window_variability': 0.1
        },
        'fan': {
            'daily_use_variability': 0.3,
            'usage_window_variability': 0.1
        },
        'pc': {
            'daily_use_variability': 0.3,
            'usage_window_variability': 0.1
        },
        'refrigerator': {
            'daily_use_variability': 0.3,
            'usage_window_variability': 0.1
        },
        'in_bulb': {
            'daily_use_variability': 0.3,
            'usage_window_variability': 0.1
        },
        'out_bulb': {
            'daily_use_variability': 0.3,
            'usage_window_variability': 0.1
        },
        'television': {
            'daily_use_variability': 0.3,
            'usage_window_variability': 0.1
        },
        'saw': {
            'daily_use_variability': 0.3,
            'usage_window_variability': 0.1
        },
        'cd': {
            'daily_use_variability': 0.3,
            'usage_window_variability': 0.1
        },
        'air': {
            'daily_use_variability': 0.3,
            'usage_window_variability': 0.1
        },
        'blender': {
            'daily_use_variability': 0.3,
            'usage_window_variability': 0.1
        },
        'shaver': {
            'daily_use_variability': 0.3,
            'usage_window_variability': 0.1
        },
        'welder': {
            'daily_use_variability': 0.3,
            'usage_window_variability': 0.1
        },
        'iron': {
            'daily_use_variability': 0.3,
            'usage_window_variability': 0.1
        },
        'fan': {
            'daily_use_variability': 0.3,
            'usage_window_variability': 0.1
        },
        'kettle': {
            'daily_use_variability': 0.3,
            'usage_window_variability': 0.1
        },
        'wash_mach': {
            'daily_use_variability': 0.3,
            'usage_window_variability': 0.1
        },
        'mobile': {
            'daily_use_variability': 0.3,
            'usage_window_variability': 0.1
        },
        'other_device_1': {
            'daily_use_variability': 0.3,
            'usage_window_variability': 0.1
        },
        'other_device_2': {
            'daily_use_variability': 0.3,
            'usage_window_variability': 0.1
        },
        'other_device_3': {
            'daily_use_variability': 0.3,
            'usage_window_variability': 0.1
        },
        'other_device_4': {
            'daily_use_variability': 0.3,
            'usage_window_variability': 0.1
        },
        'other_device_5': {
            'daily_use_variability': 0.3,
            'usage_window_variability': 0.1
        },
        'other_device_6': {
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
                },
                'biofuel': {
                    'energy_content': 10,
                    'unit': 'l'
                },
                'kerosene':{
                    'energy_content': 10,
                    'unit': 'l'
                },
                'pellet':{
                    'energy_content': 10,
                    'unit': 'kg'
                },
                'briquette': {
                    'energy_content': 10,
                    'unit': 'kg'
                },
                'dung': {
                    'energy_content': 10,
                    'unit': 'kg'
                },
                'LPG': {
                    'energy_content': 10,
                    'unit': 'kg'
                },
                'eth_alc': {
                    'energy_content': 10,
                    'unit': 'kg'
                }
            },
            'cooking_stoves': {
                'three_stone_fire': {
                    'efficiency': 0.1
                },
                'advanced_firewood_stove': {
                    'efficiency': 0.2
                },
                'CD_ICS': {
                    'efficiency': 0.2
                },
                'CD_LPG': {
                    'efficiency': 0.2
                },
                'CD_three_stone':{
                    'efficiency': 0.2
                },
                'CD_traditional_fire': {
                    'efficiency': 0.2
                },
                'CD_hot_plates': {
                    'efficiency': 0.2
                },
                'CD_solar_cooker': {
                    'efficiency': 0.2
                },
                'CD_ethanol': {
                    'efficiency': 0.2
                },
                'CD_other': {
                    'efficiency': 0.2
                },
                'CD_traditional_charcoal':{
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
            'electric': {
                'energy_content': 1,
                'unit': 'kWh'
            },
            'petrol': {
                'energy_content': 8,
                'unit': 'l'
            }
        },
        'husking_mill': {
            'daily_use_variability': 0.2,
            'usage_window_variability': 0.2,
            'processed_per_run_variability': 0.2,
        },
        'mill': {
            'daily_use_variability': 0.2,
            'usage_window_variability': 0.2,
            'processed_per_run_variability': 0.2,
        },
        'oil': {
            'daily_use_variability': 0.2,
            'usage_window_variability': 0.2,
            'processed_per_run_variability': 0.2,
        },
    },
    'service_water_metadata': {
        'irrigation': {
            'daily_demand_variability': 0.2,
            'demand_window_variability': 0.2
        },
        'livestock': {
            'daily_demand_variability': 0.2,
            'demand_window_variability': 0.2
        }
    }
}