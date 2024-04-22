import dash
from dash import Dash, html, callback, Output, Input, dcc
import dash_bootstrap_components as dbc

dash.register_page(
    __name__,
    path='/data-analysis',
    title='Data Analysis',
    name='Data Analysis',
    order=1
)

layout = dbc.Container([
    dbc.Row(html.H1('Analyse demand data')),
    dbc.Row(
        [
            dbc.Col([
                html.Div('List of survey data loaded from Kobo. Click to open analysis editor.'),
                html.A('Open analysis editor', id='open-analysis-editor', href='http://127.0.0.1:8053/',
                       target='_blank'),
            ], width=6),
            dbc.Col([
                html.Div('List of already analyzed demand data. Click to open analysis editor.')
            ], width=6),
        ]
    ),
    dcc.Store(id='placeholder')
])


@callback(
    Output("placeholder", "data"),
    Input("open-analysis-editor", "n_clicks"),
    prevent_initial_call=True
)
def open_analysis_editor(n_clicks):
    """
    Open data analysis table editor in new tab as new dash app
    :param n_clicks:
    :return:
    """
    # Initialize app

    #TODO call function to start data_analysis_editor from this callback

    # Test -> starting other dash app works
    app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
    # Initialize layout of navbar and page_content container
    app.layout = dbc.Container(
        [
            dbc.ButtonGroup([dbc.Button("Save data")], id='task_bar'),
            dbc.Row(html.H2('test'))
        ]
    )

    app.run_server(debug=True, port=8053)

