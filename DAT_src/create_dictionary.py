import json
from DAT_src.kobo_api_access import load_kobo_data
import defaults
from copy import copy

with open("first_survey.json", "r") as file:
    first_survey = json.load(file)

# Get the parameters - Electrical appliances (Business)
app_dict = {}

for key, data in first_survey.items():
    if "B_11/" in key and "_power" in key :
        app_name = key.replace("B_11/","", 1).replace("_power","",1)    # appliance name
        number = first_survey["B_11/"+app_name+"_number"]
        power = first_survey["B_11/"+app_name+"_power"]
        value = first_survey ["B_11/"+app_name+"_value"]
        hour = first_survey["B_11/"+app_name+"_hour_wd"]
        string = first_survey['B_11/in_bulb_usage_wd']

        usage_wd_dict = copy(defaults.usage_wd_defaults)

        for window in usage_wd_dict:
            if window in string:
                usage_wd_dict[window] = True
            else:
                usage_wd_dict[window] = False
        time_window = first_survey["B_11/"+app_name+"_usage_wd"].split()
        app_dict[app_name] = {
            "number" : float(number),           # appliance quantity
            "power" : float(power),             # appliance power
            "value" : float(value),             # appliance value
            "hour": float(hour),                # appliance operating hours
            "time_window" : usage_wd_dict       # appliance time windows
        }

print(app_dict)

# Get the parameters - Cooking demand (Business)
cook_dict = {}

for key, data in first_survey.items():
    if "B_13" in key and "_time" in key :
        fuel_name = key.replace("B_13/","", 1).replace("_time","",1)    # fuel name
        time_cons = first_survey["B_13/"+fuel_name+"_time"]
        unit = first_survey["B_13/"+fuel_name+"_unit"]
        bag = first_survey ["B_13/"+fuel_name+"_bag"]
        quantity = first_survey["B_13/"+fuel_name+"_amount"]
        price = first_survey["B_13/"+fuel_name+"_cost"]

        cook_dict[fuel_name] = {
        "time": time_cons,
        "unit": unit,  # appliance power
        "bag": float(bag),  # appliance value
        "quantity": float(quantity),  # appliance operating hours
        "price": float(price)  # appliance time windows
    }

print(cook_dict)
