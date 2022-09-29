# Import required libraries
from distutils.log import debug
from turtle import filling
import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px

spacex_df = pd.read_csv("spacex_launch_dash.csv")
labels=['Failed', 'Succeed']
spacex_df["Output"] = spacex_df["class"].map(dict(zip(range(0,2), labels)))


def query_df(df, launch_site, booster_type, payload):
    q_df = df[df['Launch Site'].isin(launch_site) & df['Booster Version Category'].isin(booster_type)]
    q_df = q_df[(q_df['Payload Mass (kg)'] > payload[0]) & (q_df['Payload Mass (kg)'] < payload[1])] 
    return q_df


def plot_scatter(df):
    fig = px.scatter(df, x="Flight Number", y="Launch Site", color="Output", size="Payload Mass (kg)", 
                     hover_data=["Flight Number", "Payload Mass (kg)"])
    fig.update_layout(title={'text': '<b>Launch Site And Outcome Of Each Flight No.</b>', 'x': 0.5, 
                            'xanchor': 'center', 'font_size': 18},
                      xaxis={'title': '<b>Flight Number</b>','fixedrange':True},
                      yaxis={'title': '<b>Launch Site</b>','fixedrange':True},)
    return fig


def plot_pie(df):
    plot_df = df.groupby('Output').count()
    fig = px.pie(plot_df, values='class', names=plot_df.index)
    fig.update_layout(title={'text': '<b>Percentage of Successful Outcomes</b>', 'x': 0.5, 'xanchor': 'center', 
                            'font_size': 18})
    return fig



app = dash.Dash(__name__, meta_tags=[{'name': 'viewport', 'content': 'width=device-width, initial-scale=1.0'}])
app.title = 'SpaceX Launch Dashboard'
app._favicon = ("SpaceX-Logo.ico")


# Create an app layout
app.layout = dbc.Container([dbc.Row(dbc.Col(html.H1('SpaceX Launch Records Dashboard', className='text-center text-dark mt-3 mb-4 font-weight-bold outline', 
                                            style={'font-size': 40}),width=12)),
                            dbc.Row(dbc.Col(dbc.Card(dbc.CardBody([dbc.Row(html.H4(' Select Launch Site And Booster Type', className='text-left text-dark font-weight-bold', style={'font-size': 20})),
                                                                   dbc.Row([dbc.Col(dcc.Dropdown(list(spacex_df['Launch Site'].unique()), placeholder="Select Launch Site", 
                                                                                                 value=list(spacex_df['Launch Site'].unique()),id='site-dropdown', 
                                                                                                 className='border-primary', style={'textAlign': "center", "width": "100%"}, multi=True),
                                                                            className='mb-2', xs=12, sm=12, md=12, lg=6, xl=6),
                                                                            dbc.Col(dcc.Dropdown(list(spacex_df['Booster Version Category'].unique()), placeholder="Select Booster Type", 
                                                                                                 value=list(spacex_df['Booster Version Category'].unique()),id='booster-dropdown', 
                                                                                                 className='border-primary', style={'textAlign': "center", "width": "100%"}, multi=True),
                                                                            className='mb-2', xs=12, sm=12, md=12, lg=6, xl=6)]),
                                                                   dbc.Row(html.H4(' Select Payload: ',className='text-left text-dark font-weight-bold', style={'font-size': 20})),
                                                                   dbc.Row(dbc.Col(dcc.RangeSlider(int(spacex_df['Payload Mass (kg)'].min()), int(spacex_df['Payload Mass (kg)'].max()), 
                                                                                    value=[0, 9600], id='payload-slider', tooltip={"placement": "bottom", "always_visible": True}),xs=12, sm=12, md=12, lg=12, xl=12))
                                                            ]),className='border-primary'),xs=12, sm=12, md=12, lg=12, xl=12), className='mb-2'),
                            dbc.Row(dbc.Col(dbc.Card(dbc.CardBody(dbc.Row([dbc.Col(dcc.Graph(id='success-pie-chart'), className='mb-2', xs=12, sm=12, md=12, lg=5, xl=5),
                                                                           dbc.Col(dcc.Graph(id='success_scatter'), className='mb-2', xs=12, sm=12, md=12, lg=7, xl=7)]), 
                                                                 ),className='border-primary', style={"width": "100%"})), className='mb-2'),
                            ],fluid=True)

@app.callback(
    Output('success-pie-chart', 'figure'),
    Output('success_scatter', 'figure'),
    Input('site-dropdown', 'value'),
    Input('booster-dropdown', 'value'),
    Input('payload-slider', 'value'),
    prevent_initial_call=False
)

def update_dashbaord(launch_site, booster_type, payload):
    df = query_df(spacex_df, launch_site, booster_type, payload)
    pie_chart = plot_pie(df)
    scatter_plot = plot_scatter(df)
    return pie_chart, scatter_plot


if __name__ == '__main__':
    app.run_server(debug=True)
