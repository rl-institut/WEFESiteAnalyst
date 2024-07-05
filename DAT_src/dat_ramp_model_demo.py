from ramp_model.ramp_control import RampControl

from helpers import plotting
from plotly.subplots import make_subplots
#from input.complete_input import input_dict
from input.admin_input import admin_input
from preprocessing.process_survey import process_survey
import dash
from dash import dcc
from dash import html


# Create instance of RampControl class, define timeframe to model load profiles
ramp_control = RampControl(365, '2018-01-01')

#dat_output = ramp_control.run_opti_mg_dat(input_dict, admin_input)
input_dic = process_survey(surv_id="affG8Fq5Suc99Sg9UB5hPv", token="ea290627972a055fd067e1efc02c803869b1747c",DUMP=True)

dat_output = ramp_control.run_opti_mg_dat(input_dic, admin_input)
# %% Plot raw output


i = 1  # Plotly subplot rows start at index 1
figures = []
for demand, df in dat_output.groupby(level=0, axis=1):
    fig = make_subplots(rows=1, cols=1, shared_xaxes=True)
    fig = plotting.plotly_high_res_df(fig, df=df, subplot_row=1)
    i = i + 1
    print(demand)
    figures.append(
        html.Div([
            html.H3(demand),
            dcc.Graph(figure=fig),
        ])
    )

fig.update_layout(autosize=True)

# fig.show_dash(mode='external')

#%% Plot aggregated demands

agg_demand = dat_output.groupby(level=0, axis=1).sum()
agg_demand.head()

fig = make_subplots(rows=1, cols=1, shared_xaxes=True)
fig = plotting.plotly_high_res_df(fig, df=agg_demand, subplot_row=1)
#fig.show_dash(mode='external')
figures.append(
        html.Div([
            html.H3("aggregated demands"),
            dcc.Graph(figure=fig),
        ])
    )

if __name__=="__main__":
    demo_app = dash.Dash(__name__)
    demo_app.layout = html.Div(children=figures)
    demo_app.run_server(debug=False)
