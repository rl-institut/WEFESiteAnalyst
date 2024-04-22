from ramp_model.ramp_control import RampControl

from helpers import plotting
from plotly.subplots import make_subplots
from input.complete_input import input_dict
from input.admin_input import admin_input

# Create instance of RampControl class, define timeframe to model load profiles
ramp_control = RampControl(365, '2018-01-01')

dat_output = ramp_control.run_opti_mg_dat(input_dict, admin_input)
# %% Plot raw output
fig = make_subplots(rows=5, cols=1, shared_xaxes=True)

i = 1  # Plotly subplot rows start at index 1
for demand, df in dat_output.groupby(level=0, axis=1):
    fig = plotting.plotly_high_res_df(fig, df=df, subplot_row=i)
    i = i + 1
    print(demand)

fig.update_layout(autosize=True)

fig.show_dash(mode='external')

#%% Plot aggregated demands

agg_demand = dat_output.groupby(level=0, axis=1).sum()
agg_demand.head()

fig = make_subplots(rows=1, cols=1, shared_xaxes=True)
fig = plotting.plotly_high_res_df(fig, df=agg_demand, subplot_row=1)
fig.show_dash(mode='external')
