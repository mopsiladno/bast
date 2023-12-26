import dash
from dash import html

dash.register_page(__name__, path='/', title="БАСТ", name='Главная')

layout = html.Div([
    html.H1('Добро пожаловать в Банковскую Аналитическую СисТему регионального анализа - БАСТ', style={"font-family": "'Anonymous Pro'",'margin-top':'32px'}),
    html.Div('Данная система была выполнена в рамках курсовой работы студенткой 4 курса ИНБО-05-20 Батраковой Ангелиной.', style={"font-family": "'Anonymous Pro'"}),
])