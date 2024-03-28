from pandas import DataFrame
from dash import Dash, dcc, html, Input, Output, dash_table, no_update, callback


class RelationalDf:
    def __init__(self, table_name, unique_key_column, df):

        self.df = df
        self.table_name = table_name
        self.unique_key_column = unique_key_column

        self.child_tables = {}  # dict of child_tables -> {child_table_name: child_table_df}
        self.parent_tables = {}  # dict of parent_tables -> {parent_table_name: (parent_table, foreign_key_column)

    def add_child_table(self, child_table, foreign_key_column):
        # Check if passed child_table is of class RelationalDF
        if not isinstance(child_table, RelationalDf):
            raise TypeError(f"child_table must be an instance of {RelationalDf.__name__}")

        # Check if child_table with the same name as passed child_table already exists in child_tables dict
        if child_table.table_name in self.child_tables:
            raise KeyError(f"'{child_table.table_name}' already exists as child table of '{self.table_name}'")

        # Add to dict of child_tables
        self.child_tables[child_table.table_name] = child_table

        # Add to child_table's list of parent_tables
        child_table.parent_tables[self.table_name] = (self, foreign_key_column)

    def add_parent_table(self, parent_table, foreign_key_column):
        # Check if passed parent_table is of class RelationalDF
        if not isinstance(parent_table, RelationalDf):
            raise TypeError(f"parent_table must be an instance of {RelationalDf.__name__}")

        # Check if parent_table with the same name as passed parent_table already exists in parent_tables list
        if parent_table.table_name in self.parent_tables:
            raise KeyError(f"'{parent_table.table_name}' already exists as child table of '{self.table_name}'")

        # Add table and foreign_key_column name to parent_tables dict
        self.parent_tables[parent_table.table_name] = (parent_table, foreign_key_column)

        # Add to parent_table's list of child_tables
        parent_table.child_tables[self.table_name] = self

    def display_table(self, page_size):

        # Create dash app
        external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
        app = Dash(__name__, external_stylesheets=external_stylesheets)

        initial_active_cell = {"row": 0, "column": 0, "column_id": "country", "row_id": 0}

        # Get list of child tables
        child_tables_names = list(self.child_tables.keys())

        # Add columns for child_tables to df to display
        for child_table in child_tables_names:
            self.df[child_table] = "click me"

        # Fill app
        app.layout = html.Div(
            [
                html.Div(
                    [
                        html.H3(self.table_name, style={"textAlign": "center"}),
                        dash_table.DataTable(
                            id=self.table_name,
                            columns=[{"name": c, "id": c} for c in self.df.columns],
                            data=self.df.to_dict("records"),
                            page_size=page_size,
                            sort_action="native",
                            active_cell=initial_active_cell,
                        ),
                    ],
                    style={"margin": 50},
                    className="row"
                )
            ],
            className="row")

        app.run_server(debug=False, port=8052)
        print('done')

    @callback(
        Output("details", "children"),
        Input(self.table_name, "active_cell"),
    )
    def cell_clicked(active_cell):
        if active_cell is None:
            return no_update

        print(active_cell)
        row_id = active_cell["row_id"]
        print(f"row id: {row_id}")

        col_id = active_cell["column_id"]
        print(f"column id: {col_id}")
        print("---------------------")


        # Check if active cell has sub-data (=entry exists in sub-data dict)
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
                style={"margin":50}
            )
            return sub_data_table
        else:
            print('no')
            return no_update