import json
import defaults
from copy import copy
from conversion_functions import *
from defaults import *

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
months_present = convert(month_dict)                                                # Months of stay in the village

# Get the parameters - Working days (business)
if first_survey["G_0/respondent_type"] == "business":
    string_day = first_survey["B_2a/working_day"]
    work_days_dict = copy(defaults.working_day_default)

    for day in work_days_dict:
        if day in string_day:
            work_days_dict[day] = True
        else:
            work_days_dict[day] = False

    working_days = convert(work_days_dict)                                         # Working days (business)

# Get the parameters - Working days (agro-processing)
if first_survey["G_0/respondent_type"] == "agroprocessing":
    string_day_AP = first_survey["AP_2c/working_day_AP"]
    working_AP = copy(defaults.working_day_default)

    for day in working_AP:
        if day in string_day_AP:
            working_AP[day] = True
        else:
            working_AP[day] = False

    working_days_AP=working_AP                                     # Working days (agroprocessing)

# Get the parameters - Working days (household)
if first_survey["G_0/respondent_type"] == "household":
    hh_working_day = [0,1,2,3,4,5,6]

# Get the parameters - Working days (service)
if first_survey["G_0/respondent_type"] == "service":
    string_day = first_survey["S_2/working_day_S"]
    serv_work_days_dict = copy(defaults.working_day_default)

    for day in serv_work_days_dict:
        if day in string_day:
            serv_work_days_dict[day] = True
        else:
            serv_work_days_dict[day] = False

    serv_working_days = convert(serv_work_days_dict)

# Get the parameters - Monthly revenues (Business)
rev_B = {}

if first_survey["G_0/respondent_type"] == "business":
    rev_week = float(first_survey["B_4b/bus_rev_lastweek"])
    rev_month = float(first_survey["B_4b/bus_rev_lastmonth"])

    rev_B["business monthly revenues"] = {
        "weekly revenues * 4" : rev_week * 4,
        "monthly revenues" : rev_month
    }

# Get the parameters - Monthly revenues (Household)
sav_H = {}

total_saving_usd = 0
total_saving_local = 0

if first_survey["G_0/respondent_type"] == "household":
    for key, data in first_survey.items():
        if "H_3" in key and "_currency_H" in key :
            saving_name = key.replace("H_3","", 1).replace("_currency_H","",1)
            try:
                saving_usd = float(first_survey["H_3" + saving_name + "_amount_USD_H"])
            except KeyError:
                saving_usd = 0.0

            try:
                saving_local = float(first_survey["H_3" + saving_name + "_amount_local_H"])
            except KeyError:
                saving_local = 0.0

            total_saving_usd += saving_usd
            total_saving_local += saving_local * exc_rate
            total_saving = total_saving_usd + total_saving_local


# Get the parameters - Monthly revenues (agro-processing)
rev_AP = {}

if first_survey["G_0/respondent_type"] == "agroprocessing":
    rev_week = float(first_survey["B_4b/bus_prof_lastweek_AP"]) * 4
    rev_month = float(first_survey["B_4b/bus_rev_lastmonth_AP"])

    rev_AP["agroprocessing monthly revenues"] = {
        "weekly revenues * 4" : rev_week,
        "monthly revenues" : rev_month
    }

# Get the parameters - Electrical appliances (Business)
app_dict_B = {}

if first_survey["G_0/respondent_type"] == "business":
    for key, data in first_survey.items():
        if "B_11/" in key and "_power" in key :
            app_name = key.replace("B_11/","", 1).replace("_power","",1)        # appliance name
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
                "number" : float(number),                           # quantity of appliance
                "power" : float(power),                             # appliance power in W
                "value" : float(value),                             # appliance value
                "usage_time": float(hour)*60,                       # appliance operating usage time in min
                "time_window" : convert_usage_windows(usage_wd_dict)                       # appliance usage windows
            }


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

            usage_wd = convert_usage_windows(usage_wd_dict)

            app_dict_H[app_name] = {
                "number" : float(number),                                   # quantity of appliance
                "power" : float(power),                                     # appliance power in W
                "value" : float(value),                                     # appliance value
                "usage_time": float(hour)*60,                               # appliance operating usage time in min
                "time_window_1" : usage_wd                           # appliance usage windows
            }

# Get the parameters - Electrical appliances (Service)
app_dict_S = {}

if first_survey["G_0/respondent_type"] == "service":
    for key, data in first_survey.items():
        if "S_3/" in key and "_power" in key :
            app_name = key.replace("S_3/","", 1).replace("_power_S","",1)        # appliance name
            number = first_survey["S_3/"+app_name+"_number_S"]
            power = first_survey["S_3/"+app_name+"_power_S"]
            value = first_survey ["S_3/"+app_name+"_value_S"]
            hour = first_survey["S_3/"+app_name+"_hour_wd_S"]
            string = first_survey["S_3/"+app_name+"_usage_wd_S"]

            usage_wd_dict = copy(defaults.usage_wd_defaults)

            for window in usage_wd_dict:
                if window in string:
                    usage_wd_dict[window] = True
                else:
                    usage_wd_dict[window] = False
            time_window = first_survey["S_3/"+app_name+"_usage_wd_S"].split()
            app_dict_S[app_name] = {
                "number" : float(number),                           # quantity of appliance
                "power" : float(power),                             # appliance power in W
                "value" : float(value),                             # appliance value
                "usage_time": float(hour)*60,                       # appliance operating usage time in min
                "time_window" : convert_usage_windows(usage_wd_dict)                       # appliance usage windows
            }



# Get the parameters - Cooking demand (Business)
cook_dict_B = {}

if first_survey["G_0/respondent_type"] == "business":
    for key, data in first_survey.items():
        if "B_13" in key and "_time" in key :
            fuel_name = key.replace("B_13","", 1).replace("_time","",1)     # fuel name
            time_cons = first_survey["B_13"+fuel_name+"_time"]
            unit = first_survey["B_13"+fuel_name+"_unit"]
            kg_bag = float(first_survey["B_13"+fuel_name+"_bag"])
            quantity = float(first_survey["B_13"+fuel_name+"_amount"])
            price = float(first_survey["B_13"+fuel_name+"_cost"])

            if time_cons == "daily" :
                if unit == "kilogram" :
                    daily_cons = quantity
                elif unit == "liter" :
                    fuel_density = density_dict[fuel + "_density"]
                    daily_cons = quantity * fuel_density
                elif unit == "bag" or unit == "cylinder":
                    daily_cons = quantity * kg_bag
            if time_cons == "weekly" :
                if unit == "kilogram" :
                    daily_cons = quantity/7
                elif unit == "liter" :
                    fuel_density = density_dict[fuel + "_density"]
                    daily_cons = quantity * fuel_density/7
                elif unit == "bag" or unit == "cylinder":
                    daily_cons = quantity * kg_bag/7
            if time_cons == "monthly" :
                if unit == "kilogram" :
                    daily_cons = quantity/30
                elif unit == "liter" :
                    fuel_density = density_dict[fuel + "_density"]
                    daily_cons = quantity * fuel_density/30
                elif unit == "bag" or unit == "cylinder":
                    daily_cons = quantity * kg_bag/30


            cook_dict_B[fuel_name] = {
            "time": time_cons,                                  # time window to express fuel consumption
            "unit": unit,                                       # unit to express fuel consumption
            "bag": kg_bag,                                      # kg per unit of fuel
            "quantity": quantity,                               # quantity of unit consumption in the time window
            "price": price,                                     # price per unit
            "fuel_amount": daily_cons                           # daily fuel consumption [kg]
        }


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

            bus_meal_time_window = convert_usage_windows(meal_usage_time)

            meal_dict_B["meal_business"] = {
            "meal_week" : float(week),                              # number of meals per week
            "meal_fuel" : fuel,                                     # fuel used for meals
            "meal_stove" : cooking_device,                          # stove used for meals
            "cooking_window_start": bus_meal_time_window[0][0],  # meals time window
            "cooking_window_end": bus_meal_time_window[0][1],
            "cooking_time": float(bus_meal_time_window[0][1]) - float(bus_meal_time_window[0][0])
            }


# Get the parameters - Cooking demand (Household)
cook_dict_H = {}

if first_survey["G_0/respondent_type"] == "household":
    for key, data in first_survey.items():
        if "H_18" in key and "_unit" in key :
            fuel_name = key.replace("H_18","", 1).replace("_unit_H","",1)
            time_cons = first_survey["H_18"+fuel_name+"_time_H"]
            unit = first_survey["H_18"+fuel_name+"_unit_H"]
            quantity = float(first_survey["H_18"+fuel_name+"_amount_H"])
            price = float(first_survey["H_18"+fuel_name+"_cost_H"])
            kg_bag = float(first_survey["H_18" + fuel_name + "_bag_H"])


            if time_cons == "daily" :
                if unit == "kilogram" :
                    daily_cons = quantity
                elif unit == "liter" :
                    fuel_density = density_dict[fuel + "_density"]
                    daily_cons = quantity * fuel_density
                elif unit == "bag" or unit == "cylinder":
                    daily_cons = quantity * kg_bag
            if time_cons == "weekly" :
                if unit == "kilogram" :
                    daily_cons = quantity/7
                elif unit == "liter" :
                    fuel_density = density_dict[fuel + "_density"]
                    daily_cons = quantity * fuel_density/7
                elif unit == "bag" or unit == "cylinder":
                    daily_cons = quantity * kg_bag/7
            if time_cons == "monthly" :
                if unit == "kilogram" :
                    daily_cons = quantity/30
                elif unit == "liter" :
                    fuel_density = density_dict[fuel + "_density"]
                    daily_cons = quantity * fuel_density/30
                elif unit == "bag" or unit == "cylinder":
                    daily_cons = quantity * kg_bag/30


            cook_dict_H[fuel_name] = {
            "time": time_cons,                                  # time window to express fuel consumption
            "unit": unit,                                       # unit to express fuel consumption
            "quantity": quantity,                               # quantity of unit consumption in the time window
            "price": price,                                     # price per unit
            "fuel_amount": daily_cons                           # daily fuel consumption
        }


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
            meal_time_window = convert_usage_windows(meal_usage_time)

            meal_dict_H["meal_household"] = {
            "meal_week" : float(week),                              # number of meals per week
            "meal_fuel" : fuel,                                     # fuel used for meals
            "meal_stove" : cooking_device,                          # stove used for meals
            "cooking_window_start" : meal_time_window[0][0],       # meals time window
            "cooking_window_end": meal_time_window[0][1],
            "cooking_time": float(meal_time_window[0][1])-float(meal_time_window[0][0])
            }

# Get the parameters - Drinking Water (Business)
drinking_water_dict_B = {}

if first_survey["G_0/respondent_type"] == "business":
    unit_of_measurement = first_survey["B_7/drinking_express"]
    unit = float(first_survey["B_7/drink_use"])
    string_drink_window = first_survey["B_7/drink_time"]

    if unit_of_measurement == "drink_liter" :
        consume = unit
    elif unit_of_measurement == "drink_large_buck" :
        consume = unit * large_buck
    elif unit_of_measurement == "drink_medium_buck" :
        consume = unit * medium_buck
    elif unit_of_measurement == "drink_small_buck" :
        consume = unit * small_buck

    drink_usage_time = copy(defaults.usage_wd_defaults)

    for window in drink_usage_time:
        if window in string_drink_window:
            drink_usage_time[window] = True
        else:
            drink_usage_time[window] = False
    time_window = first_survey["B_7/drink_time"].split()

    drinking_water_dict_B["drinking_water_B"] = {
        "daily_demand" : consume,                                   # daily drinking water demand
        "water_window" : convert_usage_windows(drink_usage_time)                           # drinking water usage window
    }


# Get the parameters - Drinking Water (Household)
drinking_water_dict_H = {}

if first_survey["G_0/respondent_type"] == "household":
    unit_of_measurement = first_survey["H_8/drinking_express_H"]
    unit = float(first_survey["H_8/drink_use_H"])
    string_drink_window = first_survey["H_8/drink_time_H"]

    if unit_of_measurement == "drink_liter" :
        consume = unit
    elif unit_of_measurement == "drink_large_buck" :
        consume = unit * large_buck
    elif unit_of_measurement == "drink_medium_buck" :
        consume = unit * medium_buck
    elif unit_of_measurement == "drink_small_buck" :
        consume = unit * small_buck

    drink_usage_time = copy(defaults.usage_wd_defaults)

    for window in drink_usage_time:
        if window in string_drink_window:
            drink_usage_time[window] = True
        else:
            drink_usage_time[window] = False
    time_window = first_survey["H_8/drink_time_H"].split()

    drinking_water_dict_H["drinking_water_H"] = {
        "daily_demand" : consume,                               # daily drinking water demand
        "water_window" : convert_usage_windows(drink_usage_time)                       # drinking water usage window
    }


# Get the parameters - Service Water (Business)

service_water_dict_B = {}

if first_survey["G_0/respondent_type"] == "business":
    unit_of_measurement_serv = first_survey["B_7/service_express"]
    unit_serv = float(first_survey["B_7/serv_use"])
    string_serv_window = first_survey["B_7/serv_time"]
    pumping_head = float(first_survey["B_7/pump_head"])
    demand_time = float(first_survey["B_7/serv_duration"])

    if unit_of_measurement_serv == "serv_liter":
        consume_serv = unit_serv
    elif unit_of_measurement_serv == "serv_large_buck":
        consume_serv = unit_serv * large_buck
    elif unit_of_measurement_serv == "serv_medium_buck":
        consume_serv = unit_serv * medium_buck
    elif unit_of_measurement_serv == "serv_small_buck":
        consume_serv = unit_serv * small_buck

    daily_demand = copy(defaults.months_defaults)
    daily_water_demand = ser_value (daily_demand, consume_serv)

    service_usage_time = copy(defaults.usage_wd_defaults)

    for window in service_usage_time:
        if window in string_serv_window:
            service_usage_time[window] = True
        else:
            service_usage_time[window] = False

    service_water_dict_B["service_water_business"] = {
        "daily_demand": daily_water_demand,
        "water_window": convert_usage_windows(service_usage_time),
        "pumping_head" : pumping_head,
        "demand_duration" : demand_time
    }


# Get the parameters - Service Water (Household)

irrigation_water_dict_H = {}
if first_survey["G_0/respondent_type"] == "household":
    uom_dry_irr = first_survey["H_10/express_dry_H"]
    unit_dry_irr = float(first_survey["H_10/irrigation_dry_H"])
    string_irr_dry_window = first_survey["H_10/usage_dry_H"]
    pumping_head_irr = float(first_survey["H_10/pump_head_irr_H"])
    demand_time_irr = float(first_survey["H_10/irr_time_H"])

    if uom_dry_irr == "serv_liter":
        consume_dry_irr = unit_dry_irr
    elif uom_dry_irr == "serv_large_buck":
        consume_dry_irr = unit_dry_irr * large_buck
    elif uom_dry_irr == "serv_medium_buck":
        consume_dry_irr = unit_dry_irr * medium_buck
    elif uom_dry_irr == "serv_small_buck":
        consume_dry_irr = unit_dry_irr * small_buck

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
        consume_rainy_irr = unit_rainy_irr * large_buck
    elif uom_rainy_irr == "serv_medium_buck":
        consume_rainy_irr = unit_rainy_irr * medium_buck
    elif uom_rainy_irr == "serv_small_buck":
        consume_rainy_irr = unit_rainy_irr * small_buck

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

    irr_season_dict = rename_keys(season_dict)

    irrigation_water_dict_H["irrigation_water_household"] = {
        "daily_demand": irr_season_dict,                                        # irrigation water demand of typical day for each month
        "irr_window_dry": convert_usage_windows(dry_irr_usage_time),            # irrigation water time window (dry season)
        "irr_window_rainy" : convert_usage_windows(rainy_irr_usage_time),        # irrigation water time window (rainy season)
        "pumping_head": pumping_head_irr,
        "demand_duration": demand_time_irr
    }

animal_water_dict_H = {}
if first_survey["G_0/respondent_type"] == "household":
    uom_dry_animal = first_survey["H_11/express_animal_dry_H"]
    unit_dry_animal = float(first_survey["H_11/animal_dry_H"])
    string_animal_dry_window = first_survey["H_11/usage_animal_dry_H"]
    pumping_head_animal = float(first_survey["H_11/pump_head_animal_H"])
    demand_time_animal = float(first_survey["H_11/animal_time_H"])

    if uom_dry_animal == "serv_liter":
        consume_dry_animal = unit_dry_animal
    elif uom_dry_animal == "serv_large_buck":
        consume_dry_animal = unit_dry_animal * large_buck
    elif uom_dry_animal == "serv_medium_buck":
        consume_dry_animal = unit_dry_animal * medium_buck
    elif uom_dry_animal == "serv_small_buck":
        consume_dry_animal = unit_dry_animal * small_buck

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
        consume_rainy_animal = unit_rainy_animal * large_buck
    elif uom_rainy_animal == "serv_medium_buck":
        consume_rainy_animal = unit_rainy_animal * medium_buck
    elif uom_rainy_irr == "serv_small_buck":
        consume_rainy_animal = unit_rainy_animal * small_buck

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

    anim_season_dict = rename_keys(season_dict_animal)

    animal_water_dict_H["animal_water_household"] = {
        "daily_demand": anim_season_dict,                                                         # animal water demand of typical day for each month
        "animal_window_dry": convert_usage_windows(dry_animal_usage_time),                        # animal water time window (dry season)
        "animal_window_rainy" : convert_usage_windows(rainy_animal_usage_time),                    # animal water time window (rainy season)
        "pumping_head": pumping_head_animal,
        "demand_duration": demand_time_animal
    }


# Get the parameters - Agro processing demand (Agroprocessing)
agroproc_dict = {}

if first_survey["G_0/respondent_type"] == "agroprocessing":
    for key, data in first_survey.items():
        if "AP_5/" in key and "_motor_AP" in key:
            mach_name = key.replace("AP_5/", "", 1).replace("_motor_AP", "", 1)  # machinery name
            fuel_AP = first_survey["AP_5/" + mach_name + "_motor_AP"]
            product = first_survey["AP_5/" + mach_name + "_prod_onerun_AP"]
            hourly_prod = first_survey["AP_5/" + mach_name + "_hour_prod_AP"]
            efficiency = first_survey["AP_5/" + mach_name + "_eff_AP"]
            hour_AP = first_survey["AP_5/" + mach_name + "_hour_AP"]
            string_AP = first_survey["AP_5/" + mach_name + "_usage_AP"]

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
                "fuel": fuel_AP,                                        # agroprocessing machine fuel
                "crop_processed_per_run": float(product),               # crop processed [kg] per run
                "throughput": float(hourly_prod),                       # [kg] of crop processed per [h] of machine operation
                "crop_processed_per_fuel": float(efficiency),           # crop processed [kg] per unit of fuel
                "usage_time": float(hour_AP) * 60,                      # machine operating usage time in min
                "time_window": convert_usage_windows(usage_AP_dict),    # machine usage windows
                "crop_processed_per_day": months_AP                     # crop processed on a typical working day for each months
            }

if first_survey["G_0/respondent_type"] == "local_aut":
    number_hh = float(first_survey["LA_2/HS_HH"])
    perc_low_income = float(first_survey["LA_2/HS_lower"])
    perc_medium_income = float(first_survey["LA_2/HS_middle"])
    perc_high_income = float(first_survey["LA_2/HS_upper"])

    primary_school = float(first_survey["LA_3/number_primary"])
    secondary_school = float(first_survey["LA_3/number_secondary"])
    hospital = float(first_survey["LA_4/number_hospital"])
    health_centre = float(first_survey["LA_4/number_hc"])
    church = float(first_survey["LA_5/number_church"])
    mosque = float(first_survey["LA_5/number_mosque"])

    mill = float(first_survey["LA_7/number_mill"])
    husker = float(first_survey["LA_7/number_husker"])
    other = float(first_survey["LA_7/number_other"])

    household_numerosity = {
        "low_income_hh" : number_hh * perc_low_income / 100,
        "medium_income_hh": number_hh * perc_medium_income / 100,
        "high_income_hh": number_hh * perc_high_income / 100,
    }

    service_numerosity = {
        "school_numerosity" : primary_school + secondary_school,
        "health_centre_numerosity" : hospital + health_centre,
        "church_moscque_numerosity" : church + mosque
    }

    agroprocessing_numerosity = {
        "mill_numerosity" : mill,
        "husker_numerosity": husker,
        "other_numerosity": other
    }


if first_survey["G_0/respondent_type"] == "business":
    business_dict = {'months_present':months_present,'working_days':working_days,'revenues_business':rev_B,'elec_demand_B':app_dict_B,'cooking_demand_B':cook_dict_B,'meal_B':meal_dict_B,'driking_water_B':drinking_water_dict_B,'service_water_B':service_water_dict_B}
    with open('business_dictionary.json', 'w') as json_file:
        json.dump(business_dict, json_file)

if first_survey["G_0/respondent_type"] == "household":
    household_dict = {'months_present':months_present,'working_days':hh_working_day,'total_saving_household':total_saving,'elec_demand_H':app_dict_H,'cooking_demand_H':cook_dict_H,'meal_H':meal_dict_H,'drinking_water_H':drinking_water_dict_H,'irrigation_water':irrigation_water_dict_H,'animal_water':animal_water_dict_H}
    with open('household_dictionary.json', 'w') as json_file:
        json.dump(household_dict, json_file)

if first_survey["G_0/respondent_type"] == "agroprocessing":
    agroprocessing_dict = {'working_days_AP':working_days_AP,'revenues_AP':rev_AP,'agroprocessing_dict':agroproc_dict}
    with open('agroprocessing_dictionary.json', 'w') as json_file:
        json.dump(agroprocessing_dict, json_file)

if first_survey["G_0/respondent_type"] == "service":
    service_dict = {'months_present':months_present,'working_days':serv_working_days,'elec_demand_S':app_dict_S}
    with open('service_dictionary.json', 'w') as json_file:
        json.dump(service_dict, json_file)

if first_survey["G_0/respondent_type"] == "local_aut":
    local_aut_dict = {'household':household_numerosity,'service':service_numerosity,'agroprocessing':agroprocessing_numerosity}
    with open('local_aut_dictionary.json', 'w') as json_file:
        json.dump(local_aut_dict, json_file)
