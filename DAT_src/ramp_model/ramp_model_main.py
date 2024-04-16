"""
Temporary main file for the automatized demand assessment tool (DAT) developed in WP2 of the OptiMG project
"""

# Create RAMP input

"""
Based on each survey response, an instance of the RAMP user class for each relevant demand will be generated

In the OptiMG DAT we generate timeseries for the following demands:
1. Household electrical appliances [kWh_elec]
- one load profile of electrical energy demand caused by household devices
2. Business electrical appliances [kWh_elec]
3. Cooking energy demand [kWh_therm]
4. Agro-processing energy demand [kWh_mech]
5. Drinking water demand [l]
6. Service water demand [l]

"""

#%%
import pandas as pd
from ramp_model.ramp_control import RampControl
from input.cooking_demand import cooking_demand_dict
from input.household_elec_demand import households_dict
from input.agro_processing_demand import agro_processing_dict
from input.admin_input import admin_input
from input.drinking_water_demand import drinking_water_dict
from input.service_water_demand import service_water_dict

# Create instance of RampControl class, define timeframe to model load profiles
ramp_control = RampControl(365, '2018-01-01')

# Create RAMP use cases
service_water_use_cases_list = ramp_control.generate_service_water_use_cases(service_water_dict, admin_input)
agro_processing_use_cases_list = ramp_control.generate_agro_processing_use_cases(agro_processing_dict, admin_input)
elec_use_cases_list = ramp_control.generate_electric_appliances_use_cases(households_dict, admin_input)
cooking_use_cases_list = ramp_control.generate_cooking_demand_use_cases(cooking_demand_dict, admin_input)
drinking_water_use_cases_list = ramp_control.generate_drinking_water_use_cases(drinking_water_dict)

# Run load use_cases and create demand profiles
service_water_dp = ramp_control.run_use_cases(service_water_use_cases_list, service_water_dict, 'Service water')
drinking_water_dp = ramp_control.run_use_cases(drinking_water_use_cases_list, drinking_water_dict, 'Drinking water')
elec_lp = ramp_control.run_use_cases(elec_use_cases_list, households_dict, 'Household appliances')
cooking_dp = ramp_control.run_use_cases(cooking_use_cases_list, cooking_demand_dict, 'Cooking demand')
agro_processing_dp = ramp_control.run_use_cases(agro_processing_use_cases_list, agro_processing_dict, 'Agro-processing')

#%% Generate dataframe containing all demand profiles
all_demands_df = pd.DataFrame(index=service_water_dp.index)

all_demands_df['hh_elec'] = elec_lp.sum(axis='columns')
all_demands_df['business_elec'] = elec_lp.sum(axis='columns')*5
all_demands_df['agro_processing'] = agro_processing_dp.sum(axis='columns')
all_demands_df['cooking'] = agro_processing_dp.sum(axis='columns')
all_demands_df['drinking_water'] = drinking_water_dp.sum(axis='columns')
all_demands_df['service_water'] = service_water_dp.sum(axis='columns')

# Resample to hourly resolution
all_demand_df = all_demands_df.resample('h').mean()

# Get average day and week
all_demands_day = all_demands_df.groupby(
        all_demands_df.index.strftime('%H'), sort=False).mean()

all_demands_week = all_demands_df.groupby(
        all_demands_df.index.strftime('%a - %H'), sort=False).mean()

#%% Plot results
from helpers import plotting
from plotly.subplots import make_subplots

fig = make_subplots(2, 1, shared_xaxes=False)

fig = plotting.plotly_df(fig, df=all_demands_week, subplot_row=1)
fig = plotting.plotly_df(fig, df=all_demands_day, subplot_row=2)
fig.show()

#%%
fig = make_subplots(1, 1, shared_xaxes=True)
fig = plotting.plotly_high_res_df(fig, df=all_demand_df, subplot_row=1, prefix=' ')
#fig = plotting.plotly_high_res_df(fig, df=drinking_water_dp.resample('h').sum(), subplot_row=2, prefix='h_')
#fig = plotting.plotly_high_res_df(fig, df=service_water_dp, subplot_row=3, prefix=' ')
#fig = plotting.plotly_high_res_df(fig, df=service_water_dp.resample('h').sum(), subplot_row=4, prefix='h_')

fig.update_layout(height=900)

fig.show_dash(mode='external')
