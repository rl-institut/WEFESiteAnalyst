"""
Complete UI for data_analysis of DAT

"""

from dash import Dash, ALL, dcc, html, Input, Output, State, dash_table, no_update, ctx, Patch
import dash_bootstrap_components as dbc

import pandas as pd

pd.options.mode.chained_assignment = None  # default='warn'
from copy import deepcopy

import logging, sys

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

# Initialize app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

"""
Input:
- All data from preprocessing is saved in relational_dfs.
- The first "parent" table is the "users" table. All other tables are children of the parent table.
    o Electrical appliances
    o Cooking demands
    o Drinking water demands
    o Service water demands
    o ...
"""

""" DONE
1. Open view:
- dict of relational_dfs loaded from pickle
- all tables are iteratively loaded into view:
    o start with first table
    o all child_tables of first_table
    o all child_tables of child_tables...
    -> columns added for links to child tables
- first table visibility=True
"""

"""
2. Display child tables
- if link is clicked:
    o set child_table visibility=True
    o set filter for foreign_key column in child_table to corresponding ID of element in parent table
"""

"""
3. Edit tables
- preliminary: use dash's native edit function
- check if input is correct
    o set columns to allow numeric, string...
    o custom content checking function
- future:
    o
    o save each edit (allow for "undo", "redo)
"""

"""
4. Save tables
- on button click:
    o save all tables into pickle
    o creat filesystem for version control...
"""

from data_analysis.data_analysis_test import display_tables_dict  # dict containing all tables to be displayed

# Dynamically create dict of callback outputs for all tables
# Necessary because Dash pattern matching callback with "ALL" (updating all tables on every callback) breaks active cell
callback_output_dict = {}
# Loop through each table to display
for table_id, table in display_tables_dict.items():
    callback_output_dict[f'style_table_row_{table_id}'] = Output({'type': 'table_row_wrapper', 'table_id': table_id},
                                                                 'style')
    callback_output_dict[f'filter_query_table_{table_id}'] = Output({'type': 'table', 'table_id': table_id},
                                                                    'filter_query')

# Prepare output dict with identical keys and all values set to no_update to be used in callback
function_output_dict = {key: no_update for key in callback_output_dict.keys()}


@app.callback(
    # List of tables in view
    output=[Output({'type': 'table', 'table_id': ALL}, 'filter_query')],
    inputs=[
        # Active cell of the tables in view
        Input('test', "active_cell")
    ]
)
def update_tables(active_cell,
                  close_table_button_clicks,
                  add_row_button_clicks,
                  tables_data,
                  tables_columns,
                  tables_filter_queries,
                  table_rows_style
                  ):
    """
    Callback function to run when any button related to an individual table or a table cell is clicked.

    :param active_cell:
    :param close_table_button_clicks:
    :param add_row_button_clicks:
    :param displayed_tables_data:
    :param displayed_tables_columns:
    :param displayed_tables_list:
    :param current_tables_view:
    :return:
    """

    # Get id of table that was clicked: ID is dict with the following entries:
    # "type": "table", -> fix identifier for every table
    # "table_id": relational_df.table_id,  -> specific ID of this table
    # "table_number": table_number  -> number of the table in the list of displayed tables

    # Get ID of element that was clicked -> decide which action to perform
    element_clicked = ctx.triggered_id

    print(table_rows_style)

    if element_clicked['type'] == 'table':  # If table was clicked
        # Run table cell clicked actions
        logging.debug('Table cell clicked')
        # Abort if there is no active cell or no table clicked
        if active_cell[0] is None:
            return no_update

        return table_cell_clicked(active_cell, table_rows_style, tables_filter_queries)

    elif element_clicked['type'] == 'close_table_button':
        # Run close table button clicked actions
        logging.debug('Close table button clicked')
        #return (close_table_button_clicked(close_table_button_clicks, displayed_tables_list, current_tables_view)
        #        + (displayed_tables_data,))
    elif element_clicked['type'] == 'add_row_button':
        logging.debug('Add row button clicked')
        #return add_table_row(add_row_button_clicks, displayed_tables_data, displayed_tables_columns,
        #                     displayed_tables_list, current_tables_view)


def table_cell_clicked(active_cell, table_rows_style, table_filter_queries):
    table_clicked = ctx.triggered_id
    print(f'table {table_clicked} clicked at {active_cell}')

    # Check if the clicked column is child column and contains sub-data
    if active_cell[table_clicked['table_number']]['column_id'].startswith('!child_'):

        # Make deepcopy of prepared function_output_dict
        output_dict = deepcopy(function_output_dict)

        # Get child_table_id from the clicked column
        child_table_id = active_cell[table_clicked['table_number']]['column_id'][7:]
        # Get the position of the clicked child table in view (= position in input dict)
        child_table_pos = list(display_tables_dict).index(child_table_id)

        table_rows_style = [no_update] * len(table_rows_style)

        # Update visibility this table in output_dict
        output_dict[f'style_table_row_{table_clicked["table_id"]}'] = {'display': 'block'}

        # Get the corresponding query_col of the child table
        query_col = display_tables_dict[table_clicked['table_id']].child_tables[child_table_id].parent_tables[
            table_clicked['table_id']][1]
        # Get corresponding query_id
        query_id = active_cell[table_clicked['table_number']]['row_id']

        output_dict[f'filter_query_table_{table_clicked["table_id"]}'] = f'{{{query_col}}} ={query_id}'

        # Return dict of displayed tables and updated view (HTML) if currently displayed tables and None for active cell
        return output_dict
    else:
        return no_update


def load_tables(tables_dict):
    """
    Generate initial view containing all tables to display.
    - only first table is visible, others are hidden in the beginning

    :return: list containing all rows of tables to display
    """

    tables_view = []
    table_number = 0  # counter for positions of table
    # Loop through all tables to display
    for table_id, table_relational_df in tables_dict.items():

        # Create copy of the dataframe
        df = table_relational_df.df.copy()

        # Get this relational_df's foreign key columns -> to not display them
        foreign_key_columns = []
        for parent_table in table_relational_df.parent_tables.values():
            foreign_key_columns.append(parent_table[1])

        # Get this tables original columns
        original_columns = []
        for c in df.columns:
            if c == 'id':  # If column is ID column...
                original_columns.append(
                    {"name": c, "id": c, "editable": False}  # ...it is NOT editable
                )
            elif c in foreign_key_columns:  # If column is foreign_key column
                original_columns.append(
                    {"name": c, "id": c, "editable": False}  # ...it is NOT editable
                )
            else:  # Every regular column...
                original_columns.append(
                    {"name": c, "id": c, "editable": True}  # ...is editable
                )

        # Create new "button" column for this table -> to link to child tables
        child_table_columns = []

        # Create button column for every child table of this dataframe
        for child_table_id, child_table_relational_df in table_relational_df.child_tables.items():
            child_table_columns.append(
                {'name': child_table_relational_df.table_name,  # Column name is child_table name
                 'id': "!child_" + str(child_table_id),
                 'editable': False  # "Button column" is not editable
                 }
            )  # Column ID is identifier + child_table id
            # Add "button text" to display in the button column
            if len(df.index) > 0:  # only if the table to display is not empty
                df.loc[:, "!child_" + str(child_table_id)] = 'Click me!'

        # Add original and custom created child_table columns
        columns = original_columns + child_table_columns

        # Generate dash datatable object
        table = dash_table.DataTable(
            id={"type": "table", "table_id": table_relational_df.table_id, "table_number": table_number},
            columns=columns,
            data=df.to_dict("records"),
            page_size=10,
            sort_action="native",
            active_cell=None,
            editable=True,
            filter_action="native",
            sort_mode='multi',
            row_selectable='multi',
            row_deletable=True,
            selected_rows=[],
            page_action='native',
            page_current=0,
        ),

        # Create new row to add to app HTML layout

        # Generate header for new table
        header = table_relational_df.table_name

        # Make only first table visible on load
        display = 'block' if table_number == 0 else 'none'

        new_table_row = html.Div(
            [
                dbc.Row(dbc.Col(html.H2(header))),
                dbc.Row(
                    [
                        dbc.Col(table, width=11),
                        dbc.Col(
                            [
                                dbc.Button('X', id={
                                    'type': 'close_table_button',
                                    "table_id": table_relational_df.table_id,
                                    "table_number": table_number
                                }) if table_number != 0 else None,  # don't display close button for first table
                                dbc.Button('Add row', id={
                                    'type': 'add_row_button',
                                    "table_id": table_relational_df.table_id,
                                    'table_number': table_number
                                }),
                            ],
                            width=1)
                    ])

            ], id={'type': 'table_row_wrapper', 'table_id': table_relational_df.table_id}, style={'display': display}
        )

        # Append generated table to list of all tables to display
        tables_view.append(new_table_row)
        table_number =+ 1

    return tables_view


# Initialize layout (with users table)
app.layout = html.Div(
    [
        # Add first displayed table to app_wrapper
        html.Div(dbc.Button('Add row', id='test'), id='app_wrapper')
    ]
)

if __name__ == '__main__':
    app.run_server(debug=False, port=8052)
    logging.debug('App running')
