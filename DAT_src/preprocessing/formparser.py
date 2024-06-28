import numpy as np
from copy import copy


from preprocessing.defaults import prefix, suffix 
from preprocessing.defaults import months_present_defaults, working_day_default, months_of_presence, months_defaults, working_day
from preprocessing import utils


class FormParser():
	
	def __init__(self, form=None):
		self.form = form
		self.formtype = None
		self.suffix = None
		self.prefix = None

		self.cooking_demand = {}
		self.appliance_demand = {}
		self.drinking_water_demand = {}
		self.service_water_demand = {}
		self.agro_machine_demand = {}

		self.months_prefix = "G_1b"

		self.output_dict = {}

		if form is not None:
			self.init_parser(form)

	def init_parser(self, form):
		self.form = form
		self.check_form_type()
		self.assign_prefix_suffix()

	def create_dictionary(self):
		if self.prefix is not None and self.suffix is not None:
			self.output_dict['num_users'] = int(1) 
			self.output_dict['months_present'] = self.read_months_of_presence()
			self.output_dict['working_days'] = self.read_working_days(self.prefix['working_days'])
			self.output_dict["appliances"] = self.create_elec_appliance_demand(self.prefix['electric'])
			self.output_dict["cooking_demands"] = self.create_cooking_demand(self.prefix['cooking'],self.prefix['meal'])
			self.output_dict["drinking_water_demand"] = self.create_drinking_water_demand(self.prefix['driking_water'])
			self.output_dict["service_water_demands"] = self.create_service_water_demand(self.prefix['service_water'])
			
			if self.prefix['agro_machine'] is None:
				self.output_dict['agro_processing_machines'] = {}
			else:
				self.output_dict['agro_processing_machines'] = self.create_agroprocessing_demand(self.prefix['agro_machine'])
		else:
			raise BaseException("Please init the parser with giving a form before creating the dictionary")
	
	def check_form_type(self):
	    for form_t in ["business", "service", "agroprocessing", "local_aut"]:
	        if f"G_0/respondent_{form_t}" in self.form.keys() and self.form[f"G_0/respondent_{form_t}"] == "yes":
	            self.formtype = form_t
	    if self.formtype is None:
		    self.formtype = "household"

	def assign_prefix_suffix(self):
		if self.formtype is not None:
			self.prefix = prefix[self.formtype]
			self.suffix = suffix[self.formtype]
		else:
			raise ValueError("Missing form type")

	def create_cooking_demand(self, cooking_prefix, meal_prefix):
	    cook_dic = self.read_cooking(cooking_prefix)
	    meal_dic = self.read_meal(meal_prefix, cook_dic.keys())

	    for key in meal_dic.keys():
	    	meal_dic[key]['fuel_amount'] = cook_dic[meal_dic[key]['fuel']]['fuel_amount']

	    self.cooking_demand =  meal_dic

	    return self.cooking_demand

	def create_service_water_demand(self, prefix):
		if type(prefix) is dict:
		    irr_dict = self.read_irr_water(prefix['irrigation_water'])
		    animal_dict = self.read_animal_water(prefix['animal_water'], prefix['irrigation_water'])
		    
		    self.service_water_demand = {"irrigation":irr_dict,"livestock": animal_dict} 
		    return self.service_water_demand
		else:
			self.service_water_demand = {'livestock': self.read_service_water(prefix)}
			return self.service_water_demand

	def create_drinking_water_demand(self, drinking_prefix):
	    unit_of_measurement = self.form[f"{drinking_prefix}/drinking_express{self.suffix}"]
	    unit = float(self.form[f"{drinking_prefix}/drink_use{self.suffix}"])
	    string_drink_window = self.form[f"{drinking_prefix}/drink_time{self.suffix}"]

	    if "buck" in unit_of_measurement:
	    	buck_conversion = float(self.form[f"{drinking_prefix}/drink_dim{self.suffix}"])
	    else:
	    	buck_conversion = None

	    consume = utils.convert_perliter(unit_of_measurement, unit, buck_conversion)
	    drink_usage_time = utils.exctract_time_window(string_drink_window)

	    time_window = self.form[f"{drinking_prefix}/drink_time{self.suffix}"].split()

	    #self.drinking_water_demand = {"daily_demand" : consume, "water_window" : utils.convert_usage_windows(drink_usage_time) }
	    self.drinking_water_demand = {"daily_demand" : consume }
	    win = utils.convert_usage_windows_2(drink_usage_time)
	    for key, item in win.items():
	    	self.drinking_water_demand[f'water_{key}'] = item
	    return self.drinking_water_demand

	def create_elec_appliance_demand(self, electric_prefix):
	    app_dict = {}

	    for key, data in self.form.items():
	        if electric_prefix in key and "_power" in key :
	            app_name = key.split(sep="/")[1].split(sep="_power")[0]
	            number = float(self.form[f"{electric_prefix}/{app_name}_number{self.suffix}"])
	            power = float(self.form[f"{electric_prefix}/{app_name}_power{self.suffix}"])
	            hour = float(self.form[f"{electric_prefix}/{app_name}_hour_wd{self.suffix}"])
	            switch_on = int(self.form[f"{electric_prefix}/{app_name}_min_on{self.suffix}"])
	            string = self.form[f"{electric_prefix}/{app_name}_usage_wd{self.suffix}"]

	            usage_wd_dict = utils.exctract_time_window(string)

	            usage_wd = utils.convert_usage_windows_2(usage_wd_dict)

	            app_dict[app_name] = {
	                "num_app" : number,                                   # quantity of appliance
	                "power" : power,                                     # appliance power in W
	                "daily_usage_time": hour,                               # appliance operating usage time in min
	                "func_cycle": switch_on,
	                #"time_window_1" : usage_wd                           # appliance usage windows
	            }
	            for key, item in usage_wd.items():
	            	app_dict[app_name][f"usage_{key}"] = item

	    self.appliance_demand = app_dict
	    #print(self.appliance_demand)
	    return self.appliance_demand

	def create_agroprocessing_demand(self, agro_prefix):
	    for key, data in self.form.items():
	        if f"{agro_prefix}/" in key and f"_motor{self.suffix}" in key:
	            mach_name = key.replace(f"{agro_prefix}/", "", 1).replace(f"_motor{self.suffix}", "", 1)  # machinery name
	            fuel_AP = self.form[f"{agro_prefix}/{mach_name}_motor{self.suffix}"]
	            product = self.form[f"{agro_prefix}/{mach_name}_prod_onerun{self.suffix}"]
	            hourly_prod = self.form[f"{agro_prefix}/{mach_name}_hour_prod{self.suffix}"]
	            efficiency = self.form[f"{agro_prefix}/{mach_name}_eff{self.suffix}"]
	            hour_AP = self.form[f"{agro_prefix}/{mach_name}_hour{self.suffix}"]
	            string_AP = self.form[f"{agro_prefix}/{mach_name}_usage{self.suffix}"]


	            usage_AP_dict = utils.exctract_time_window(string_AP)

	            months_AP = {
	                'January': float(self.form[f"{agro_prefix}/{mach_name}_prod_jan{self.suffix}"]),
	                'February': float(self.form[f"{agro_prefix}/{mach_name}_prod_feb{self.suffix}"]),
	                'March': float(self.form[f"{agro_prefix}/{mach_name}_prod_mar{self.suffix}"]),
	                'April': float(self.form[f"{agro_prefix}/{mach_name}_prod_apr{self.suffix}"]),
	                'May': float(self.form[f"{agro_prefix}/{mach_name}_prod_may{self.suffix}"]),
	                'June': float(self.form[f"{agro_prefix}/{mach_name}_prod_jun{self.suffix}"]),
	                'July': float(self.form[f"{agro_prefix}/{mach_name}_prod_jul{self.suffix}"]),
	                'August': float(self.form[f"{agro_prefix}/{mach_name}_prod_aug{self.suffix}"]),
	                'September': float(self.form[f"{agro_prefix}/{mach_name}_prod_sep{self.suffix}"]),
	                'October': float(self.form[f"{agro_prefix}/{mach_name}_prod_oct{self.suffix}"]),
	                'November': float(self.form[f"{agro_prefix}/{mach_name}_prod_nov{self.suffix}"]),
	                'December': float(self.form[f"{agro_prefix}/{mach_name}_prod_dec{self.suffix}"])
	            }

	            for k in months_AP:
	                months_AP[k] = utils.convert_perday(months_AP[k], self.form[f"{agro_prefix}/{mach_name}_prod_exp{self.suffix}"])
	            months_AP = utils.rename_keys(months_AP)

	            if mach_name == 'husker':
	            	mach_name = 'husking_mill'

	            self.agro_machine_demand[mach_name] = {
	                "fuel": fuel_AP,                                        # agroprocessing machine fuel
	                "crop_processed_per_run": float(product),               # crop processed [kg] per run
	                "throughput": float(hourly_prod),                       # [kg] of crop processed per [h] of machine operation
	                "crop_processed_per_fuel": float(efficiency),           # crop processed [kg] per unit of fuel
	                "usage_time": float(hour_AP),                      # machine operating usage time in min
	                #"time_window": utils.convert_usage_windows(usage_AP_dict),    # machine usage windows
	                "crop_processed_per_day": months_AP                     # crop processed on a typical working day for each months
	            }
	            for key, item in utils.convert_usage_windows_2(usage_AP_dict).items():
		            self.agro_machine_demand[mach_name][f'usage_{key}'] = item

	    return self.agro_machine_demand

	# reading functions

	def read_working_days(self, prefix):
		if prefix is not None:
			string_day = self.form[f"{prefix}/working_day{self.suffix}"]
			working = []

			for day in working_day:
				if day in string_day:
					working.append(working_day[day])

			return working
		else:
			return list(range(7))      

	def read_months_of_presence(self):
		string_months = self.form[f'{self.months_prefix}/residency_month']
		months = []
		for month in months_of_presence.keys():
		        if month in string_months:
		            months.append(months_of_presence[month])
		return months

	def read_irr_water(self, irr_water_prefix):
	    if self.form[f"{irr_water_prefix}/irrigation{self.suffix}"] == "yes":

	        pumping_head_irr = float(self.form[f"{irr_water_prefix}/pump_head_irr{self.suffix}"])
	        demand_time_irr = float(self.form[f"{irr_water_prefix}/irr_time{self.suffix}"])

	        uom_dry_irr = self.form[f"{irr_water_prefix}/express_dry{self.suffix}"]
	        unit_dry_irr = float(self.form[f"{irr_water_prefix}/irrigation_dry{self.suffix}"])
	        string_irr_dry_window = self.form[f"{irr_water_prefix}/usage_dry{self.suffix}"]

	       	if "buck" in uom_dry_irr:
	        	buck_conversion = float(self.form[f"{irr_water_prefix}/dim_dry{self.suffix}"])
	        else:
	        	buck_conversion = None

	        consume_dry_irr = utils.convert_perliter(uom_dry_irr, unit_dry_irr,buck_conversion)
	        dry_irr_usage_time = utils.exctract_time_window(string_irr_dry_window)

	        uom_rainy_irr = self.form[f"{irr_water_prefix}/express_rainy{self.suffix}"]
	        unit_rainy_irr = float(self.form[f"{irr_water_prefix}/irrigation_rainy{self.suffix}"])
	        string_irr_rainy_window = self.form[f"{irr_water_prefix}/usage_rainy{self.suffix}"]

	        if "buck" in uom_rainy_irr:
	        	buck_conversion = float(self.form[f"{irr_water_prefix}/dim_rainy{self.suffix}"])
	        else:
	        	buck_conversion = None

	        consume_rainy_irr = utils.convert_perliter(uom_rainy_irr, unit_rainy_irr, buck_conversion)
	        rainy_irr_usage_time = utils.exctract_time_window(string_irr_rainy_window)

	        string_rainy = self.form[f"{irr_water_prefix}/dry_season{self.suffix}"]
	        
	        season_dict = copy(months_present_defaults)
	        for month in season_dict:
	        	if month in string_rainy:
	        		season_dict[month] = consume_rainy_irr
	        	else:
	        		season_dict[month] = consume_dry_irr

	        irr_season_dict = utils.rename_keys(season_dict)

	        irr_windows = {}

	        for k in dry_irr_usage_time.keys():
	        	irr_windows[k] = dry_irr_usage_time[k]+rainy_irr_usage_time[k]

	        out_windows = utils.convert_usage_windows(irr_windows)
	        if len(out_windows) < 3:
	        	out_windows.append(None)
	        elif len(out_windows) > 3:
	        	raise BaseException("got a problem, more than 3 windows")

	        return {
	            "daily_demand": irr_season_dict,                                        # irrigation water demand of typical day for each month
	            #"irr_window_dry": utils.convert_usage_windows(dry_irr_usage_time),      # irrigation water time window (dry season)
	            #"irr_window_rainy" : utils.convert_usage_windows(rainy_irr_usage_time), # irrigation water time window (rainy season)
	            "usage_windows": out_windows,
	            "pumping_head": pumping_head_irr,
	            "demand_duration": demand_time_irr
	        }
	    else:
	    	return {}

	def read_animal_water(self, a_water_prefix, irr_water_prefix):
	    if self.form[f"{a_water_prefix}/animal_water{self.suffix}"] == "yes":
	        pumping_head_animal = float(self.form[f"{a_water_prefix}/pump_head_animal{self.suffix}"])
	        demand_time_animal = float(self.form[f"{a_water_prefix}/animal_time{self.suffix}"])

	        uom_dry_animal = self.form[f"{a_water_prefix}/express_animal_dry{self.suffix}"]
	        unit_dry_animal = float(self.form[f"{a_water_prefix}/animal_dry{self.suffix}"])
	        string_animal_dry_window = self.form[f"{a_water_prefix}/usage_animal_dry{self.suffix}"]

	        if "buck" in uom_dry_animal:
	        	buck_conversion = float(self.form[f"{a_water_prefix}/dim_anim_dry{self.suffix}"])
	        else:
	        	buck_conversion = None

	        consume_dry_animal = utils.convert_perliter(uom_dry_animal, unit_dry_animal, buck_conversion)
	        dry_animal_usage_time = utils.exctract_time_window(string_animal_dry_window)

	        uom_rainy_animal = self.form[f"{a_water_prefix}/express_animal_rainy{self.suffix}"]
	        unit_rainy_animal = float(self.form[f"{a_water_prefix}/animal_rainy{self.suffix}"])
	        string_animal_rainy_window = self.form[f"{a_water_prefix}/usage_animal_rainy{self.suffix}"]

	        if "buck" in uom_rainy_animal:
	        	buck_conversion = float(self.form[f"{a_water_prefix}/dim_anim_rainy{self.suffix}"])
	        else:
	        	buck_conversion = None

	        consume_rainy_animal = utils.convert_perliter(uom_rainy_animal, unit_rainy_animal, buck_conversion)
	        rainy_animal_usage_time = utils.exctract_time_window(string_animal_rainy_window)

	        string_rainy_animal = self.form[f"{irr_water_prefix}/dry_season{self.suffix}"]
	        season_dict_animal = copy(months_present_defaults)

	        for month in season_dict_animal:
	            if month in string_rainy_animal:
	                season_dict_animal[month] = consume_rainy_animal
	            else:
	                season_dict_animal[month] = consume_dry_animal

	        anim_season_dict = utils.rename_keys(season_dict_animal)

	        a_windows = {}

	        for k in dry_animal_usage_time.keys():
	        	a_windows[k] = dry_animal_usage_time[k]+rainy_animal_usage_time[k]

	        out_windows = utils.convert_usage_windows(a_windows)
	        if len(out_windows) < 3:
	        	out_windows.append(None)
	        elif len(out_windows) > 3:
	        	raise BaseException("got a problem, more than 3 windows")

	        return {
	            "daily_demand": anim_season_dict,                                                         # animal water demand of typical day for each month
	            #"animal_window_dry": utils.convert_usage_windows(dry_animal_usage_time),                        # animal water time window (dry season)
	            #"animal_window_rainy" : utils.convert_usage_windows(rainy_animal_usage_time),                    # animal water time window (rainy season)
	            "usage_windows" : out_windows,
	            "pumping_head": pumping_head_animal,
	            "demand_duration": demand_time_animal
	        }
	    else:
	    	return {}

	def read_service_water(self, prefix):
		service_water_dict_B = {}

		unit_of_measurement_serv = self.form[f"{prefix}/service_express{self.suffix}"]
		unit_serv = float(self.form[f"{prefix}/serv_use{self.suffix}"])
		string_serv_window = self.form[f"{prefix}/serv_time{self.suffix}"]
		pumping_head = float(self.form[f"{prefix}/pump_head{self.suffix}"])
		demand_time = float(self.form[f"{prefix}/serv_duration{self.suffix}"])

		if "buck" in unit_of_measurement_serv:
			buck_conversion = float(self.form[f"{prefix}/serv_dim{self.suffix}"])
		else:
			buck_conversion = None

		consume_serv = utils.convert_perliter(unit_of_measurement_serv, unit_serv, buck_conversion)
		service_usage_time = utils.exctract_time_window(string_serv_window)

		daily_demand = copy(months_defaults)
		daily_water_demand = utils.set_values(daily_demand, consume_serv)

		out_windows = utils.convert_usage_windows(service_usage_time)
		while len(out_windows) < 3:
			out_windows.append(None)

		return {
	        "daily_demand": daily_water_demand,
	        "usage_windows": out_windows,
	        "pumping_head" : pumping_head,
	        "demand_duration" : demand_time
	    }

	def read_cooking(self, cooking_prefix):
	    cook_dict = {}

	    for key, data in self.form.items():
	        if cooking_prefix in key and "unit" in key:
	            fuel_name = key.replace(cooking_prefix,"", 1).replace(f"_unit{self.suffix}","",1)
	            time_cons = self.form[f"{cooking_prefix}{fuel_name}_time{self.suffix}"]
	            unit = self.form[f"{cooking_prefix}{fuel_name}_unit{self.suffix}"]
	            quantity = float(self.form[f"{cooking_prefix}{fuel_name}_amount{self.suffix}"])

	            if unit == "bag" or unit == "cylinder":
	                bag_to_kg = float(self.form[f"{cooking_prefix}{fuel_name}_bag{self.suffix}"])
	            else:
	                bag_to_kg = None

	            q = utils.convert_perkg(quantity, unit, fuel_name, bag_to_kg)
	            daily_cons = utils.convert_perday(q, time_cons)

	            cook_dict[fuel_name.split(sep="/")[1]] = {
	            "time": time_cons,                                  # time window to express fuel consumption
	            "unit": unit,                                       # unit to express fuel consumption
	            "quantity": quantity,                               # quantity of unit consumption in the time window
	            "fuel_amount": daily_cons                           # daily fuel consumption
	            }

	    return cook_dict 

	def read_meal(self, meal_prefix, cooking_fuels):
	    meal_dict = {}
	    for key, data in self.form.items():
	        if meal_prefix in key and "meal_per_day" in key:
	            n_meal = utils.how_many_meal(self.form[f"{meal_prefix}/meal_per_day{self.suffix}"])

	            for n in np.arange(n_meal)+1:
	                fuel = self.form[f"{meal_prefix}/fuels_meal{n}{self.suffix}"].split(sep="_")[1]
	                if fuel not in cooking_fuels:
	                    raise ValueError("This fuel has not be defined in cooking fuels")

	                cooking_device = self.form[f"{meal_prefix}/cooking_meal{n}{self.suffix}"]
	                string_meal_window = self.form[f"{meal_prefix}/usage_meal{n}{self.suffix}"]
	                cooking_time = float(self.form[f"{meal_prefix}/time_meal{n}{self.suffix}"])
        	        meal_usage_time = utils.exctract_time_window(string_meal_window)

	                meal_time_window = utils.convert_usage_windows(meal_usage_time)

	                meal_dict[f'meal_{n}'] = {
	                "fuel" : fuel,                                   # fuel used for meals
	                "stove" : cooking_device,                        # stove used for meals
	                "cooking_window_start" : meal_time_window[0][0],      # meals time window
	                "cooking_window_end": meal_time_window[0][1],
	                #"cooking_time": float(meal_time_window[0][1])-float(meal_time_window[0][0]) # Simone defined cooking time like this, but we have the question for this
	                "cooking_time": cooking_time # <-- this has to be < window_time 
	                } 
	    return meal_dict


if __name__ == "__main__":

    forms = utils.get_survey(survey_id="atiMZ5E4jaZHv37TUekb6N")
    formparser = FormParser(forms[3])
    formparser.create_dictionary()

    #print(formparser.appliance_demand)
    #print(formparser.cooking_demand)
    #print(formparser.output_dict['cooking_demand'])

    print(formparser.formtype)
    #print(formparser.output_dict['appliances'])

    print(formparser.output_dict['service_water_demands'])

    