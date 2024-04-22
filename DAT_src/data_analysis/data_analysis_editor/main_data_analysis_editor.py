# Import packages
from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc

# Import own modules
from load_tables import load_tables  # Function to load all tables in the view.
from table_actions import set_table_actions_callbacks  # Func to set all table actions and set callbacks

# Initialize app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Load data to display -> dict of all tables (relational_dfs) to display
# TEMPORARY -> testing data, in DAT this will be read from pickle file
from data_analysis.data_analysis_test import display_tables_dict

# Set table actions callbacks
set_table_actions_callbacks(app, display_tables_dict)


# Initialize layout of navbar and page_content container
app.layout = dbc.Container(
    [
        dbc.ButtonGroup([dbc.Button("Save data")], id='task_bar'),
        dbc.Row(load_tables(display_tables_dict), id='tables_wrapper')
    ]
)

if __name__ == '__main__':
    app.run_server(debug=True, port=8052)

