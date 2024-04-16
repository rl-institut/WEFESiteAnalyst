import ramp
import pandas as pd
import numpy as np
import copy
from tqdm import tqdm

from helpers.exceptions import MissingInput


class RampControl:
    """
    - !!
    """

    def __init__(self, number_of_days, start_date):
        self.number_of_days = number_of_days
        self.min_timeseries = pd.date_range(start_date, periods=number_of_days * 24 * 60, freq="Min")
        self.days_timeseries = pd.date_range(start_date, periods=number_of_days, freq="D")

    def run_use_cases(self, use_cases_list, user_data, description):
        """

        :param use_cases_list:
        :param user_data:
        :param description: description to show in progress bar of this run of use cases
        :return:
        """

        # Dict to store generated demand profiles
        demand_profiles = {}

        # Day of year counter
        day_counter = 0
        for entry in tqdm(use_cases_list, desc=description):

            use_case = entry[0]  # use_case object is first entry in tuple in use_cases_list
            use_case_month = entry[1]  # month number of the use_case is second entry

            # Calculate peak time range of this use case
            peak_time_range = use_case.calc_peak_time_range()

            if len(peak_time_range) == 0:
                print('Alert')

            # Loop through all days of this month's use_case

            for day in self.days_timeseries[self.days_timeseries.month == use_case_month]:
                # Return weekday of this day (Monday=0, Sunday=6)
                weekday = day.weekday()
                # Loop through all user instances (= user types)
                for user in use_case.users:

                    # Check if user_name does not exist in demand_profiles dict yet (=first day to be simulated)
                    if user.user_name not in demand_profiles:
                        # Create dict entry for every user
                        demand_profiles[user.user_name] = {}

                    # Check if current weekday is working day of the user
                    if weekday in user_data[user.user_name]['working_days']:
                        day_type = 0  # set day_type=0 -> working day
                    else:
                        day_type = 1   # set day_type=1 -> holiday

                    # Loop through each user of this user type
                    for _ in range(user.num_users):
                        # Loop through user's appliances
                        for appliance in user.App_list:
                            # Check if there is no dict entry for this appliance yet in the load profiles dict
                            # (= first day of simulation)
                            if appliance.name not in demand_profiles[user.user_name]:  #
                                # Create dict entry for this appliance with pre-allocated 2D numpy array
                                # 1440 (minute) timesteps for each day to be simulated
                                demand_profiles[user.user_name][appliance.name] = np.zeros((self.number_of_days, 1440))

                            # --- Generate appliance load profile ---
                            # Generate a daylong profile with 1-min resolution (1440 time steps) for this appliance
                            # Load profile is not returned but saved in the appliance's daily_use attribute
                            appliance.generate_load_profile(
                                prof_i=0,  # Day of the year in RAMP core. Not used here, thus always 0
                                peak_time_range=peak_time_range,
                                day_type=day_type,  # Day type: 0->working day, 1->holiday
                                power=appliance.power  # Power of the appliance at this day
                            )

                            # Add this appliance load profile to the day's load profile
                            demand_profiles[user.user_name][appliance.name][day_counter] += appliance.daily_use

                # Increase day counter
                day_counter += 1

        # Create dataframe from dict
        # Loop through all users for which load profiles where generated
        for user, user_dp in demand_profiles.items():
            # Loop through every appliance
            for app, app_dp in user_dp.items():
                # Turn 2D numpy array: [day_of_timeframe, min_of_day] into 1D numpy array: [min_of_timeframe]
                user_dp[app] = app_dp.reshape(1, len(app_dp) * 1440).squeeze()

            # Create dataframe of load profiles of this user's appliances
            demand_profiles[user] = pd.DataFrame(user_dp)

        # Concat dataframe of each user in multi-level column dataframe and return
        df = pd.concat(demand_profiles, axis=1)
        df['datetime'] = self.min_timeseries
        df.set_index('datetime', drop=True, inplace=True)
        return df

    def generate_cooking_demand_use_cases(self, cooking_input_data, admin_input):
        """
        Generate one RAMP use_case for every month of the year
        - this way the seasonality of demands can be represented
        - for electrical appliances, cooking energy and drinking water demands, it is only relevant if the user reports
          being present in the settlement during the month of the year
        - for service water (livestock and irrigation) and agro-processing demand the usage_time of the appliances
          changes depending on the month
        :param cooking_input_data:
        :param admin_input
        :return:
        """

        # List for every month's use case
        cooking_demand_use_cases_list = []
        # Loop through every month of the year
        for month in range(1, 13):
            # Create dict to store generated RAMP user instances
            ramp_users_dict = {}
            # Loop through every survey respondent.
            for user_name, user_data in cooking_input_data.items():
                # Create user instance for this household survey respondent
                new_user = ramp.User(
                    user_name=user_name,
                    num_users=user_data['num_users']
                )

                # Check if this household survey respondent is present in the settlement during this month
                if month in user_data['months_present']:
                    present = True
                else:
                    present = False

                # Add cooking demands to this user
                for cooking_demand_name, cooking_demand_data in user_data['cooking_demands'].items():
                    # Get cooking window of this cooking demand -> turn into minutes

                    cooking_window = [cooking_demand_data['cooking_window_start'] * 60,
                                      cooking_demand_data['cooking_window_end'] * 60]

                    # Get cooking metadata
                    cooking_metadate = admin_input['cooking_metadata']

                    # Get cooking and stove data of fuel used for this cooking demand
                    fuel_data = admin_input['cooking_metadata']['cooking_fuels'][cooking_demand_data['fuel']]
                    stove_data = admin_input['cooking_metadata']['cooking_stoves'][cooking_demand_data['stove']]

                    # Calculate thermal power of this cooking demand in W !!
                    # Thermal_power = ((fuel_amount_of_meal * energy_content * stove_efficiency) / cooking_time) * 1000
                    cooking_power = int(
                        ((cooking_demand_data['fuel_amount'] * fuel_data['energy_content'] * stove_data['efficiency']) /
                         cooking_demand_data['cooking_time']) * 1000)

                    if present:  # if user is present
                        func_time = int(cooking_demand_data['cooking_time'] * 60)  # Duration of this cooking demand
                    else:  # if not present
                        func_time = 0  # func_time of cooking demand is 0 -> therefore no demand is modeled

                    # Add appliance to user instance
                    new_user.add_appliance(
                        name=cooking_demand_name,  # Name of cooking demand
                        number=1,  # Every cooking demand exist only once per user
                        power=cooking_power,  # Thermal power of this cooking demand
                        num_windows=1,  # One time window per cooking demand
                        window_1=cooking_window,  # Set time window of cooking demand

                        func_time=func_time,  # Duration of this cooking demand
                        func_cycle=func_time,  # Duration of this cooking demand is also func_cycle
                        time_fraction_random_variability=cooking_metadate['cooking_time_variability'],

                        fixed_cycle=1,  # every cooking demand has one duty cycle

                        p_11=cooking_power,  # first part of duty cycle: power = cooking_power,
                        t_11=func_time,  # first part of duty cycle: duration = cooking_time
                        p_12=0,  # second part of duty cycle is unused -> assume constant power -> power and time = 0
                        t_12=0,  # steady state duration = total duration - start-up time
                        r_c1=cooking_metadate['cooking_time_variability'],  # random variability of cooking duration
                        wd_we_type=2,  # Cooking demand is used on every weekday (simplification for now)

                        random_var_w=cooking_metadate['cooking_window_variability']
                    )

                # Add deepcopy of user instance to ramp_user_dict
                ramp_users_dict[user_name] = copy.deepcopy(new_user)

            # Create RAMP use_case
            cooking_demand_use_case = ramp.UseCase(
                name='cooking_demand',
                users=list(ramp_users_dict.values())
            )
            cooking_demand_use_cases_list.append((cooking_demand_use_case, month))  # add tuple of (use_case, month)
        return cooking_demand_use_cases_list

    def generate_electric_appliances_use_cases(self, input_data, admin_input):

        # List for every month's use case
        electric_appliances_use_cases_list = []

        for month in range(1, 13):
            # Create dict to store generated RAMP user instances
            ramp_users_dict = {}
            # Loop through every household survey respondent.
            for user_name, user_data in input_data.items():
                # Create user instance for this household survey respondent
                new_user = ramp.User(
                    user_name=user_name,
                    num_users=user_data['num_users']
                )

                # Check if this household survey respondent is present in the settlement during this month
                if month in user_data['months_present']:
                    present = True
                else:
                    present = False

                # Add appliances to this user.
                for appliance_name, appliance_data in user_data['appliances'].items():
                    # Get appliance's metadata
                    appliance_metadata = admin_input['appliance_metadata'][appliance_name]

                    # Get appliance's usage windows
                    # Definition of usage windows is extremely messy. Propose to RAMP core to define usage windows in list?
                    usage_windows = [  # Create list of usage windows
                        np.array(appliance_data['usage_window_1'])*60 if 'usage_window_1' in appliance_data.keys() else
                        None,
                        np.array(appliance_data['usage_window_2'])*60 if 'usage_window_2' in appliance_data.keys() else
                        None,
                        np.array(appliance_data['usage_window_3'])*60 if 'usage_window_3' in appliance_data.keys() else
                        None,
                    ]
                    num_usage_windows = sum(x is not None for x in usage_windows)  # Count how many windows are not none

                    if present:  # if user is present
                        func_time = int(appliance_data['daily_usage_time'] * 60)  # Func_time as specified
                        func_cycle = appliance_data['func_cycle']
                    else:  # if not present
                        func_time = 0  # func_time is 0 -> therefore no demand is modeled
                        # func_cycle needs to be set to 0, otherwise RAMP core increases func_time to be >= func_cycle
                        func_cycle = 0


                    # Add appliance to user instance
                    new_user.add_appliance(
                        name=appliance_name,  # Name of the appliance as specified in survey response
                        number=appliance_data['num_app'],  # Number of identical appliances of this type that this user owns
                        power=appliance_data['power'],  # Power of the appliance (actual power drawn, not nominal power)

                        func_time=func_time,  # Total time of use per day
                        time_fraction_random_variability=appliance_metadata['daily_use_variability'],
                        # Fraction of daily usage time which is subject to random variability
                        func_cycle=func_cycle,

                        # Check if windows are given and set them
                        # If no windows are specified,
                        num_windows=num_usage_windows,
                        window_1=usage_windows[0],
                        window_2=usage_windows[1],
                        window_3=usage_windows[2],

                        random_var_w=appliance_metadata['usage_window_variability'],
                        # appliance is only used on (RAMP-) workdays. User-individual workdays are checked when running
                        # use_cases
                        wd_we_type=0  # 0 -> working days
                    )

                # Add deepcopy of user instance to ramp_user_dict
                ramp_users_dict[user_name] = copy.deepcopy(new_user)

            # Create RAMP use_case
            electric_appliances_use_case = ramp.UseCase(
                name='household_elec',
                users=list(ramp_users_dict.values())
            )

            electric_appliances_use_cases_list.append((electric_appliances_use_case, month))

        return electric_appliances_use_cases_list

    def generate_agro_processing_use_cases(self, input_data, admin_input):

        # List for every month's use case
        agro_processing_use_cases_list = []

        for month in range(1, 13):
            # Create dict to store generated RAMP user instances
            ramp_users_dict = {}
            # Loop through every household survey respondent.
            for user_name, user_data in input_data.items():
                # Create user instance for this household survey respondent
                new_user = ramp.User(
                    user_name=user_name,
                    num_users=user_data['num_users']
                )

                # Add appliances to this user.
                for appliance_name, appliance_data in user_data['agro_processing_machines'].items():
                    # Get appliance's metadata
                    appliance_metadata = admin_input['agro_processing_metadata'][appliance_name]

                    # Get appliance's usage windows
                    usage_windows = [  # Create list of usage windows
                        np.array(appliance_data['usage_window_1'])*60 if 'usage_window_1' in appliance_data.keys() else
                        None,
                        np.array(appliance_data['usage_window_2'])*60 if 'usage_window_2' in appliance_data.keys() else
                        None,
                        np.array(appliance_data['usage_window_3'])*60 if 'usage_window_3' in appliance_data.keys() else
                        None,
                    ]
                    num_usage_windows = sum(x is not None for x in usage_windows)  # Count how many windows are not none

                    # Get data of used fuel
                    fuel_data = admin_input['agro_processing_metadata']['agro_processing_fuels'][appliance_data['fuel']]

                    # Calculate machine's mechanical power
                    mech_power = int((1 / appliance_data['crop_processed_per_fuel']) * fuel_data['energy_content'] *
                                  appliance_data['throughput']*1000)

                    # Calculate machine's daily usage time (=func_time)
                    func_time = int((appliance_data['crop_processed_per_day'][month] / appliance_data['throughput']) *
                                    60)

                    # Calculate machine's typical duty cycle duration
                    func_cycle = int((appliance_data['crop_processed_per_run'] / appliance_data['throughput']) * 60)

                    # Add appliance to user instance
                    new_user.add_appliance(
                        name=appliance_name,  # Name of the appliance as specified in survey response
                        number=1,  # Number of machines fixed to 1 -> collect every machine separately
                        power=mech_power,  # Power of the appliance (actual power drawn, not nominal power)

                        func_time=func_time,  # Total time of use per day
                        time_fraction_random_variability=appliance_metadata['daily_use_variability'],
                        # Fraction of daily usage time which is subject to random variability
                        func_cycle=func_cycle,

                        # Check if windows are given and set them
                        # If no windows are specified,
                        num_windows=num_usage_windows,
                        window_1=usage_windows[0],
                        window_2=usage_windows[1],
                        window_3=usage_windows[2],

                        random_var_w=appliance_metadata['usage_window_variability'],
                        # appliance is only used on (RAMP-) workdays. User-individual workdays are checked when
                        # simulating use_cases
                        wd_we_type=0,  # 0 -> working days

                        fixed_cycle=1,  # one duty cycle per machine

                        p_11=mech_power,  # first part of duty cycle
                        t_11=func_cycle,  # first part of duty cycle
                        p_12=0,  # second part of duty cycle is unused -> assume constant power -> power and time = 0
                        t_12=0,  # steady state duration = total duration - start-up time
                        r_c1=appliance_metadata['processed_per_run_variability'],  # random variability of duty_cycle
                    )

                # Add deepcopy of user instance to ramp_user_dict
                ramp_users_dict[user_name] = copy.deepcopy(new_user)

            # Create RAMP use_case
            agro_processing_use_case = ramp.UseCase(
                name='agro_processing',
                users=list(ramp_users_dict.values())
            )

            agro_processing_use_cases_list.append((agro_processing_use_case, month))

        return agro_processing_use_cases_list

    def generate_drinking_water_use_cases(self, input_data):

        # List for every month's use case
        drinking_water_use_cases_list = []

        for month in range(1, 13):
            # Create dict to store generated RAMP user instances
            ramp_users_dict = {}
            # Loop through every household survey respondent.
            for user_name, user_data in input_data.items():
                # Create user instance for this household survey respondent
                new_user = ramp.User(
                    user_name=user_name,
                    num_users=user_data['num_users']
                )

                # Check if this household survey respondent is present in the settlement during this month
                if month in user_data['months_present']:
                    present = True
                else:
                    present = False

                drinking_water_demand = user_data['drinking_water_demand']
                # Drinking water windows
                # Definition of usage windows is extremely messy. Propose to RAMP core to define usage windows in list?
                usage_windows = [  # Create list of usage windows
                    np.array(drinking_water_demand['water_window_1']) * 60 if 'water_window_1' in
                                                                              drinking_water_demand.keys() else None,
                    np.array(drinking_water_demand['water_window_2']) * 60 if 'water_window_2' in
                                                                              drinking_water_demand.keys() else None,
                    np.array(drinking_water_demand['water_window_3']) * 60 if 'water_window_3' in
                                                                              drinking_water_demand.keys() else None,
                ]
                num_usage_windows = sum(x is not None for x in usage_windows)  # Count how many windows are not none

                if present:  # if user is present
                    func_time = num_usage_windows  # one peak (="water-fetching") per num of usage windows
                    func_cycle = 1  # water demand is always represented by "1-min peak"
                else:  # if not present
                    func_time = 0  # func_time is 0 -> therefore no demand is modeled

                # Add appliance to user instance
                new_user.add_appliance(
                    name='drinking_water_demand',
                    number=1,
                    power=drinking_water_demand['daily_demand']/num_usage_windows,
                    func_time=func_time,
                    time_fraction_random_variability=0,  # no random variability of drinking water use

                    # Check if windows are given and set them
                    # If no windows are specified,
                    num_windows=num_usage_windows,
                    window_1=usage_windows[0],
                    window_2=usage_windows[1],
                    window_3=usage_windows[2],

                    fixed_cycle=1,

                    p_11=drinking_water_demand['daily_demand']/num_usage_windows,
                    t_11=1,
                    p_12=0,
                    t_12=0,
                    r_c1=0,  # no random variability of drinking water use
                    wd_we_type=2,  # Drinking water demand is the same on every weekday
                )

                # Add deepcopy of user instance to ramp_user_dict
                ramp_users_dict[user_name] = copy.deepcopy(new_user)

            # Create RAMP use_case
            drinking_water_use_case = ramp.UseCase(
                name='drinking_water',
                users=list(ramp_users_dict.values())
            )

            drinking_water_use_cases_list.append((drinking_water_use_case, month))

        return drinking_water_use_cases_list

    def generate_service_water_use_cases(self, input_data, admin_input):

        # List for every month's use case
        service_water_use_cases_list = []

        for month in range(1, 13):
            # Create dict to store generated RAMP user instances
            ramp_users_dict = {}
            # Loop through every survey respondent.
            for user_name, user_data in input_data.items():
                # Create user instance for this household survey respondent
                new_user = ramp.User(
                    user_name=user_name,
                    num_users=user_data['num_users']
                )

                for demand_name, demand_data in user_data['service_water_demands'].items():

                    try:
                        demand_metadata = admin_input['service_water_metadata'][demand_name]
                    except KeyError:
                        raise MissingInput('%s: No metadate provided in admin input.' % demand_name)

                    # Count how many usage windows are defined
                    num_usage_windows = sum(x is not None for x in demand_data['usage_windows'])  # Count how many windows are not none
                    if num_usage_windows > 3:
                        print("Survey respondent: %s - Demand: %s: More than 3 usage windows were defined. "
                              "Only the first 3 are considered" % (user_name, demand_name))
                        num_usage_windows = 3

                    # Get this month's daily volume of this demand
                    daily_demand = demand_data['daily_demand'][month]

                    # Add appliance to user instance
                    new_user.add_appliance(
                        name=demand_name,
                        number=1,  # Each water demand is modeled separately
                        power=daily_demand/(demand_data['demand_duration']*60),  # = flow rate: total_demand/duration
                        func_time=demand_data['demand_duration']*60,
                        time_fraction_random_variability=demand_metadata['daily_demand_variability'],

                        num_windows=num_usage_windows,
                        window_1=minutes_wd(demand_data['usage_windows'][0]),
                        window_2=minutes_wd(demand_data['usage_windows'][1]),
                        window_3=minutes_wd(demand_data['usage_windows'][2]),

                        wd_we_type=2,  # Service water demand is the same on every day of the week
                    )

                # Add deepcopy of user instance to ramp_user_dict
                ramp_users_dict[user_name] = copy.deepcopy(new_user)

            # Create RAMP use_case
            service_water_use_case = ramp.UseCase(
                name='service_water',
                users=list(ramp_users_dict.values())
            )

            service_water_use_cases_list.append((service_water_use_case, month))

        return service_water_use_cases_list


def minutes_wd(window):
    """
    Turns usage window given in hours into minutes (needed for RAMP)
    - if window is None -> returns None (no window specified)
    - else returns numpy array of window in minutes
    :param window:
    :return:
    """
    if window is None:
        return None
    else:
        return np.array(window) * 60
