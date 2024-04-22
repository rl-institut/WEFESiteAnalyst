from dash import ALL, Input, Output, State, no_update, ctx, MATCH
import dash_bootstrap_components as dbc

import pandas as pd

pd.options.mode.chained_assignment = None  # default='warn'
from copy import deepcopy

import logging, sys

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

def set_table_actions_callbacks(app, display_tables_dict):
    # Dynamically create dict of callback outputs for all tables
    # Necessary because Dash pattern matching callback with "ALL"
    # (updating all tables on every callback) breaks active cell

    callback_output_dict = {}
    # Loop through each table to display
    i = 0
    for table_id, table in display_tables_dict.items():
        # Output to manipulate this tables table_row_wrapper's style (to change display property)
        callback_output_dict[f'style_table_row_{table_id}'] = Output({'type': 'table_row_wrapper', 'table_id': table_id},
                                                                     'style')

        # Output to manipulate this tables filter_query -> to allow callbacks to set filter_query on table cell click
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
                # Extract part of table query of this foreign key column -> exists only once -> get first list item
                query = [k for k in table_filter_query.split("&&") if col['id'] in k][0]
                # Find the index of the equal sign
                index = query.find('=')

                if index == -1:  # if no equal sign is found
                    new_row[col['id']] = ""  # no value is set in this column
                    # TODO: fk_column is currently not editable -> user would not be able to provide fk_id
                    # -> for now this is ok?
                else:
                    new_row[col['id']] = int(query[index + 1:])  # value is set to be the fk_id of the current query
            else:
                new_row[col['id']] = ""

        table_data.append(new_row)

        return table_data
