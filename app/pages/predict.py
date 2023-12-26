import dash
from dash import html, dcc, callback, Input, Output
from prophet import Prophet
from prophet.plot import plot_plotly, plot_components_plotly
import plotly.express as px
import df_init
import plotly.graph_objs as go
import pandas as pd
import numpy as np

dash.register_page(__name__, name='Прогнозирование', title='Прогнозирование')


layout = html.Div([
    html.H1(children='Прогнозирование', style={'textAlign':'center',"font-family": "'Anonymous Pro'",'margin-top':'32px'}),
    html.P(children=["Регион: ", dcc.Dropdown(df_init.df.region.unique(), 'Altai region', id='dropdown-region-predict', style={"font-family": "'Anonymous Pro'",'width':'400px','display':'inline-block'})],
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
        'The average amount of a mortgage application', id='dropdown-parameter-predict',
        style={"font-family": "'Anonymous Pro'",'width':'500px','display':'inline-block'})],
        style={"font-family": "'Anonymous Pro'",'display':'inline-block'}),
    html.Br(),
    html.P(children=["Год, до которого предсказывать: ", dcc.Input(
        2025,
        min=2000, max=2099, step=1,
        id='input-year-predict',
        type='number',
        placeholder="input type {}".format('number'),
        size='40',
        style={"font-family": "'Anonymous Pro'", 'width':'200px', 'font-size':'14pt','padding' : '5px 10px'}
    )],style={"font-family": "'Anonymous Pro'",'display':'inline-block'}),
    dcc.Graph(id='main-graph-predict', config={'responsive':True}),
    html.Title("Series prediction")
])

@callback(
    Output('main-graph-predict', 'figure'),
    Input('dropdown-region-predict', 'value'),
    Input('dropdown-parameter-predict', 'value'),
    Input('input-year-predict', 'value')
)
def update_main_graph(value_region, value_parameter, value_year):
    dff = df_init.df[df_init.df.region==value_region]
    dff = dff.drop(dff[dff[value_parameter]==0].index)
    dff_p = dff[['date', value_parameter]].rename(columns={'date':'ds',value_parameter:'y'})
    
    period = 0
    if value_year > dff.year.max():
        period = (value_year - dff.year.max()) * 12 + 24

    m = Prophet(weekly_seasonality=True)

    m.fit(dff_p)
    future = m.make_future_dataframe(periods=period,  freq='MS')

    forecast = m.predict(future)

    w=15
    filt = np.ones(w)/w
    forecast['yhat'] = np.convolve(forecast['yhat'], filt, mode='same')

    w=np.hanning(5)
    forecast['yhat_lower']=np.convolve(w/w.sum(),forecast['yhat_lower'],mode='same') 
    forecast['yhat_upper']=np.convolve(w/w.sum(),forecast['yhat_upper'],mode='same') 

    forecast = forecast.iloc[:-24]

    fig = plot_plotly(m, forecast)

    # fig = px.line(dff, x='date', y=value_parameter, labels={'date':'Date', value_parameter:value_parameter})
    fig.update_traces(line_color='#95A5C9')
    fig.update_layout(
        plot_bgcolor='#FFFCFD',
        font_family='PT Sans Narrow',
        font_size=14,
        xaxis_title="Date",
        yaxis_title=value_parameter,
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