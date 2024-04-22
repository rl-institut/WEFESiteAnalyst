import dash_bootstrap_components as dbc
from dash import dash_table, html

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
                        dbc.Col(dbc.ButtonGroup(
                            [ # don't display close button for first table
                                dbc.Button("close", id={
                                    'type': 'close_table_button',
                                    "table_id": table_relational_df.table_id,
                                    "table_number": table_number
                                }, style={'margin': '1px'}) if table_number != 0 else None,
                                dbc.Button('add row', id={
                                    'type': 'add_row_button',
                                    "table_id": table_relational_df.table_id,
                                    'table_number': table_number
                                }, style={'margin': '1px'}),
                            ], vertical=True),
                            width=1)
                    ])

            ], id={'type': 'table_row_wrapper', 'table_id': table_relational_df.table_id}, style={'display': display}
        )

        # Append generated table to list of all tables to display
        tables_view.append(new_table_row)
        table_number += 1

    return tables_view