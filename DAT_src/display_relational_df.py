# %%
from dash import Dash, ALL, dcc, html, Input, Output, dash_table, no_update, ctx, MATCH
import dash_bootstrap_components as dbc

# Initialize app
app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

@app.callback(
    [
        Output("displayed_tables", "data", allow_duplicate=True),
        Output('app_wrapper', 'children', allow_duplicate=True)
    ],
    [
        Input({'type': 'table', 'table_id': ALL, 'table_number': ALL}, "active_cell"),
        Input({'type': 'close_table_button', 'table_id': ALL, 'table_number': ALL}, 'n_clicks'),
        Input('displayed_tables', 'data'),
        Input('app_wrapper', 'children')
    ],
    prevent_initial_call=True

)
def update_tables(active_cell, close_table_button_clicks,displayed_tables_list, current_tables_view):
    """
    Callback function to run when a cell of a table is clicked

    :param active_cell:
    :param close_button_table_button_clicks:
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

    if element_clicked['type'] == 'table':
        # Run table cell clicked actions
        print('table cell clicked')
        return table_cell_clicked(active_cell, displayed_tables_list, current_tables_view)

    elif element_clicked['type'] == 'close_table_button':
        # Run close table button clicked actions
        print('close table button clicked')
        return close_table_button_clicked(close_table_button_clicks, displayed_tables_list, current_tables_view)


def table_cell_clicked(active_cell, displayed_tables_list, current_tables_view):
    table_clicked = ctx.triggered_id

    # Abort if there is no active cell or no table clicked
    if not active_cell:
        return no_update

    print(active_cell)
    # Check if the clicked column is child column and contains sub-data
    if active_cell[table_clicked['table_number']]['column_id'].startswith('!child_'):
        # Get child_table_id from the clicked column
        child_table_id = active_cell[table_clicked['table_number']]['column_id'][7:]

        # Check if this table is already displayed
        if child_table_id not in displayed_tables_list:
            print('Add new table')

            # Generate new table to display
            new_table = display_table(
                relational_df=display_tables_dict[table_clicked['table_id']].child_tables[child_table_id],
                table_number=len(current_tables_view),  # position of new table is at the end of current tables view
                query_col=display_tables_dict[table_clicked['table_id']].
                child_tables[child_table_id].parent_tables[table_clicked['table_id']][1],
                query_id=active_cell[table_clicked['table_number']]['row_id']
            )

            # Add new table to App view
            current_tables_view.append(new_table)

            # Add id of new table to list of displayed tables
            displayed_tables_list.append(child_table_id)
        else:
            print('Table is already displayed')
            # Update displayed table with new query

    # return list of displayed tables and updated view (HTML) if currently displayed tables and None for active cell
    return displayed_tables_list, current_tables_view

def close_table_button_clicked(n, displayed_tables_list, current_tables_view):
    print('Button clicked:')
    print(ctx.triggered_id)

    button_clicked = ctx.triggered_id
    # Remove this close button's corresponding table from displayed_tables_list
    displayed_tables_list = displayed_tables_list[0:button_clicked['table_number']]

    # Remove this close button's corresponding table and a
    current_tables_view = current_tables_view[0:button_clicked['table_number']]

    return displayed_tables_list, current_tables_view


def display_table(relational_df, table_number, query_col=None, query_id=None):
    """
    Generates and returns new "row" containing Dash data table to add to the layout

    :param relational_df: containing data to display in this table
    :param table_number: position, at which this table will be displayed
    :param query_col: foreign_key column to query the dataframe for, default=None
    :param query_id: ID to query parent table for (ID of the entry in the clicked row)
    :return:
    """

    # Check if query data is provided
    if query_col and query_id:
        # If specified, query table for foreign key
        df = relational_df.df.query(str(query_col) + ' == ' + str(query_id))
    else:
        # Otherwise create copy of the dataframe to display
        df = relational_df.df.copy()

    # Get this relational_df's foreign key columns -> to not display them
    foreign_key_columns = []
    for parent_table in relational_df.parent_tables.values():
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

    # Create custom child columns for dash table
    child_table_columns = []
    child_table_column_names = []
    for child_table_id, child_table_relational_df in relational_df.child_tables.items():
        child_table_columns.append(
            {'name': child_table_relational_df.table_name,  # Column name is child_table name
             'id': "!child_"+str(child_table_id),
             'editable': False  # "Button column" is not editable
             }
        )  # Column ID is identifier + child_table id
        # Add columns for child_tables of df to display
        df["!child_"+str(child_table_id)] = 'Click me!'
        # Collect names of added columns in list (to drop later)
        child_table_column_names.append("!child_"+str(child_table_id))

    # Add original and custom created child_table columns
    columns = original_columns + child_table_columns

    # Generate dash datatable object
    table = dash_table.DataTable(
        id={"type": "table", "table_id": relational_df.table_id, "table_number": table_number},
        columns=columns,
        data=df.to_dict("records"),
        page_size=10,
        sort_action="native",
        active_cell=None,
        editable=True
    ),

    # Create new row to add to app HTML layout

    # Generate header for new table
    if query_col:  # If table is queried, add query column name in header
        header = query_col + ': ' + str(query_id) + ' - ' + relational_df.table_name
    else:
        header = relational_df.table_name

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
                                "table_id": relational_df.table_id,
                                "table_number": table_number
                            })
                        ],
                        width=1)
                ])

        ], id=relational_df.table_id, className='table_row_wrapper'
    )

    return new_table_row


from data_analysis_test import display_tables_dict  # dict containing all tables to be displayed
from data_analysis_test import first_table  # first table to be displayed

# Initialize layout (with users table)
app.layout = html.Div(
    [
        # Save ID of first displayed table for position 1
        dcc.Store(id='displayed_tables', data=[first_table.table_id]),
        # Add first displayed table to app_wrapper
        html.Div([display_table(first_table, 0)], id='app_wrapper')
    ]
)

if __name__ == '__main__':
    app.run_server(debug=True, port=8052)
    print('done')
