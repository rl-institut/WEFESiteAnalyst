import ramp
import pandas as pd
import numpy as np
import copy
from time import perf_counter


class RampControl:
    """
    - !!
    """

    def __init__(self, number_of_days, start_date):
        self.number_of_days = number_of_days
        self.min_timeseries = pd.date_range(start_date, periods=number_of_days * 24 * 60, freq="Min")
        self.days_timeseries = pd.date_range(start_date, periods=number_of_days, freq="D")

    def run_use_cases(self, use_cases_list, user_data):
        """

        :param use_cases_list:
        :param user_data:
        :return:
        """

        for entry in use_cases_list:
            use_case = entry[0]  # use_case object is first entry in tuple in use_cases_list
            use_case_month = entry[1]  # second entry is month number
            # Dict to store generated demand profiles
            demand_profiles = {}

            # Calculate peak time range of this use case
            peak_time_range = use_case.calc_peak_time_range()

            # Loop through all days of this month's use_case
            day_counter = 0
            for day in self.days_timeseries[self.days_timeseries.month == use_case_month]:
                # Return weekday of this day (Monday=0, Sunday=6)
                weekday = day.weekday()
                # Loop through all user instances (= user types)
                for user in use_case.users:
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
                print(day_counter)

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
        return pd.concat(demand_profiles, axis=1)

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
            # Loop through every household survey respondent.
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
                        func_cycle=func_time,
                        # Duration of this cooking demand is also func_cycle
                        time_fraction_random_variability=cooking_metadate['cooking_time_variability'],

                        fixed_cycle=1,  # every cooking demand has one duty cycle
                        # cw11=cooking_window,  # time window of cooking demand

                        p_11=cooking_power,  # first part of duty cycle: power = cooking_power,
                        t_11=func_time,
                        # first part of duty cycle: duration = cooking_time
                        p_12=0,
                        # second part of duty cycle is unused -> assume constant cooking power -> power and time = 0
                        t_12=0,  # steady state duration = total duration - start-up time
                        r_c1=0.2,
                        # =cooking_metadate['cooking_time_variability'],  # random variability of cooking duration
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