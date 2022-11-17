# Importing libraries
import os
import dash
import requests
import io
from dash import Dash, dcc, html, Input, Output, callback
import pandas as pd
import plotly.express as px
from datetime import date, timedelta

# importing data
url = "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us.csv"
download = requests.get(url).content
df_us = pd.read_csv(io.StringIO(download.decode('utf-8')))

df_us['cases_per_day'] = df_us['cases'].diff()
df_us.loc[0, 'cases_per_day'] = 1
df_us['cases_per_day'] =  df_us['cases_per_day'].astype('int')

df_us['deaths_per_day'] = df_us['deaths'].diff()
df_us.loc[0, 'deaths_per_day'] = 0
df_us['deaths_per_day'] =  df_us['deaths_per_day'].astype('int')
df_us['deaths_per_day'] = df_us['deaths_per_day'].abs()

url = "https://raw.githubusercontent.com/jagansingh93/covid_data/main/Weekly_United_States_COVID-19_Cases_and_Deaths_by_State.csv"
download = requests.get(url).content
df_state = pd.read_csv(io.StringIO(download.decode('utf-8')))
df_state['new_cases'] = df_state['new_cases'].abs()

def covid_cases(name):
    fig = px.line(x = df_us['date'], y = df_us[name])
    fig.update_layout(title = 'COVID-19 cases in US')
    return fig

def states_map():
    fig = px.scatter_geo(df_state, size="new_cases", locationmode = 'USA-states', locations = 'state', scope = 'usa', animation_frame = 'date_updated')
    fig.update_layout(title = 'States map')
    return fig


app = dash.Dash(__name__)
server = app.server
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

home_page = html.Div([
    html.H1('COVID DASHBOARD'),
    dcc.Dropdown(list(df_us.drop(columns = ['date']).columns), 'cases', id= 'dropdown'),
    dcc.Graph(id = 'graph'),
    html.Br(),
    dcc.Link('State wise new cases', href='/state_wise', id = 'button')
])

@app.callback(
    Output('graph', 'figure'),
    Input('dropdown', 'value')
)
def update_output(value):
    return covid_cases(value)

state_wise_layout = html.Div([
    html.H1('New Covid cases US'),
    dcc.Graph(id = 'map', figure = states_map())
])

@callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/state_wise':
        return state_wise_layout
    else:
        return home_page

if __name__ == '__main__':
    app.run_server()
