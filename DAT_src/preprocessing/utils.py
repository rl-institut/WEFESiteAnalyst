# util functions
from copy import copy
import numpy as np

from preprocessing.kobo_api_access import load_kobo_data
from preprocessing import defaults


def convert_perkg(how_much, unit, fuel, kg_per_bag=None):
    if unit in defaults.fuel_units_conversion.keys():
        if unit == "kilogram":
            return how_much
        elif unit == "liter":
            return how_much*defaults.density_dict[f"{fuel}_density"]
        elif unit == "bag" or unit == "cylinder":
            if kg_per_bag is not None:
                return how_much*kg_per_bag
            else:
                raise ValueError("Missing bag conversion coefficent")
    else:
        raise ValueError(f"Missing fuel unit. The one defined are: {defaults.fuel_units_conversion.keys()}")

def convert_perday(quantity, period):
    if period in defaults.time_units_conversion.keys():
        return quantity/defaults.time_units_conversion[period]
    else:
        raise ValueError(f"Missing time period of reference. The one defined are: {defaults.time_units_conversion.keys()}")

def convert_perliter(unit, quantity, buck_conversion=None):
        if "liter" in unit:
            return quantity
        elif "buck" in unit and buck_conversion is not None:
            return quantity * buck_conversion
        else:
            raise ValueError("Unit for water usage not known or buck conversion missing")

def exctract_time_window(usage_time):
    windows = copy(defaults.usage_wd_defaults)

    for window in windows:
        if window in usage_time:
            windows[window] = True
        else:
            windows[window] = False
    return windows

def how_many_meal(mystring):
    if "one" in mystring:
        return 1
    elif "two" in mystring:
        return 2
    else:
        return 3

def select_meal_type(meal_number):
    if meal_number == 1:
        return "breackfast"
    elif meal_number == 2:
        return "lunch"
    else:
        return "dinner"

# general function 

def get_survey(survey_id="atiMZ5E4jaZHv37TUekb6N", api_t="ea290627972a055fd067e1efc02c803869b1747c"):
    survey, _ = load_kobo_data(form_id=survey_id, api_token=api_t)
    
    return survey

def convert_usage_windows_2(input_dict):
    # used when "windows_1", "windows_2" etc is required
    usage_windows = []
    start_time = None
    windows = {}
    for window, active in input_dict.items():
        hour_range = window.split('-')
        if active:
            if start_time is None:
                start_time = int(hour_range[0])
        elif start_time is not None:
            end_time = int(hour_range[0])
            usage_windows.append([start_time, end_time])
            start_time = None
    if start_time is not None:
        # If there's an active window at the end of the day
        # assume it ends at midnight (24)
        usage_windows.append([start_time, 24])

    for w in np.arange(len(usage_windows)):
        windows[f'window_{w+1}'] = usage_windows[w]

    return windows


def convert_usage_windows(input_dict):
    # standard usage windows definition
    usage_windows = []
    start_time = None

    for window, active in input_dict.items():
        hour_range = window.split('-')
        if active:
            if start_time is None:
                start_time = int(hour_range[0])
        elif start_time is not None:
            end_time = int(hour_range[0])
            usage_windows.append([start_time, end_time])
            start_time = None
    if start_time is not None:
        # If there's an active window at the end of the day
        # assume it ends at midnight (24)
        usage_windows.append([start_time, 24])

    return usage_windows


def rename_keys(dictionary):
    new_dict = {}
    for i, key in enumerate(dictionary):
        new_dict[i+1] = dictionary[key]
    return new_dict

def set_values (dictionary, variable):
    new_dict = {}
    for key in dictionary:
        new_dict[key] = variable
    return new_dict
