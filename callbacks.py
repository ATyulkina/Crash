from dash import Input, Output, html
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

df = pd.read_csv('data/Crash.csv')
df = df.dropna(subset=['Регион', 'Широта', 'Долгота'])

def register_callbacks(app):    
    @app.callback(
        [Output('map-graph', 'figure'),
         Output('monthly-graph', 'figure'),
         Output('hourly-graph', 'figure'),
         Output('lighting-graph', 'figure'),
         Output('weather-graph', 'figure'),
         Output('road-condition-graph', 'figure'),
         Output('weekday-graph', 'figure'),
         Output('risk-prediction-graph', 'figure'),
         Output('regions-graph', 'figure'),
         Output('total_accidents-output', 'children'),
         Output('total_fatalities-output', 'children'),
         Output('total_injured-output', 'children'),],
        [Input('region-filter', 'value'),
         Input('month-filter', 'value'),
         Input('accident-type-filter', 'value'),
         Input('fatal-filter', 'value'),]
    )
    def update_dashboard(region, month, accident_type, fatal_filter):
        
        filtered_df = df.copy()
        
        if region != 'all':
            filtered_df = filtered_df[filtered_df['Регион'] == region]
        
        if month != 0:
            filtered_df = filtered_df[filtered_df['Месяц'] == month]
        
        if accident_type != 'all':
            filtered_df = filtered_df[filtered_df['Вид ДТП'] == accident_type]
        
        if fatal_filter and 'fatal' in fatal_filter:
            filtered_df = filtered_df[filtered_df['Число погибших'] > 0]


        # Карта ДТП
        map_fig = create_map(filtered_df)

        regions_fig = create_top_regions_chart(filtered_df)
        
        # Распределение по месяцам
        monthly_fig = create_monthly_chart(filtered_df)

        # Распределение по дням недели
        weekday_fig = create_weekday_chart(filtered_df)
        
        # Распределение по часам
        hourly_fig = create_hourly_chart(filtered_df)
        
        # Освещение
        lighting_fig = create_lighting_chart(filtered_df)
        
        # Погода
        weather_fig = create_weather_chart(filtered_df)
        
        # Состояние дороги
        road_fig = create_road_condition_chart(filtered_df)
        
        # Модель
        risk_fig = create_risk_prediction_chart(filtered_df)

        total_accidents = html.Div([
            html.H5('Общее количество ДТП'),
            # html.Br(),
            html.H4(f'{len(filtered_df)}')
        ])

        total_fatalities = html.Div([
            html.H5('Погибшие'),
            # html.Br(),
            html.H4(f'{filtered_df['Число погибших'].sum()}')
        ])

        total_injured = html.Div([
            html.H5('Раненые'),
            # html.Br(),
            html.H4(f'{filtered_df['Число раненых'].sum()}')
        ])
        
        return (map_fig, monthly_fig, hourly_fig, lighting_fig, weather_fig, 
                road_fig, weekday_fig, risk_fig, regions_fig, total_accidents, total_fatalities, total_injured)

    def create_map(df_filtered):

        try:
            region_stats = df_filtered.groupby('Регион').agg({
                'Широта': 'mean',
                'Долгота': 'mean',
                'Число погибших': 'sum',
                'Число раненых': 'sum',
                'Число участников': 'sum'
            }).reset_index()
            
            fig = px.scatter_mapbox(
                region_stats,
                lat='Широта',
                lon='Долгота',
                size='Число участников',
                color='Число погибших',
                hover_name='Регион',
                hover_data={
                    'Число погибших': True,
                    'Число раненых': True,
                    'Число участников': True
                },
                color_continuous_scale='reds',
                size_max=30,
                zoom=3,
                center={'lat': 55.7558, 'lon': 37.6173}
            )
            
            fig.update_layout(
                mapbox_style="open-street-map",
                
            )
            
            return fig
        except:
            return go.Figure()


    def create_top_regions_chart(df_filtered):
        top_regions = df_filtered['Регион'].value_counts().head(5).reset_index(name='Количество ДТП')

        fig = px.bar(
            top_regions,
            x='Количество ДТП',
            y='Регион',
            orientation='h',
            title='',
            color='Количество ДТП',
            color_continuous_scale='reds'
        )
        fig.update_layout(coloraxis_showscale=False)
        fig.update_layout(
            xaxis_title='Количество ДТП',
            yaxis_title='')
        
        return fig
    
    def create_monthly_chart(df_filtered):
        monthly_data = df_filtered.groupby('Месяц').size().reset_index(name='Количество ДТП')
        
        month_names = {1: 'Янв', 2: 'Фев', 3: 'Мар', 4: 'Апр', 5: 'Май', 6: 'Июн', 7: 'Июл', 8: 'Авг',  9: 'Сен', 10: 'Окт', 11: 'Ноя', 12: 'Дек'}

        fig = px.bar(
            monthly_data,
            x='Месяц',
            y='Количество ДТП',
            title='',
            color='Количество ДТП',
            color_continuous_scale='reds'
        )
        fig.update_yaxes(tickformat='d', separatethousands=True)
        fig.update_layout(coloraxis_showscale=False, xaxis=dict(dtick=1))
        fig.update_xaxes(tickmode='array', tickvals=list(range(1, 13)), ticktext=list(month_names.values())
    )
        
        return fig

    def create_hourly_chart(df_filtered):
        hourly_data = df_filtered.groupby('Час').size().reset_index(name='Количество ДТП')
        
        fig = px.bar(
            hourly_data,
            x='Час',
            y='Количество ДТП',
            title='',
            color='Количество ДТП',
            color_continuous_scale='reds'
        )
        fig.update_yaxes(tickformat='d', separatethousands=True)
        fig.update_layout(coloraxis_showscale=False, xaxis=dict(dtick=1))
        return fig

    def create_lighting_chart(df_filtered):
        lighting_data = df_filtered['Освещение'].value_counts().head(4).reset_index()
        
        def wrap_text(text, max_length=10):
            words = text.split()
            lines = []
            current_line = ""
            for word in words:
                if len(current_line) + len(word) + 1 <= max_length:
                    current_line += (" " if current_line else "") + word
                else:
                    lines.append(current_line)
                    current_line = word
            if current_line:
                lines.append(current_line)
            return "<br>".join(lines)

        lighting_data['Освещение_wrapped'] = lighting_data['Освещение'].apply(wrap_text)

        fig = px.bar(
            lighting_data,
            y='Освещение_wrapped',
            x='count',
            orientation='h',
            title='',
            color='count',
            color_continuous_scale='reds'
        )

        fig.update_yaxes(tickfont=dict(size=10))
        fig.update_xaxes(tickformat='d', separatethousands=True)
        fig.update_layout(coloraxis_showscale=False)
        fig.update_layout(
            xaxis_title='Количество ДТП',
            yaxis_title='')
        
        return fig

    def create_weather_chart(df_filtered):
        weather_data = df_filtered['Состояние погоды'].value_counts().head(4).reset_index()
        
        fig = px.bar(
            weather_data,
            y='Состояние погоды',
            x='count',
            orientation='h',
            title='',
            color='count',
            color_continuous_scale='reds'
        )
        fig.update_xaxes(tickformat='d', separatethousands=True)
        fig.update_layout(coloraxis_showscale=False)
        fig.update_layout(
            xaxis_title='Количество ДТП',
            yaxis_title='')
        
        return fig

    def create_road_condition_chart(df_filtered):
        road_data = df_filtered['Состояние проезжей части'].value_counts().head(4).reset_index()
        
        def wrap_text(text, max_length=10):
            words = text.split()
            lines = []
            current_line = ""
            for word in words:
                if len(current_line) + len(word) + 1 <= max_length:
                    current_line += (" " if current_line else "") + word
                else:
                    lines.append(current_line)
                    current_line = word
            if current_line:
                lines.append(current_line)
            return "<br>".join(lines)
    
        road_data['Состояние проезжей части_wrapped'] = road_data['Состояние проезжей части'].apply(wrap_text)

        fig = px.bar(
            road_data,
            y='Состояние проезжей части_wrapped',
            x='count',
            orientation='h',
            title='',
            color='count',
            color_continuous_scale='reds'
        )
        fig.update_xaxes(tickformat='d', separatethousands=True)
        fig.update_layout(coloraxis_showscale=False)
        fig.update_layout(
            xaxis_title='Количество ДТП',
            yaxis_title='')
        
        return fig

    def create_weekday_chart(df_filtered):
        weekday_data = df_filtered.groupby('День недели').size().reset_index(name='Количество ДТП')
        
        fig = px.bar(
            weekday_data,
            x='День недели',
            y='Количество ДТП',
            title='',
            color='Количество ДТП',
            color_continuous_scale='reds'
        )
        fig.update_yaxes(tickformat='d', separatethousands=True)
        fig.update_layout(coloraxis_showscale=False, xaxis=dict(dtick=1))
        return fig

    def create_risk_prediction_chart(df_filtered):
        try:
            ml_df = df_filtered.copy()
            y = ml_df['Смертность']
            X = ml_df[['Плохие погодные условия', 'Ограниченное освещение', 'Неудовлетворительное состояние проезжей части']]
            
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

            model_rf = RandomForestClassifier(
                class_weight='balanced_subsample',
                n_estimators=100,
                random_state=42,
                n_jobs=-1
            )

            model_rf.fit(X_train, y_train)

            feature_importance_rf = pd.DataFrame({
                'Фактор': X.columns,
                'Важность': model_rf.feature_importances_
            }).sort_values('Важность', ascending=False)

            fig = go.Figure()
            
            fig.add_trace(go.Bar(
                y=feature_importance_rf['Фактор'],
                x=feature_importance_rf['Важность'],
                orientation='h',
                marker_color="#660708",
            ))
            
            fig.update_layout(
                xaxis_title='Важность признака',
                
            )
            
            return fig
            
        except Exception as e:
            print(f"Ошибка в ML модели: {e}")
            return go.Figure()