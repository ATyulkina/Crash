from dash import dcc, html
import pandas as pd
import dash_bootstrap_components as dbc

df = pd.read_csv('data/Crash.csv')
df = df.dropna(subset=['Регион', 'Широта', 'Долгота'])

def create_layout():
    
    return dbc.Container([
        
        html.Div([
            html.H1("Информационно-аналитическая система для исследования причин автомобильных аварий и ДТП в России", className='header',), 
        ], className='header'),
          
        dbc.Row([
            dbc.Col([dcc.Checklist(id='fatal-filter', options=[{'label': '  Показать ДТП только с погибшими', 'value': 'fatal',}], className='checklist')], width=1, md=1, xs=12, ),

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

            dbc.Col(dbc.Card(id='total_accidents-output', body=True, className='filters-row-1'), width=2, md=2, xs=12),
            dbc.Col(dbc.Card(id='total_fatalities-output', body=True,className='filters-row-3'), width=2),
            dbc.Col(dbc.Card(id='total_injured-output', body=True, className='filters-row-2'), width=2),

        ], className='row'),


        dbc.Row([
            dbc.Col([html.H4("ДТП на карте России"), dcc.Graph(id='map-graph', config={'displayModeBar': False}, style={'border-radius': '15px', 'overflow': 'hidden'}, )], width=8, md=8, xs=12, className='map-container'),
            dbc.Col([html.H4("Топ-5 регионов"), dcc.Graph(id='regions-graph', config={'displayModeBar': False}, style={'border-radius': '15px', 'overflow': 'hidden'}, )], width=4, md=4, xs=12, className='map-container'),
        ], className='row'),

dbc.Row([
    # Первая колонка - временные графики
    dbc.Col([
        dbc.Tabs([
            dbc.Tab([
                dcc.Graph(
                    id='monthly-graph', 
                    config={'displayModeBar': False},
                    style={'border-radius': '15px', 'overflow': 'hidden'}
                )
            ], label="Месячный график", tab_id="tab-monthly", label_style={"color": "#e5383b"}),
            
            dbc.Tab([
                dcc.Graph(
                    id='hourly-graph', 
                    config={'displayModeBar': False},
                    style={'border-radius': '15px', 'overflow': 'hidden'}
                )
            ], label="Часовой график", tab_id="tab-hourly", label_style={"color": "#e5383b"}),
            
            dbc.Tab([
                dcc.Graph(
                    id='weekday-graph', 
                    config={'displayModeBar': False},
                    style={'border-radius': '15px', 'overflow': 'hidden'}
                )
            ], label="По дням недели", tab_id="tab-weekday", label_style={"color": "#e5383b"}),
        ], 
        id="tabs-charts",
        active_tab="tab-monthly",
        className="four.columns"
        )
    ], 
    width=4,
    md=4, 
    xs=12, 
    className='four.columns'
    ),
    
    # Вторая колонка - факторы ДТП
    dbc.Col([
        dbc.Tabs([
            dbc.Tab([
                dcc.Graph(
                    id='lighting-graph', 
                    config={'displayModeBar': False},
                    style={'border-radius': '15px', 'overflow': 'hidden'}
                )
            ], label="Освещение", tab_id="tab-lighting", label_style={"color": "#e5383b"}),
            
            dbc.Tab([
                dcc.Graph(
                    id='weather-graph', 
                    config={'displayModeBar': False},
                    style={'border-radius': '15px', 'overflow': 'hidden'}
                )
            ], label="Погода", tab_id="tab-weather", label_style={"color": "#e5383b"}),
            
            dbc.Tab([
                dcc.Graph(
                    id='road-condition-graph', 
                    config={'displayModeBar': False},
                    style={'border-radius': '15px', 'overflow': 'hidden'}
                )
            ], label="Состояние дороги", tab_id="tab-road-condition", label_style={"color": "#e5383b"}),
        ], 
        id="tabs-accidents",
        active_tab="tab-lighting",
        className="four.columns"
        )
    ], 
    width=4,
    md=4,
    xs=12,
    className='chart-container'
    ),
    
    # Третья колонка - ML модель
    dbc.Col([
        dbc.Tabs([
            dbc.Tab([
                dcc.Graph(
                    id='risk-prediction-graph', 
                    config={'displayModeBar': False},
                    style={'border-radius': '15px', 'overflow': 'hidden'}
                )
            ], label="Факторы риска", tab_id="tab-risk", label_style={"color": "#e5383b"}),
        ], 
        id="tabs-ml",
        active_tab="tab-risk",
        className="four.columns"
        )
    ], 
    width=4,
    md=4,
    xs=12,
    className='four.columns'
    ),
    
], className='row')
         
        
        
    ], fluid=True, className='container')
