from relational_df import RelationalDf
import pandas as pd
from dash import Dash, dcc, html, Input, Output, dash_table, no_update

users = [
    {
        'id': 123,
        'name': 'low_income_hh',
        'num': 30,
    },
    {
        'id': 23,
        'name': 'medium_income_hh',
        'num': 5,
    }
]

appliances = [
    {
        'id': 1,
        'user_id': 123,
        'name': 'radio',
        'power': 5,
    },
    {
        'id': 2,
        'user_id': 23,
        'name': 'tv',
        'power': 40,
    }
]

usage_windows = [
    {
        'id': 1,
        'appliance_id': 1,
        'start': 14,
        'end': 16
    },
    {
        'id': 2,
        'appliance_id': 1,
        'start': 20,
        'end': 24
    }
]



users = RelationalDf('users', 'users', pd.DataFrame(users))
appliances = RelationalDf('appliances', 'appliances',  pd.DataFrame(appliances))
usage_windows = RelationalDf('usage_windows', 'usage_windows',  pd.DataFrame(usage_windows))
users.add_child_table(appliances, 'user_id')
appliances.add_child_table(usage_windows, 'appliance_id')

first_table = users
display_tables_dict = {users.table_id: users, appliances.table_id: appliances, usage_windows.table_id: usage_windows}