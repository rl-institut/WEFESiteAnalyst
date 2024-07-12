import dash
from dash import html
import dash_bootstrap_components as dbc

dash.register_page(
    __name__,
    path='/survey-response-data',
    title='Survey Response Data',
    name='Survey Response Data',
    order=0
)

layout = dbc.Container([
    dbc.Row(html.H1('Survey response data')),
    dbc.Row(
        [
            dbc.Col([
                html.Div('Load survey response data from Kobo.')
            ], width=6),
            dbc.Col([
                html.Div('List of loaded survey response data. Click to analyse.')
            ], width=6),
        ]
    )
])