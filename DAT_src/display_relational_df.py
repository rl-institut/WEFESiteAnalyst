# %%
from dash import Dash, ALL, dcc, html, Input, Output, dash_table, no_update, ctx
import dash_bootstrap_components as dbc

from data_analysis_test import display_tables
from data_analysis_test import first_table

# Initialize app
app = Dash(__name__)

# Update data store when new table is opened
@app.callback(
    [
        Output("displayed_tables", "data"),
        Output('tables_container', 'children')
    ],
    [
        Input({'type': 'table', 'table_id': ALL}, "active_cell"),
        Input('displayed_tables', 'data'),
        Input('tables_container', 'children')
    ]

)
def table_cell_clicked_update_store(active_cell, displayed_tables, current_tables):
    # Get ID of table that was clicked
    table_clicked = ctx.triggered_id

    if active_cell[0] is None:
        return no_update

    # Check if the clicked column is child column and contains sub-data
    if active_cell[0]['column_id'].startswith('!child_'):
        # Get child_table_id
        child_table_id = active_cell[0]['column_id'][7:]

        # Check if this table is already displayed
        if child_table_id not in displayed_tables:
            print(displayed_tables)
            print(child_table_id)
            new_table = display_tables[table_clicked['table_id']].child_tables[child_table_id].df.head()
            # Get new df to display
            new_table_row = display_table(display_tables[table_clicked['table_id']].child_tables[child_table_id])
            current_tables.append(new_table_row)

            # Add new table to list of displayed tables
            displayed_tables.append(child_table_id)

    return displayed_tables, current_tables

def display_table(relational_df):
    # -- Generate table from this relational_df
    # Get this tables original columns
    original_columns = [{"name": c, "id": c} for c in relational_df.df.columns]

    # Create custom child columns for dash table
    child_table_columns = []
    child_table_column_names = []
    for child_table_id, child_table_relational_df in relational_df.child_tables.items():
        child_table_columns.append({'name': child_table_relational_df.table_name,  # Column name is child_table name
                                    'id': "!child_"+str(child_table_id)})  # Column ID is identifier + child_table id
        # Add columns for child_tables of df to display
        relational_df.df["!child_"+str(child_table_id)] = 'Click me!'
        # Collect names of added columns in list (to drop later)
        child_table_column_names.append("!child_"+str(child_table_id))

    # Add original and custom created child_table columns
    columns = original_columns + child_table_columns

    # Generate dash datatable object
    table = dash_table.DataTable(
        id={"type": "table", "table_id": relational_df.table_id},
        columns=columns,
        data=relational_df.df.to_dict("records"),
        page_size=10,
        sort_action="native",
        active_cell=None,
    ),

    # Drop previously added "buttom columns" from original dataframe
    relational_df.df = relational_df.df.drop(child_table_column_names, axis=1)

    # Create new row to add to app HTML layout
    new_table_row = dbc.Row(dbc.Col(table))

    return new_table_row


"""@app.callback(
    Output("tables_container", "children"),
    Input({'type': 'table', 'index': ALL}, "active_cell", ),
)
def table_cell_clicked(active_cell):
    if active_cell is None:
        return no_update

    print(active_cell)
    row_id = active_cell["row_id"]
    print(f"row id: {row_id}")

    col_id = active_cell["column_id"]
    print(f"column id: {col_id}")
    print("---------------------")


    # Check if active columns has sub-data (child_table)

    if (row_id, col_id) in sub_data_dict:
        print('yeees')
        # Get the sub data
        sub_data = sub_data_dict[(row_id, col_id)]
        # Create table of appliances
        sub_data_table = html.Div(
            [dash_table.DataTable(
                id="sub_data_table",
                columns=[{"name": c, "id": c} for c in sub_data.columns],
                data=sub_data.to_dict("records"),
                page_size=10,
                sort_action="native",
                editable=True
            )],
            style={"margin": 50}
        )
        return sub_data_table
    else:
        print('no')
        return no_update"""

# Initialize layout (with users table)
app.layout = html.Div([
    dcc.Store(id='displayed_tables', data=[first_table.table_id]),
    html.Div([display_table(first_table)],
             id='tables_container')
    ])

if __name__ == '__main__':
    app.run_server(debug=True, port=8052)
    print('done')
