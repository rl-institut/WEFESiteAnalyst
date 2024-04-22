import dash
from dash import html
import dash_bootstrap_components as dbc

dash.register_page(
    __name__,
    path='/model-demand-profiles',
    title='Model Demand Profiles',
    name='Model Demand Profiles',
    order=1
)

layout = dbc.Container([
    dbc.Row(html.H1('Model demand profiles')),
    dbc.Row(
        [
            dbc.Col([
                html.Div('Model new demand profiles. Select analysed demand data and admin input.')
            ], width=6),
            dbc.Col([
                html.Div('List of modeled demand profiles. Click to display them.')
            ], width=6),
        ]
    )
])