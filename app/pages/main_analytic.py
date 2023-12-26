import dash
from dash import html, dcc, callback, Input, Output
import plotly.express as px
import df_init
import plotly.graph_objs as go
import pandas as pd

dash.register_page(__name__, name='Аналитика', title='Аналитика')


layout = html.Div([
    html.H1(children='Аналитика', style={'textAlign':'center',"font-family": "'Anonymous Pro'",'margin-top':'32px'}),
    html.P(children=["Регион: ", dcc.Dropdown(df_init.df.region.unique(), 'Altai region', id='dropdown-region', style={"font-family": "'Anonymous Pro'",'width':'400px','display':'inline-block'})],
                style={"font-family": "'Anonymous Pro'", 'display':'inline-block', 'padding-bottom':'8pt'}),
    html.Br(),
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
        'The average amount of a mortgage application', id='dropdown-parameter',
        style={"font-family": "'Anonymous Pro'",'width':'500px','display':'inline-block'})],
        style={"font-family": "'Anonymous Pro'",'display':'inline-block'}),
    dcc.Graph(id='main-graph'),
     html.P(children=["Год: ", dcc.Input(
        2016,
        min=2000, max=2099, step=1,
        id='input-year',
        type='number',
        placeholder="input type {}".format('number'),
        size='40',
        style={"font-family": "'Anonymous Pro'", 'width':'200px', 'font-size':'14pt','padding' : '5px 10px'}
    )],style={"font-family": "'Anonymous Pro'",'display':'inline-block'}),
    dcc.Graph(id='bar'),
    html.Title("Overall visualization")
])

@callback(
    Output('main-graph', 'figure'),
    Input('dropdown-region', 'value'),
    Input('dropdown-parameter', 'value')
)
def update_main_graph(value_region, value_parameter):
    dff = df_init.df[df_init.df.region==value_region]
    dff = dff.drop(dff[dff[value_parameter]==0].index)

    fig = px.line(dff, x='date', y=value_parameter, labels={'date':'Date', value_parameter:value_parameter})
    fig.update_traces(line_color='#95A5C9')
    fig.update_layout(
        plot_bgcolor='#FFFCFD',
        font_family='PT Sans Narrow',
        font_size=14
    )
    fig.update_xaxes(
        mirror=True,
        ticks='outside',
        tickcolor='#FFDFF2',
        gridcolor='#FFDFF2'
    )
    fig.update_yaxes(
        mirror=True,
        ticks='outside',
        tickcolor='#FFDFF2',
        gridcolor='#FFDFF2'
    )

    return fig

@callback(
    Output('bar', 'figure'),
    Input('dropdown-region', 'value'),
    Input('dropdown-parameter', 'value'),
    Input('input-year', 'value')
)
def update_bar(value_region, value_parameter, value_year):
    dff = df_init.df[df_init.df.region==value_region]
    dff = dff[dff.year==value_year]
    dff = dff.drop(dff[dff[value_parameter]==0].index)

    fig = go.FigureWidget()
    fig.add_bar(x=dff['date'], y=dff[value_parameter], xperiodalignment='end', xperiod='M1', marker=dict(color = dff[value_parameter], colorscale='Burg'))
    fig.update_xaxes(tickformat = '%b', dtick='M1')
    fig.update_layout(
        plot_bgcolor='#FFFCFD',
        font_family='PT Sans Narrow',
        font_size=14,
        height=500, width=700
    )
    fig.update_xaxes(
        mirror=True,
        ticks='outside',
        tickcolor='#FFDFF2',
        gridcolor='#FFDFF2'
    )
    fig.update_yaxes(
        mirror=True,
        ticks='outside',
        tickcolor='#FFDFF2',
        gridcolor='#FFDFF2'
    )
    
    # fig = px.bar(dff, x='month', y=value_parameter, labels={'month':'Month', value_parameter:value_parameter})

    return fig