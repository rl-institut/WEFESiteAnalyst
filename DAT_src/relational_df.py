from pandas import DataFrame
from dash import Dash, dcc, html, Input, Output, dash_table, no_update, callback


class RelationalDf:
    def __init__(self, table_id, table_name, df):

        self.df = df
        self.table_id = table_id
        self.table_name = table_name

        self.child_tables = {}  # dict of child_tables -> {child_table_name: child_table_df}
        self.parent_tables = {}  # dict of parent_tables -> {parent_table_name: (parent_table, foreign_key_column)

    def add_child_table(self, child_table, foreign_key_column):
        # Check if passed child_table is of class RelationalDF
        if not isinstance(child_table, RelationalDf):
            raise TypeError(f"child_table must be an instance of {RelationalDf.__name__}")

        # Check if child_table with the same name as passed child_table already exists in child_tables dict
        if child_table.table_id in self.child_tables:
            raise KeyError(f"'{child_table.table_id}' already exists as child table of '{self.table_id}'")

        # Add to dict of child_tables
        self.child_tables[child_table.table_id] = child_table

        # Add to child_table's list of parent_tables
        child_table.parent_tables[self.table_id] = (self, foreign_key_column)

    def add_parent_table(self, parent_table, foreign_key_column):
        # Check if passed parent_table is of class RelationalDF
        if not isinstance(parent_table, RelationalDf):
            raise TypeError(f"parent_table must be an instance of {RelationalDf.__name__}")

        # Check if parent_table with the same name as passed parent_table already exists in parent_tables list
        if parent_table.table_id in self.parent_tables:
            raise KeyError(f"'{parent_table.table_id}' already exists as child table of '{self.table_id}'")

        # Add table and foreign_key_column name to parent_tables dict
        self.parent_tables[parent_table.table_id] = (parent_table, foreign_key_column)

        # Add to parent_table's list of child_tables
        parent_table.child_tables[self.table_id] = self
