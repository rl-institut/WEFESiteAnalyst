import json
from DAT_src.kobo_api_access import load_kobo_data
import defaults
from copy import copy

with open("first_survey.json", "r") as file:
    first_survey = json.load(file)

# Get the parameters - Months of stay in the village
string_month = first_survey["G_1b/residency_month"]
month_dict = copy(defaults.months_present_defaults)

for month in month_dict:
    if month in string_month:
        month_dict[month] = True
    else:
        month_dict[month] = False

print(month_dict)

# Get the parameters - Working days (business)
if first_survey["G_0/respondent_type"] == "business":
    string_day = first_survey["B_2a/working_day"]
    work_days_dict = copy(defaults.working_day_default)

    for day in work_days_dict:
        if day in string_day:
            work_days_dict[day] = True
        else:
            work_days_dict[day] = False

    print(work_days_dict)

# Get the parameters - Working days (agro-processing)
if first_survey["G_0/respondent_type"] == "agroprocessing":
    string_day_AP = first_survey["AP_2c/working_day_AP"]
    work_days_dict_AP = copy(defaults.working_day_default)

    for day in work_days_dict_AP:
        if day in string_day_AP:
            work_days_dict_AP[day] = True
        else:
            work_days_dict_AP[day] = False

    print(work_days_dict_AP)


# Get the parameters - Electrical appliances (Business)
app_dict_B = {}

if first_survey["G_0/respondent_type"] == "business":
    for key, data in first_survey.items():
        if "B_11/" in key and "_power" in key :
            app_name = key.replace("B_11/","", 1).replace("_power","",1)    # appliance name
            number = first_survey["B_11/"+app_name+"_number"]
            power = first_survey["B_11/"+app_name+"_power"]
            value = first_survey ["B_11/"+app_name+"_value"]
            hour = first_survey["B_11/"+app_name+"_hour_wd"]
            string = first_survey["B_11/"+app_name+"_usage_wd"]

            usage_wd_dict = copy(defaults.usage_wd_defaults)

            for window in usage_wd_dict:
                if window in string:
                    usage_wd_dict[window] = True
                else:
                    usage_wd_dict[window] = False
            time_window = first_survey["B_11/"+app_name+"_usage_wd"].split()
            app_dict_B[app_name] = {
                "number" : float(number),           # number of appliances
                "power" : float(power),             # appliance power in W
                "value" : float(value),             # appliance value
                "usage_time": float(hour)*60,       # appliance operating usage time in min
                "time_window" : usage_wd_dict       # appliance usage windows
            }


    print(app_dict_B)

# Get the parameters - Electrical appliances (Household)
app_dict_H = {}

if first_survey["G_0/respondent_type"] == "household":
    for key, data in first_survey.items():
        if "H_16/" in key and "_power" in key :
            app_name = key.replace("H_16/","", 1).replace("_power_H","",1)    # appliance name
            number = first_survey["H_16/"+app_name+"_number_H"]
            power = first_survey["H_16/"+app_name+"_power_H"]
            value = first_survey ["H_16/"+app_name+"_value_H"]
            hour = first_survey["H_16/"+app_name+"_hour_wd_H"]
            string = first_survey["H_16/"+app_name+"_usage_wd_H"]

            usage_wd_dict = copy(defaults.usage_wd_defaults)

            for window in usage_wd_dict:
                if window in string:
                    usage_wd_dict[window] = True
                else:
                    usage_wd_dict[window] = False
            time_window = first_survey["H_16/"+app_name+"_usage_wd_H"].split()
            app_dict_H[app_name] = {
                "number" : float(number),                                   # number of appliances
                "power" : float(power),                                     # appliance power in W
                "value" : float(value),                                     # appliance value
                "usage_time": float(hour)*60,                               # appliance operating usage time in min
                "time_window" : usage_wd_dict                               # appliance usage windows
            }

    print(app_dict_H)

# Get the parameters - Cooking demand (Business)
cook_dict_B = {}

if first_survey["G_0/respondent_type"] == "business":
    for key, data in first_survey.items():
        if "B_13" in key and "_time" in key :
            fuel_name = key.replace("B_13","", 1).replace("_time","",1)
            time_cons = first_survey["B_13"+fuel_name+"_time"]
            unit = first_survey["B_13"+fuel_name+"_unit"]
            kg_bag = first_survey["B_13"+fuel_name+"_bag"]
            quantity = first_survey["B_13"+fuel_name+"_amount"]
            price = first_survey["B_13"+fuel_name+"_cost"]

            cook_dict_B[fuel_name] = {
            "time": time_cons,
            "unit": unit,                                                   # appliance power
            "bag": float(kg_bag),                                           # appliance value
            "quantity": float(quantity),                                    # appliance operating hours
            "price": float(price)                                           # appliance time windows
        }

    print(cook_dict_B)


# Get the parameters - Meal (Business)
meal_dict_B = {}

if first_survey["G_0/respondent_type"] == "business":
    for key, data in first_survey.items():
        if "B_13" in key :
            week = first_survey["B_13_meal/meal_per_week"]
            fuel = first_survey["B_13_meal/fuels_meal"]
            cooking_device = first_survey["B_13_meal/cooking_meal"]
            string_meal_window = first_survey["B_13_meal/usage_meal"]

            meal_usage_time = copy(defaults.usage_wd_defaults)

            for window in meal_usage_time:
                if window in string_meal_window:
                    meal_usage_time[window] = True
                else:
                    meal_usage_time[window] = False
            time_window = first_survey["B_13_meal/usage_meal"].split()

            meal_dict_B["meal_business"] = {
            "meal_week" : float(week),
            "meal_fuel" : fuel,
            "meal_cooking_device" : cooking_device,
            "meal_usage_time" : meal_usage_time
            }

    print(meal_dict_B)

# Get the parameters - Cooking demand (Household)
cook_dict_H = {}

if first_survey["G_0/respondent_type"] == "household":
    for key, data in first_survey.items():
        if "H_18" in key and "_time" in key :
            fuel_name = key.replace("H_18","", 1).replace("_time_H","",1)
            time_cons = first_survey["H_18"+fuel_name+"_time_H"]
            unit = first_survey["H_18"+fuel_name+"_unit_H"]
            kg_bag = first_survey ["H_18"+fuel_name+"_bag_H"]
            quantity = first_survey["H_18"+fuel_name+"_amount_H"]
            price = first_survey["H_18"+fuel_name+"_cost_H"]

            cook_dict_H[fuel_name] = {
            "time": time_cons,
            "unit": unit,                                                   # appliance power
            "bag": float(kg_bag),                                           # appliance value
            "quantity": float(quantity),                                    # appliance operating hours
            "price": float(price)                                           # appliance time windows
        }

    print(cook_dict_H)

# Get the parameters - Meal (Household)
meal_dict_H = {}

if first_survey["G_0/respondent_type"] == "household":
    for key, data in first_survey.items():
        if "H_18" in key :
            week = first_survey["H_18l/meal_per_week_H"]
            fuel = first_survey["H_18l/fuels_meal_H"]
            cooking_device = first_survey["H_18l/cooking_meal_H"]
            string_meal_window = first_survey["H_18l/usage_meal_H"]

            meal_usage_time = copy(defaults.usage_wd_defaults)

            for window in meal_usage_time:
                if window in string_meal_window:
                    meal_usage_time[window] = True
                else:
                    meal_usage_time[window] = False
            time_window = first_survey["H_18l/usage_meal_H"].split()

            meal_dict_H["meal_household"] = {
            "meal_week" : float(week),
            "meal_fuel" : fuel,
            "meal_cooking_device" : cooking_device,
            "meal_usage_time" : meal_usage_time
            }

    print(meal_dict_H)

# Get the parameters - Drinking Water (Business)
drinking_water_dict_B = {}

if first_survey["G_0/respondent_type"] == "business":
    unit_of_measurement = first_survey["B_7/drinking_express"]
    unit = float(first_survey["B_7/drink_use"])
    string_drink_window = first_survey["B_7/drink_time"]

    if unit_of_measurement == "drink_liter" :
        consume = unit
    elif unit_of_measurement == "drink_large_buck" :
        consume = unit * 10
    elif unit_of_measurement == "drink_medium_buck" :
        consume = unit * 5
    elif unit_of_measurement == "drink_small_buck" :
        consume = unit

    drink_usage_time = copy(defaults.usage_wd_defaults)

    for window in drink_usage_time:
        if window in string_drink_window:
            drink_usage_time[window] = True
        else:
            drink_usage_time[window] = False
    time_window = first_survey["B_7/drink_time"].split()

    drinking_water_dict_B["drinking_water_B"] = {
        "daily_demand" : consume,
        "water_window" : drink_usage_time
    }

    print(drinking_water_dict_B)

# Get the parameters - Drinking Water (Household)
drinking_water_dict_H = {}

if first_survey["G_0/respondent_type"] == "household":
    unit_of_measurement = first_survey["H_8/drinking_express_H"]
    unit = float(first_survey["H_8/drink_use_H"])
    string_drink_window = first_survey["H_8/drink_time_H"]

    if unit_of_measurement == "drink_liter" :
        consume = unit
    elif unit_of_measurement == "drink_large_buck" :
        consume = unit * 10
    elif unit_of_measurement == "drink_medium_buck" :
        consume = unit * 5
    elif unit_of_measurement == "drink_small_buck" :
        consume = unit

    drink_usage_time = copy(defaults.usage_wd_defaults)

    for window in drink_usage_time:
        if window in string_drink_window:
            drink_usage_time[window] = True
        else:
            drink_usage_time[window] = False
    time_window = first_survey["H_8/drink_time_H"].split()

    drinking_water_dict_H["drinking_water_H"] = {
        "daily_demand" : consume,
        "water_window" : drink_usage_time
    }

    print(drinking_water_dict_H)

# Get the parameters - Service Water (Business)

service_water_dict_B = {}

if first_survey["G_0/respondent_type"] == "business":
    unit_of_measurement_serv = first_survey["B_7/service_express"]
    unit_serv = float(first_survey["B_7/serv_use"])
    string_serv_window = first_survey["B_7/serv_time"]

    if unit_of_measurement_serv == "serv_liter":
        consume_serv = unit_serv
    elif unit_of_measurement_serv == "serv_large_buck":
        consume_serv = unit_serv * 10
    elif unit_of_measurement_serv == "serv_medium_buck":
        consume_serv = unit_serv * 5
    elif unit_of_measurement_serv == "serv_small_buck":
        consume_serv = unit_serv

    service_usage_time = copy(defaults.usage_wd_defaults)

    for window in service_usage_time:
        if window in string_serv_window:
            service_usage_time[window] = True
        else:
            service_usage_time[window] = False
    time_window_serv = first_survey["B_7/serv_time"].split()

    service_water_dict_B["service_water_business"] = {
        "daily_demand": consume_serv,
        "water_window": service_usage_time
    }

    print(service_water_dict_B)

# Get the parameters - Service Water (Household)

irrigation_water_dict_H = {}
if first_survey["G_0/respondent_type"] == "household":
    uom_dry_irr = first_survey["H_10/express_dry_H"]
    unit_dry_irr = float(first_survey["H_10/irrigation_dry_H"])
    string_irr_dry_window = first_survey["H_10/usage_dry_H"]

    if uom_dry_irr == "serv_liter":
        consume_dry_irr = unit_dry_irr
    elif uom_dry_irr == "serv_large_buck":
        consume_dry_irr = unit_dry_irr * 10
    elif uom_dry_irr == "serv_medium_buck":
        consume_dry_irr = unit_dry_irr * 5
    elif uom_dry_irr == "serv_small_buck":
        consume_dry_irr = unit_dry_irr

    dry_irr_usage_time = copy(defaults.usage_wd_defaults)

    for window in dry_irr_usage_time:
        if window in string_irr_dry_window:
            dry_irr_usage_time[window] = True
        else:
            dry_irr_usage_time[window] = False

    uom_rainy_irr = first_survey["H_10/express_rainy_H"]
    unit_rainy_irr = float(first_survey["H_10/irrigation_rainy_H"])
    string_irr_rainy_window = first_survey["H_10/usage_rainy_H"]

    if uom_rainy_irr == "serv_liter":
        consume_rainy_irr = unit_rainy_irr
    elif uom_rainy_irr == "serv_large_buck":
        consume_rainy_irr = unit_rainy_irr * 10
    elif uom_rainy_irr == "serv_medium_buck":
        consume_rainy_irr = unit_rainy_irr * 5
    elif uom_rainy_irr == "serv_small_buck":
        consume_rainy_irr = unit_rainy_irr

    rainy_irr_usage_time = copy(defaults.usage_wd_defaults)

    for window in rainy_irr_usage_time:
        if window in string_irr_rainy_window:
            rainy_irr_usage_time[window] = True
        else:
            rainy_irr_usage_time[window] = False

    string_rainy = first_survey["H_10/dry_season_H"]
    season_dict = copy(defaults.months_present_defaults)

    for month in season_dict:
        if month in string_rainy:
            season_dict[month] = consume_rainy_irr
        else:
            season_dict[month] = consume_dry_irr

    irrigation_water_dict_H["irrigation_water_household"] = {
        "daily_demand": season_dict,
        "irr_window_dry": dry_irr_usage_time,
        "irr_window_rainy" : rainy_irr_usage_time
    }

    print(irrigation_water_dict_H)

animal_water_dict_H = {}
if first_survey["G_0/respondent_type"] == "household":
    uom_dry_animal = first_survey["H_11/express_animal_dry_H"]
    unit_dry_animal = float(first_survey["H_11/animal_dry_H"])
    string_animal_dry_window = first_survey["H_11/usage_animal_dry_H"]

    if uom_dry_animal == "serv_liter":
        consume_dry_animal = unit_dry_animal
    elif uom_dry_animal == "serv_large_buck":
        consume_dry_animal = unit_dry_animal * 10
    elif uom_dry_animal == "serv_medium_buck":
        consume_dry_animal = unit_dry_animal * 5
    elif uom_dry_animal == "serv_small_buck":
        consume_dry_animal = unit_dry_animal

    dry_animal_usage_time = copy(defaults.usage_wd_defaults)

    for window in dry_animal_usage_time:
        if window in string_animal_dry_window:
            dry_animal_usage_time[window] = True
        else:
            dry_animal_usage_time[window] = False

    uom_rainy_animal = first_survey["H_11/express_animal_rainy_H"]
    unit_rainy_animal = float(first_survey["H_11/animal_rainy_H"])
    string_animal_rainy_window = first_survey["H_11/usage_animal_rainy_H"]

    if uom_rainy_animal == "serv_liter":
        consume_rainy_animal = unit_rainy_animal
    elif uom_rainy_animal == "serv_large_buck":
        consume_rainy_animal = unit_rainy_animal * 10
    elif uom_rainy_animal == "serv_medium_buck":
        consume_rainy_animal = unit_rainy_animal * 5
    elif uom_rainy_irr == "serv_small_buck":
        consume_rainy_animal = unit_rainy_animal

    rainy_animal_usage_time = copy(defaults.usage_wd_defaults)

    for window in rainy_animal_usage_time:
        if window in string_animal_rainy_window:
            rainy_animal_usage_time[window] = True
        else:
            rainy_animal_usage_time[window] = False

    string_rainy_animal = first_survey["H_10/dry_season_H"]
    season_dict_animal = copy(defaults.months_present_defaults)

    for month in season_dict_animal:
        if month in string_rainy_animal:
            season_dict_animal[month] = consume_rainy_animal
        else:
            season_dict_animal[month] = consume_dry_animal

    animal_water_dict_H["animal_water_household"] = {
        "daily_demand": season_dict_animal,
        "irr_window_dry": dry_animal_usage_time,
        "irr_window_rainy" : rainy_animal_usage_time
    }

    print(animal_water_dict_H)

# Get the parameters - Agro processing demand (Agroprocessing)
agroproc_dict = {}

if first_survey["G_0/respondent_type"] == "agroprocessing":
    for key, data in first_survey.items():
        if "AP_5/" in key and "_motor_AP" in key:
            mach_name = key.replace("AP_5/", "", 1).replace("_motor_AP", "", 1)  # machinery name
            fuel_AP = first_survey["AP_5/" + mach_name + "_motor_AP"]
            product = first_survey["AP_5/" + mach_name + "_prod_onerun_AP"]
            efficiency = first_survey["AP_5/" + mach_name + "_eff_AP"]
            hour_AP = first_survey["AP_5/" + mach_name + "_hour_AP"]
            string_AP = first_survey["AP_5/" + mach_name + "_usage_AP"]

            usage_AP_dict = copy(defaults.usage_wd_defaults)

            for window in usage_AP_dict:
                if window in string_AP:
                    usage_AP_dict[window] = True
                else:
                    usage_AP_dict[window] = False

            months_AP = {
                'January': float(first_survey["AP_5/" + mach_name + "_prod_jan_AP"]),
                'February': float(first_survey["AP_5/" + mach_name + "_prod_feb_AP"]),
                'March': float(first_survey["AP_5/" + mach_name + "_prod_mar_AP"]),
                'April': float(first_survey["AP_5/" + mach_name + "_prod_apr_AP"]),
                'May': float(first_survey["AP_5/" + mach_name + "_prod_may_AP"]),
                'June': float(first_survey["AP_5/" + mach_name + "_prod_jun_AP"]),
                'July': float(first_survey["AP_5/" + mach_name + "_prod_jul_AP"]),
                'August': float(first_survey["AP_5/" + mach_name + "_prod_aug_AP"]),
                'September': float(first_survey["AP_5/" + mach_name + "_prod_sep_AP"]),
                'October': float(first_survey["AP_5/" + mach_name + "_prod_oct_AP"]),
                'November': float(first_survey["AP_5/" + mach_name + "_prod_nov_AP"]),
                'December': float(first_survey["AP_5/" + mach_name + "_prod_dec_AP"])
            }
            if first_survey["AP_5/" + mach_name + "_prod_exp_AP"] == "daily":
                exp = 1
            elif first_survey["AP_5/" + mach_name + "_prod_exp_AP"] == "weekly":
                exp = 7
            elif first_survey["AP_5/" + mach_name + "_prod_exp_AP"] == "monthly":
                exp = 30
            for k in months_AP:
                months_AP[k] = months_AP[k] / exp

            agroproc_dict[mach_name] = {
                "fuel": fuel_AP,
                "crop_processed_per_fuel": float(product),
                "throughput": float(efficiency),
                "usage_time": float(hour_AP) * 60,  # machine operating usage time in min
                "time_window": usage_AP_dict,  # machine usage windows
                "crop_processed_per_day" : months_AP
            }

    print(agroproc_dict)

