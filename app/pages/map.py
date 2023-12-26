import dash
from dash import html, dcc, callback, Input, Output
from prophet import Prophet
from prophet.plot import plot_plotly, plot_components_plotly
import plotly.express as px
import df_init
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import json
from urllib.request import urlopen

dash.register_page(__name__, name='Географическая визуализация', title='Географическая визуализация')

with urlopen('https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/russia.geojson') as response:
    counties = json.load(response)


layout = html.Div([
    html.H1(children='Географическая визуализация данных', style={'textAlign':'center',"font-family": "'Anonymous Pro'",'margin-top':'32px'}),
    html.P(children=["Параметр: ",  dcc.Dropdown(df_init.df[['Average Fast Food format Check', \
        'Average amount of new deposit', \
        'Average check in Restaurant format', \
        'Average consumer loan application', \
        'Average pension', \
        'Average salary', \
        'Average spending in a fast food restaurant', \
        'Average spending in a restaurant', \
        'Average spending on cards', \
        'Number of new deposits', \
        'On average rubles on current account per person', \
        'On average, deposits in rubles per person', \
        'The average amount of a mortgage application', \
        'The number of applications for consumer loans', \
        'The number of applications for mortgages']].columns, 
        'The average amount of a mortgage application', id='dropdown-parameter-map',
        style={"font-family": "'Anonymous Pro'",'width':'500px','display':'inline-block'})],
        style={"font-family": "'Anonymous Pro'",'display':'inline-block'}),
    html.Br(),
    html.P(children=["Год: ", dcc.Input(
        2015,
        min=2000, max=2099, step=1,
        id='input-year-map',
        type='number',
        placeholder="input type {}".format('number'),
        size='40',
        style={"font-family": "'Anonymous Pro'", 'width':'200px', 'font-size':'14pt','padding' : '5px 10px'}
    )],style={"font-family": "'Anonymous Pro'",'display':'inline-block'}),
    html.P(children=["Месяц: ",  dcc.Dropdown(['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь'], 
                'Январь', id='dropdown-month-map', style={"font-family": "'Anonymous Pro'",'width':'400px','display':'inline-block'})],
                style={"font-family": "'Anonymous Pro'"}),
    dcc.Graph(id='main-graph-map', config={'responsive':True}),
    html.Title("Map")
])

@callback(
    Output('main-graph-map', 'figure'),
    Input('dropdown-parameter-map', 'value'),
    Input('input-year-map', 'value'),
    Input('dropdown-month-map', 'value')
)
def update_main_graph(value_parameter, value_year, value_month):
    date = f'{value_year}-{df_init.match_month(value_month)}-15'
    df = df_init.df[df_init.df.date==date]

    df['region'] = df['region'].apply(lambda x: region_replace(x))
    
    fig = px.choropleth_mapbox(df, geojson=counties, locations='region', color=f"{value_parameter}",
                           color_continuous_scale="Viridis",
                           mapbox_style="carto-positron",
                           zoom=2, center = {"lat": 64.012766, "lon": 91.985136},
                           opacity=0.5,
                           labels={'unemp':'unemployment rate'},
                           featureidkey="properties.name_latin",
                           height=700
                          )
    
    fig.update_layout(
        plot_bgcolor='#FFFCFD',
        font_family='PT Sans Narrow',
        font_size=14,
    )
    return fig


def region_replace(x):
    match x:
        case 'The Republic of Sakha (Yakutia)':
            x = 'Sakha (Yakutia) Republic'
        case 'St. Petersburg':
            x = 'Saint Petersburg'
        case 'Altai region':
            x = 'Altai Krai'
        case 'Republic of Altai (Gorny Altai)':
            x = 'Altai Republic'
        case 'Khabarovsk region':
            x = 'Khabarovsk Krai'
        case 'Stavropol region':
            x = 'Stavropol Krai'
        case 'Krasnodar region':
            x = 'Krasnodar Krai'
        case 'Perm':
            x = 'Perm Krai'
        case 'Perm':
            x = 'Perm Krai'
        case 'Transbaikal region':
            x = 'Zabaykalsky Krai'
        case 'Krasnoyarsk region':
            x = 'Krasnoyarsk Krai'
        case 'Khanty-Mansi Autonomous District - Yugra':
            x = 'Khanty–Mansi Autonomous Okrug – Yugra'
        case 'Arhangelsk region':
            x = 'Arkhangelsk Oblast'
        case 'Yaroslavskaya oblast':
            x = 'Yaroslavl Oblast'
        case 'Udmurt republic':
            x = 'Udmurt Republic'
        case _:
            x = x.replace('region', 'Oblast')
            x = x.replace('The ', '')
            x = x.replace('Region', 'Oblast')
    return x