import dash
from dash import dcc, html, Input, Output
import requests
import pandas as pd
import os
import dash_bootstrap_components as dbc
from datetime import datetime

# 🔗 Configuration API
WEATHER_API_URL = os.getenv("WEATHER_API_URL", "http://weather_api:5000/cities")

# 🌟 Initialisation de Dash
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])
server = app.server

# 🛠️ **Mise en page du Dashboard**
app.layout = dbc.Container([
    html.H1("🌤️ Weather Dashboard", className='text-center mb-4'),

    dbc.Row([
        dbc.Col([
            html.Label("Select City:"),
            dcc.Dropdown(
                id='city-dropdown',
                options=[
                    {'label': city, 'value': city}
                    for city in ["New York", "London", "Paris", "Tokyo", "Sydney"]
                ],
                placeholder="Select a city"
            )
        ], width=4),

        dbc.Col([
            html.Label("Select Date Range:"),
            dcc.DatePickerRange(
                id='date-picker-range',
                start_date=pd.Timestamp.now() - pd.Timedelta(days=30),
                end_date=pd.Timestamp.now()
            )
        ], width=4),

        dbc.Col([
            html.Button('Load Data', id='load-data-btn', n_clicks=0, className='btn btn-primary mt-4')
        ], width=4)
    ], className='mb-4'),

    dbc.Row([
        dbc.Col([
            dcc.Graph(id='temperature-graph')
        ], width=4),
        dbc.Col([
            dcc.Graph(id='humidity-graph')
        ], width=4),
        dbc.Col([
            dcc.Graph(id='precipitation-graph')
        ], width=4),
    ], className='mb-4'),

    dbc.Row([
        dbc.Col([
            html.Div(id='city-info', className='border p-3 bg-light')
        ], width=12)
    ])
], fluid=True)


# 📊 **Callback : Charger les Données**
@app.callback(
    [Output('temperature-graph', 'figure'),
     Output('humidity-graph', 'figure'),
     Output('precipitation-graph', 'figure'),
     Output('city-info', 'children')],
    [Input('load-data-btn', 'n_clicks')],
    [Input('city-dropdown', 'value'),
     Input('date-picker-range', 'start_date'),
     Input('date-picker-range', 'end_date')]
)
def load_city_data(n_clicks, selected_city, start_date, end_date):
    if not selected_city:
        return {}, {}, {}, "⚠️ Please select a city."

    try:
        # 🔗 Récupération des données
        response = requests.get(f"{WEATHER_API_URL}/{selected_city}")
        if response.status_code == 200:
            data = response.json()
            df = pd.DataFrame(data)

            # 🕒 Normalisation des dates
            df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce', utc=True)
            df['timestamp'] = df['timestamp'].dt.tz_convert(None)
            df['timestamp'] = df['timestamp'].dt.floor('H')  # Arrondi à l'heure

            # 🛡️ Nettoyage
            df = df.drop_duplicates(subset=['timestamp'])
            df = df.dropna(subset=['temperature', 'humidity', 'precipitation', 'weather'])
            df = df[df['temperature'].between(-50, 50)]

            # 📅 Filtrage par plage de dates
            start_date = pd.to_datetime(start_date).replace(tzinfo=None)
            end_date = pd.to_datetime(end_date).replace(tzinfo=None)
            df = df[(df['timestamp'] >= start_date) & (df['timestamp'] <= end_date)]

            if df.empty:
                return {}, {}, {}, f"⚠️ No data available for {selected_city} in the selected date range."

            # 📊 Température (avec moyenne mobile)
            df['temperature_avg'] = df['temperature'].rolling(window=10).mean()

            temp_fig = {
                'data': [
                    {'x': df['timestamp'], 'y': df['temperature'], 'type': 'line', 'name': 'Temperature'},
                    {'x': df['timestamp'], 'y': df['temperature_avg'], 'type': 'line', 'name': 'Moving Average', 'line': {'dash': 'dash'}}
                ],
                'layout': {
                    'title': f"🌡️ Temperature Evolution in {selected_city}",
                    'xaxis': {'title': 'Timestamp'},
                    'yaxis': {'title': 'Temperature (°C)'}
                }
            }

            # 📊 Humidité
            humidity_fig = {
                'data': [{'x': df['timestamp'], 'y': df['humidity'], 'type': 'line', 'name': 'Humidity'}],
                'layout': {
                    'title': f"💧 Humidity Evolution in {selected_city}",
                    'xaxis': {'title': 'Timestamp'},
                    'yaxis': {'title': 'Humidity (%)'}
                }
            }

            # 📊 Précipitations
            precipitation_fig = {
                'data': [{'x': df['timestamp'], 'y': df['precipitation'], 'type': 'line', 'name': 'Precipitation'}],
                'layout': {
                    'title': f"🌧️ Precipitation Evolution in {selected_city}",
                    'xaxis': {'title': 'Timestamp'},
                    'yaxis': {'title': 'Precipitation (mm)'}
                }
            }

            # 📝 Extraire les valeurs actuelles
            latest_data = df.iloc[-1]
            city_info = (
                f"🌆 City: {selected_city} | "
                f"🌡️ Avg Temp: {df['temperature'].mean():.2f}°C | 🌡️ Current Temp: {latest_data['temperature']:.2f}°C\n"
                f"💧 Avg Humidity: {df['humidity'].mean():.2f}% | 💧 Current Humidity: {latest_data['humidity']:.2f}%\n"
                f"🌧️ Avg Precipitation: {df['precipitation'].mean():.2f}mm | 🌧️ Current Precipitation: {latest_data['precipitation']:.2f}mm\n"
                f"☁️ Current Weather: {latest_data['weather']}"
            )

            return temp_fig, humidity_fig, precipitation_fig, city_info

    except Exception as e:
        return {}, {}, {}, f"❌ Error: {str(e)}"


# 🚀 **Lancer le serveur Dash**
if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8050)
