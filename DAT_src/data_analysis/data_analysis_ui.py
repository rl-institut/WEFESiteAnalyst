"""
Complete UI for data_analysis of DAT

"""

from dash import Dash, ALL, dcc, html, Input, Output, State, dash_table, no_update, ctx, MATCH
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

""" DONE
2. Display child tables
- if link is clicked:
    o set child_table visibility=True
    o set filter for foreign_key column in child_table to corresponding ID of element in parent table
"""

"""
3. Edit tables
- add row
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
i = 0
for table_id, table in display_tables_dict.items():
    callback_output_dict[f'style_table_row_{table_id}'] = Output({'type': 'table_row_wrapper', 'table_id': table_id},
                                                                 'style')
    callback_output_dict[f'filter_query_table_{table_id}'] = Output({'type': 'table', 'table_id': table_id,
                                                                    'table_number': i}, 'filter_query')
    i += 1

# Prepare output dict with identical keys and all values set to no_update to be used in callback
function_output_dict = {key: no_update for key in callback_output_dict.keys()}

@app.callback(
    # List of tables in view
    output=callback_output_dict,
    inputs=[
        # Active cell of the tables in view
        Input({'type': 'table', 'table_id': ALL, 'table_number': ALL}, "active_cell"),
        # Clicked "close_table" button
        Input({'type': 'close_table_button', 'table_id': ALL, 'table_number': ALL}, 'n_clicks'),
    ],
    prevent_initial_call=True
)
def update_tables(active_cell, close_table_button_clicks):
    """
    Callback function to display new table with new query or closing table

    :param active_cell:
    :param close_table_button_clicks:
    :return: dict of callback outputs for styles and filter queries of all tables
    """

    # Get id of table that was clicked: ID is dict with the following entries:
    # "type": "table", -> fix identifier for every table
    # "table_id": relational_df.table_id,  -> specific ID of this table
    # "table_number": table_number  -> number of the table in the list of displayed tables

    # Get ID of element that was clicked -> decide which action to perform
    element_clicked = ctx.triggered_id

    if element_clicked['type'] == 'table':  # If table was clicked
        # Run table cell clicked actions
        logging.debug('Table cell clicked')
        # Abort if there is no active cell or no table clicked
        if active_cell[0] is None:
            return no_update

        return table_cell_clicked(active_cell)

    elif element_clicked['type'] == 'close_table_button':
        # Run close table button clicked actions
        logging.debug('Close table button clicked')
        return close_table()

    elif element_clicked['type'] == 'add_row_button':
        logging.debug('Add row button clicked')
        #return add_table_row(add_row_button_clicks, displayed_tables_data, displayed_tables_columns,
        #                     displayed_tables_list, current_tables_view)


def table_cell_clicked(active_cell):
    """
    Function to run when table cell is clicked
    - checks if clicked cell links to child table
    - changes display property of the corresponding child table
    - changes filter_query property of the corresponding child table
    :param active_cell:
    :return: dict of callback outputs for styles and filter queries of all tables
    """
    table_clicked = ctx.triggered_id
    print(f'table clicked: {table_clicked["table_number"]}')

    # Check if the clicked column is child column and contains sub-data
    if active_cell[table_clicked['table_number']]['column_id'].startswith('!child_'):

        # Make deepcopy of prepared function_output_dict
        output_dict = deepcopy(function_output_dict)

        # Get child_table_id from the clicked column
        child_table_id = active_cell[table_clicked['table_number']]['column_id'][7:]

        # Update display property of child table in output_dict -> make visible
        output_dict[f'style_table_row_{child_table_id}'] = {'display': 'block'}

        # Get the corresponding query_col of the child table
        query_col = display_tables_dict[table_clicked['table_id']].child_tables[child_table_id].parent_tables[
            table_clicked['table_id']][1]
        # Get corresponding query_i
        query_id = active_cell[table_clicked['table_number']]['row_id']


        # Update query property of child table in output_dict -> query for corresponding item
        output_dict[f'filter_query_table_{child_table_id}'] = f'{{!fk_{query_col}}}={query_id}'

        #print(f' Callback returns: {output_dict}')
        # Return dict of displayed tables and updated view (HTML) if currently displayed tables and None for active cell
        return output_dict
    else:
        return no_update


def close_table():
    """
    Closes table by updating the display property in the dict of callback outputs
    :return: dict of callback outputs for styles and filter queries of all tables
    """
    close_button_clicked = ctx.triggered_id
    print(f'table clicked: {close_button_clicked["table_number"]}')

    output_dict = deepcopy(function_output_dict)
    # Update visibility this table in output_dict
    output_dict[f'style_table_row_{close_button_clicked["table_id"]}'] = {'display': 'none'}

    return output_dict

@app.callback(
    Output({'type': 'table', 'table_id': MATCH, 'table_number': MATCH}, 'data'),
    Input({'type': 'add_row_button', 'table_id': MATCH, 'table_number': MATCH}, 'n_clicks'),
    State({'type': 'table', 'table_id': MATCH, 'table_number': MATCH}, 'data'),
    State({'type': 'table', 'table_id': MATCH, 'table_number': MATCH}, 'columns'),
    State({'type': 'table', 'table_id': MATCH, 'table_number': MATCH}, 'filter_query'),
    prevent_initial_call=True
)
def add_table_row(clicks, table_data, table_columns, table_filter_query):
    logging.debug('Add table row button clicked:')

    # Turn table data into dataframe
    table_df = pd.DataFrame(table_data)

    # Construct new row entry
    new_row = {}
    for col in table_columns:
        if col['id'].startswith('!child_'):  # if column is button column
            new_row[col['id']] = 'Click me! (added)'
        elif col['id'] == 'id':  # if column is ID column
            # Generate ID of new element to add -> must be unique! -> current max id +1
            new_row[col['id']] = table_df['id'].max() + 1
        elif col['id'].startswith('!fk_'):  # if column is query column
            # Extract part of table query of this column -> exists only once get first list item
            query = [k for k in table_filter_query.split("&&") if col['id'] in k][0]
            # Find the index of the equal sign
            index = query.find('=')

            if index == -1:  # if no equal sign is found
                new_row[col['id']] = ""  # no value is set in this column
                # TODO: fk_column is currently not editable -> user would not be able to provide fk_id
            else:
                new_row[col['id']] = int(query[index + 1:])  # value is set to be the fk_id of the current query
        else:
            new_row[col['id']] = ""

    table_data.append(new_row)

    return table_data

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

        # TODO give ability to define column display names -> to be displayed to user and not equal to actual df columns

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
                    {"name": c, "id": "!fk_"+c, "editable": False}  # ...it is NOT editable and has prefix in id
                )
            else:  # Every regular column...
                original_columns.append(
                    {"name": c, "id": c, "editable": True}  # ...is editable
                )

        # Add !fk prefix to df foreign key columns to oad data correctly
        df = df.rename(columns={c: '!fk_' + c for c in df.columns if c in foreign_key_columns})

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
                                dbc.Row(dbc.Button("close", id={
                                    'type': 'close_table_button',
                                    "table_id": table_relational_df.table_id,
                                    "table_number": table_number
                                }) if table_number != 0 else None), # don't display close button for first table
                                dbc.Row(dbc.Button('add row', id={
                                    'type': 'add_row_button',
                                    "table_id": table_relational_df.table_id,
                                    'table_number': table_number
                                }))
                            ],
                            width=1)
                    ])

            ], id={'type': 'table_row_wrapper', 'table_id': table_relational_df.table_id}, style={'display': display}
        )

        # Append generated table to list of all tables to display
        tables_view.append(new_table_row)
        table_number += 1

    return tables_view


# Save each tables information about foreign_key columns
tables_foreign_key_columns = {}
for table_id, table_relational_df in display_tables_dict.items():
    tables_foreign_key_columns[table_id] = {}
    # Get this tables foreign key columns and save in dict:
    # {'foreign_key_column': 'current_query_id' (None at the beginning, to be updated on queries)}
    for parent_table_name, parent_table in table_relational_df.parent_tables.items():
        tables_foreign_key_columns[table_id][parent_table[1]] = None

# Initialize layout (with users table)
app.layout = html.Div(
    [
# Data store to save information about this tables foreign key columns to easily access in callbacks
        dcc.Store(id='tables_foreign_key_columns_store', data=tables_foreign_key_columns),
        # Add first displayed table to app_wrapper
        html.Div(load_tables(display_tables_dict), id='app_wrapper')
    ]
)

if __name__ == '__main__':
    app.run_server(debug=False, port=8052)
    logging.debug('App running')
