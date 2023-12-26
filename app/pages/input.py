import dash
from dash import html, dcc, callback, Input, Output, State
import plotly.express as px
import df_init
import plotly.graph_objs as go
import pandas as pd

dash.register_page(__name__, name='Ввод данных', title='Ввод данных')


layout = html.Div([
    html.H1(children='Ввод данных', style={'textAlign':'center',"font-family": "'Anonymous Pro'", 'margin-top':'32px'}),
    html.Div(children=[
        html.H3("Вы успешно добавили данные", hidden=True, id="page_header", style={"font-family": "'Anonymous Pro'"}),
        # login form
        html.Div(children=[
            html.P(children=["Регион: ", dcc.Dropdown(df_init.df.region.unique(), 'Altai region', id='dropdown-region-in', style={"font-family": "'Anonymous Pro'",'width':'400px','display':'inline-block'})],
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
                'The average amount of a mortgage application', id='dropdown-parameter-in',
                style={"font-family": "'Anonymous Pro'",'width':'500px','display':'inline-block'})],
                style={"font-family": "'Anonymous Pro'",'display':'inline-block'}),
            html.Br(),
            html.P(children=["Год: ", dcc.Input(
                    2020,
                    min=2000, max=2024, step=1,
                    id='input-year-in',
                    type='number',
                    placeholder="input type {}".format('number'),
                    size='40',
                    style={"font-family": "'Anonymous Pro'", 'width':'200px', 'font-size':'14pt','padding' : '5px 10px'}
                )],style={"font-family": "'Anonymous Pro'",'display':'inline-block'}),
            html.Br(),
            html.P(children=["Месяц: ",  dcc.Dropdown(['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь'], 
                'Январь', id='dropdown-month-in', style={"font-family": "'Anonymous Pro'",'width':'400px','display':'inline-block'})],
                style={"font-family": "'Anonymous Pro'", 'display':'inline-block', 'padding-bottom':'8pt'}),
            html.Br(),
            html.P(children=["Значение: ", dcc.Input(
                    step=1,
                    id='input-value-in',
                    type='number',
                    placeholder="input type {}".format('number'),
                    size='40',
                    style={"font-family": "'Anonymous Pro'", 'width':'200px', 'font-size':'14pt','padding' : '5px 10px'}
                )],style={"font-family": "'Anonymous Pro'",'display':'inline-block'}),
            html.Br(),
            html.Button(children=['Загрузить'], id='submit',  n_clicks=0, className='button-28', style={"width":"200px"})
        ], style={'margin' : '0 auto'}, id="login_form", hidden=False)
    ], style={'display' : 'block', 'text-align' : 'center', 'padding' : 2}),



    html.H1(children='Удаление данных', style={'textAlign':'center',"font-family": "'Anonymous Pro'"}),
    html.Div(children=[
        html.H3("Вы успешно удалили данные", hidden=True, id="page_header", style={"font-family": "'Anonymous Pro'"}),
        # login form
        html.Div(children=[
            html.P(children=["Регион: ", dcc.Dropdown(df_init.df.region.unique(), 'Altai region', id='dropdown-region-del', style={"font-family": "'Anonymous Pro'",'width':'400px','display':'inline-block'})],
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
                'The average amount of a mortgage application', id='dropdown-parameter-del',
                style={"font-family": "'Anonymous Pro'",'width':'500px','display':'inline-block'})],
                style={"font-family": "'Anonymous Pro'",'display':'inline-block'}),
            html.Br(),
            html.P(children=["Год: ", dcc.Input(
                    2020,
                    min=2000, max=2024, step=1,
                    id='input-year-del',
                    type='number',
                    placeholder="input type {}".format('number'),
                    size='40',
                    style={"font-family": "'Anonymous Pro'", 'width':'200px', 'font-size':'14pt','padding' : '5px 10px'}
                )],style={"font-family": "'Anonymous Pro'",'display':'inline-block'}),
            html.Br(),
            html.P(children=["Месяц: ",  dcc.Dropdown(['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь'], 
                'Январь', id='dropdown-month-del', style={"font-family": "'Anonymous Pro'",'width':'400px','display':'inline-block'})],
                style={"font-family": "'Anonymous Pro'", 'display':'inline-block', 'padding-bottom':'8pt'}),
            html.Br(),
            html.Button(children=['Удалить'], id='submit-del',  n_clicks=0, className='button-28', style={"width":"200px"})
        ], style={'margin' : '0 auto'}, id="login_form", hidden=False)
    ], style={'display' : 'block', 'text-align' : 'center', 'padding' : 2}),
    html.Title("Data input")
])

@callback(
    Output('page_header', 'children', allow_duplicate=True),
    State('dropdown-region-in', 'value'),
    State('dropdown-parameter-in', 'value'),
    State('input-year-in', 'value'),
    State('dropdown-month-in', 'value'),
    State('input-value-in', 'value'),
    Input('submit','n_clicks'),
    prevent_initial_call=True
)
def update_bar(value_region, value_parameter, value_year, value_month, value_value, n_clicks):
    date = f'{value_year}-{df_init.match_month(value_month)}-15'
    print(df_init.df.loc[(df_init.df['date'] == date) & (df_init.df['region'] == value_region)].empty)
    print(df_init.df.loc[(df_init.df['date'] == date) & (df_init.df['region'] == value_region)])
    if value_value != "" or value_value != 0:
        if df_init.df.loc[(df_init.df['date'] == date) & (df_init.df['region'] == value_region)].empty:
            new_row = {c : 0 for c in df_init.df.columns}
            new_row['region'] = value_region
            new_row['date'] = date
            new_row[value_parameter] = value_value
            df_init.df = pd.concat([df_init.df, pd.DataFrame([new_row])], ignore_index=True)
        else:
            df_init.df.loc[(df_init.df['date'] == date) & (df_init.df['region'] == value_region), value_parameter] = value_value
    return 

@callback(
    Output('page_header', 'children'),
    State('dropdown-region-del', 'value'),
    State('dropdown-parameter-del', 'value'),
    State('input-year-del', 'value'),
    State('dropdown-month-del', 'value'),
    Input('submit-del','n_clicks'),
    prevent_initial_call=True
)
def update_bar(value_region, value_parameter, value_year, value_month, n_clicks):
    date = f'{value_year}-{df_init.match_month(value_month)}-15'
    print(df_init.df.loc[(df_init.df['date'] == date) & (df_init.df['region'] == value_region)].empty)
    print(df_init.df.loc[(df_init.df['date'] == date) & (df_init.df['region'] == value_region)])
    if not df_init.df.loc[(df_init.df['date'] == date) & (df_init.df['region'] == value_region)].empty:
        df_init.df.loc[(df_init.df['date'] == date) & (df_init.df['region'] == value_region), value_parameter] = 0
    return 