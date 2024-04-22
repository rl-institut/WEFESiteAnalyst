from dash import Dash, Input, Output
from dash import html, dcc

import dash_bootstrap_components as dbc

home_layout = html.Div(children=[html.H1(children="This is our Home page")])

data_upload_layout = html.Div(
    children=[html.H1(children="This is our upload page")]
)

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Home", href="/")),
        dbc.NavItem(dbc.NavLink("Data upload", href="/data_upload")),
    ],
    brand="Multipage Dash App",
    color="dark",
    dark=True,
    className="mb-2",
)

app.layout = html.Div(
    [
        dcc.Location(id="url", refresh=False),
        navbar,
        dbc.Container(id="page-content", className="mb-4", fluid=True),
    ]
)


@app.callback(Output("page-content", "children"), Input("url", "pathname"))
def display_page(pathname):
    if pathname == "/":
        return home_layout
    elif pathname == "/data_upload":
        return data_upload_layout
    else:
        return dbc.Jumbotron(
            [
                html.H1("404: Not found", className="text-danger"),
            ]
        )


if __name__ == "__main__":
    app.run_server(debug=True)