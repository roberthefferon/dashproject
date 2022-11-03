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

df_us['case_day'] = df_us['cases'].diff()
df_us.loc[0, 'case_day'] = 1
df_us['case_day'] =  df_us['case_day'].astype('int')

url = "https://raw.githubusercontent.com/jagansingh93/covid_data/main/Weekly_United_States_COVID-19_Cases_and_Deaths_by_State.csv"
download = requests.get(url).content
df_state = pd.read_csv(io.StringIO(download.decode('utf-8')))
df_state.loc[df_state.new_cases  < 0,'new_cases'] = df_state.loc[df_state.new_cases  < 0,'new_cases'].abs()

def covid_cases():
    fig = px.line(x = df_us['date'], y = df_us['case_day'])
    fig.update_layout(title = 'COVID-19 cases in US', xaxis_title = 'Date', yaxis_title = 'Cases' )
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

index_page = html.Div([
    html.H1('COVID DASHBOARD'),
    dcc.Link('New Covid cases US', href='/page-1'),
    html.Br(),
    dcc.Link('State wise new cases', href='/page-2'),
])

page_1_layout = html.Div([
    html.H1('New Covid cases US'),
    dcc.Graph(id = 'line_plot', figure = covid_cases())
])

page_2_layout = html.Div([
    html.H1('New Covid cases US'),
    dcc.Graph(id = 'map', figure = states_map())
])

@callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/page-1':
        return page_1_layout
    elif pathname == '/page-2':
        return page_2_layout
    else:
        return index_page

if __name__ == '__main__':
    app.run_server()
