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
from DAT_src.ramp_control import RampControl
from DAT_src.cooking_demand import cooking_demand_dict
from DAT_src.household_elec_demand import households_dict
from DAT_src.admin_input import admin_input

# Create instance of RampControl class, define timeframe to model load profiles
ramp_control = RampControl(365, '2018-01-01')

# Create RAMP use cases

"""
The modeling of the 6 timeseries is performed separately in independent RAMP use cases
- Analog to my (Johann's) masters thesis, we generate one RAMP use case for every day. 
- RAMPs function of looping through all the days defined for a multi-day UseCase is not used.
- This gives more flexibility in modeling weekly variation and seasonality:
    o By default, RAMP can only model if an appliance is or is not used during a weekday, or weekend day
    -> this approach gives the flexibility to specify if an appliance has a different usage time or usage windows on 
    certain weekdays
    o The change of use of an appliance due to seasonal variation (most relevant for agro-processing and irrigation 
    water)
"""

elec_use_cases_list = ramp_control.generate_electric_appliances_use_cases(households_dict, admin_input)
cooking_use_cases_list = ramp_control.generate_cooking_demand_use_cases(cooking_demand_dict, admin_input)


# Run load use_cases and create demand profiles
elec_lp = ramp_control.run_use_cases(elec_use_cases_list, households_dict, 'Household appliances')
cooking_dp = ramp_control.run_use_cases(cooking_use_cases_list, cooking_demand_dict, 'Cooking demand')


#%% Plot results
from DAT_src import plotting
from plotly.subplots import make_subplots

fig = make_subplots(2,1, shared_xaxes=True)

fig = plotting.plotly_high_res_df(fig, df=elec_lp, subplot_row=1)
fig = plotting.plotly_high_res_df(fig, df=cooking_dp, subplot_row=2)
fig.update_layout(height=600)

fig.show_dash(mode='external')
