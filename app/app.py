from dash import Dash, html, dcc, callback, Output, Input, page_container, page_registry
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import flask
import df_init
import time
import os
import json

debug = True

try:
    debug = False if os.environ["DASH_DEBUG_MODE"] == "False" else True
except:
    debug = True

server = flask.Flask(__name__, template_folder='static')

external_stylesheets = [
    "https://fonts.googleapis.com/css2?family=Anonymous+Pro&display=swap",
    dbc.themes.BOOTSTRAP
]

@server.route('/1/3/3/7/refresh', methods=['POST'])
def refresh():
    # haha so funny
    df_init.df = pd.read_csv('SberData.csv')
    df_init.df = df_init.df.pivot_table(index = ["region", "date"], columns = "name", values = "value", aggfunc = "mean", fill_value = 0).reset_index()
    df_init.df = df_init.df[df_init.df["region"] != "Russia"]
    df_init.df['month'] = df_init.df["date"].apply(lambda t: time.strptime(t, '%Y-%m-%d').tm_mon)
    df_init.df['year'] = df_init.df["date"].apply(lambda t: time.strptime(t, '%Y-%m-%d').tm_year)
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 

app = Dash(name=__name__, server=server, title="БАСТ", use_pages=True, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    dbc.Navbar(
        dbc.Container(
            [
                html.A(
                    # Use row and col to control vertical alignment of logo / brand
                    dbc.Row(
                        [
                            dbc.Col(html.Img(src='assets/paw.png', style={'width': '32pt', 'height': '32pt','margin-right':'16pt'})),
                            dbc.Col(dbc.NavbarBrand("БАСТ", className="ms-2"), style={"font-family": "'Anonymous Pro'", 'font-size':'20pt'}),
                        ],
                        align="center",
                        className="g-0",
                    ),
                    href="/",
                    style={"textDecoration": "none"},
                ),
                dbc.Row(
                    [
                        dbc.Col([
                            dbc.Nav([
                                dbc.NavItem(dbc.NavLink(f"{page['name']}", href=page["relative_path"]),style={"font-family": "'Anonymous Pro'"}, ) for page in page_registry.values()
                            ])
                        ]) 
                    ], className="g-0", align="left"
                )
            ]
        ),
        style={'margin-left':'-32px', 'margin-right':'-32px'}
    ),
    # html.Img(src='assets/paw.png',style={'display':'inline-block', 'width': '32pt', 'height': '32pt','margin-right':'16pt'}),
    # html.H1('БАСТ', style={"font-family": "'Anonymous Pro'", 'display':'inline-block'}),
    # html.Div([
    #     html.Div(
    #         dcc.Link(f"{page['name']}", href=page["relative_path"])
    #     ) for page in page_registry.values()
    # ], style={"font-family": "'Anonymous Pro'"}),
    page_container
])

if __name__ == '__main__':
    df_init.df = pd.read_csv('SberData.csv')
    df_init.df = df_init.df.pivot_table(index = ["region", "date"], columns = "name", values = "value", aggfunc = "mean", fill_value = 0).reset_index()
    df_init.df = df_init.df[df_init.df["region"] != "Russia"]
    df_init.df['month'] = df_init.df["date"].apply(lambda t: time.strptime(t, '%Y-%m-%d').tm_mon)
    df_init.df['year'] = df_init.df["date"].apply(lambda t: time.strptime(t, '%Y-%m-%d').tm_year)

    app.run_server(host="0.0.0.0", port="8050", debug=debug)    