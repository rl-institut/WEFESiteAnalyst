import dash
from dash import Dash, html, callback, Output, Input, dcc
import dash_bootstrap_components as dbc
from datatable_editor.core import DatatableEditor

from datatable_editor.demo_data import display_tables_dict

editor_port = 8053

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
                html.A('Open analysis editor', id='open-analysis-editor', href=f'http://127.0.0.1:{editor_port}/',
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
    # Initialize datatable editor
    editor = DatatableEditor(datatables=display_tables_dict, port=editor_port, debug=True)

    # Run editor
    editor.run_app()


