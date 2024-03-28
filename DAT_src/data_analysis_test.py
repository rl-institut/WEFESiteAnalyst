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

users = RelationalDf('users', 'id', pd.DataFrame(users))
appliances = RelationalDf('appliances', 'id', pd.DataFrame(appliances))

users.add_child_table(appliances, 'user_id')

users.display_table(10)
