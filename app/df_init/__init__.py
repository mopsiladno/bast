import pandas as pd
import time

pd.options.plotting.backend = "plotly"


df = pd.read_csv('SberData.csv')
df = df.pivot_table(index = ["region", "date"], columns = "name", values = "value", aggfunc = "mean", fill_value = 0).reset_index()
df = df[df["region"] != "Russia"]
df['month'] = df["date"].apply(lambda t: time.strptime(t, '%Y-%m-%d').tm_mon)
df['year'] = df["date"].apply(lambda t: time.strptime(t, '%Y-%m-%d').tm_year)

def match_month(month_str):
    match month_str:
        case 'Январь':
            return '01'
        case 'Февраль':
            return '02'
        case 'Март':
            return '03'
        case 'Апрель':
            return '04'
        case 'Май':
            return '05'
        case 'Июнь':
            return '06'
        case 'Июль':
            return '07'
        case 'Август':
            return '08'
        case 'Сентябрь':
            return '09'
        case 'Октябрь':
            return '10'
        case 'Ноябрь':
            return '11'
        case 'Декабрь':
            return '12'
        case _:
            return '13'