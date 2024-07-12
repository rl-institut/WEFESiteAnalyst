import dash
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc

app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([
    dbc.NavbarSimple(
        [
            dbc.NavItem(dbc.NavLink(
                html.Div(page["name"], className="ms-2"),
                href=page["path"]))
            for page in dash.page_registry.values()
        ],
        brand="DAT",
        color="dark",
        dark=True,
        className="mb-2",
    ),
    dash.page_container
])

if __name__ == '__main__':
    app.run(debug=True, port=8060)
