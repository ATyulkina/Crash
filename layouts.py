from dash import dcc, html
import pandas as pd
import dash_bootstrap_components as dbc

df = pd.read_csv('data/Crash.csv')
df = df.dropna(subset=['Регион', 'Широта', 'Долгота'])

def create_layout():
    
    return dbc.Container([
        
        html.Div([
            html.H1("Анализ автомобильных аварий и ДТП в России", className='header-title'),
            html.P("Панель мониторинга состояния дорог и оценки рисков аварий", className='header-description')
        ], className='header'),
          
        dbc.Row([
            dbc.Col([dcc.Checklist(id='fatal-filter', options=[{'label': 'Показать ДТП только с погибшими', 'value': 'fatal'}])], width=1, md=1, xs=12, ),

            dbc.Col([
                dcc.Dropdown(
                    id='region-filter',
                    options=[{'label': 'Все регионы', 'value': 'all'}] + [{'label': reg, 'value': reg} for reg in df['Регион'].unique()],
                    value='all',
                    multi=False
                )
            ], width=2, md=2, xs=12,),
            
            dbc.Col([
                dcc.Dropdown(
                    id='month-filter',
                    options=[{'label': 'Все месяцы', 'value': 0}] + 
                            [{'label': month, 'value': i} for i, month in enumerate([
                                'Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь'
                            ], 1)],
                    value=0,
                    multi=False
                )
            ], width=1, md=1, xs=12, ),
            
            dbc.Col([
                dcc.Dropdown(
                    id='accident-type-filter',
                    options=[{'label': 'Все виды ДТП', 'value': 'all'}] + 
                            [{'label': tp, 'value': tp} for tp in df['Вид ДТП'].unique()],
                    value='all',
                    multi=False
                )
            ], width=2, md=2, xs=12, ),

            dbc.Col(dbc.Card(id='total_accidents-output', body=True,), width=2, md=2, xs=12),
            dbc.Col(dbc.Card(id='total_fatalities-output', body=True,), width=2),
            dbc.Col(dbc.Card(id='total_injured-output', body=True,), width=2),

        ], className='row filters-row'),


        dbc.Row([
            dbc.Col(dcc.Graph(id='map-graph', config={'displayModeBar': False}), width=8, md=8, xs=12, className='map-container'),
            dbc.Col([html.H4("Топ-5 регионов"), dcc.Graph(id='regions-graph', config={'displayModeBar': False}, style={'height': '350px'})], width=4, md=4, xs=12, className='four columns chart-container'),
        ], className='row'),

        dbc.Row([
            dbc.Col(dcc.Graph(id='monthly-graph', config={'displayModeBar': False}), width=4, md=4, xs=12, className='four columns chart-container'),
            dbc.Col(dcc.Graph(id='hourly-graph', config={'displayModeBar': False}), width=4, md=4, xs=12, className='four columns chart-container'),
            dbc.Col(dcc.Graph(id='weekday-graph', config={'displayModeBar': False}), width=4, md=4, xs=12, className='four columns chart-container'),
        ], className='row'),
       
        dbc.Row([
            dbc.Col([
                html.H4("ДТП по освещению"),
                dcc.Graph(id='lighting-graph', config={'displayModeBar': False})
            ], className='four columns chart-container', style={'height': '500px'}),
        
            dbc.Col([
                html.H4("ДТП по погодным условиям"),
                dcc.Graph(id='weather-graph', config={'displayModeBar': False})
            ], className='four columns chart-container', style={'height': '500px'}),
            
            dbc.Col([
                html.H4("ДТП по состоянию дороги"),
                dcc.Graph(id='road-condition-graph', config={'displayModeBar': False})
            ], className='four columns chart-container', style={'height': '500px'})
        ], className='row'),       
         
        dbc.Row([
            html.H3("Оценка факторов риска ДТП на основе ML модели"),
            dcc.Graph(id='risk-prediction-graph', config={'displayModeBar': False})
        ], className='ml-container'),
        
    ], fluid=True, className='container')
