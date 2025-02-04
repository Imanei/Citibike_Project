################################################ CITI BIKES DASHABOARD #####################################################

import streamlit as st
import pandas as pd
import numpy as np
import os
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from streamlit_keplergl import keplergl_static
from keplergl import KeplerGl
from datetime import datetime as dt

############################## INITIAL SETTINGS #########################################
st.set_page_config(page_title = 'Citi Bike Strategy Dashboard', page_icon="🚲",layout='wide')
st.title("🚲 Citi Bike Strategy Dashboard")
st.markdown("#### This dashboard will help analyze current user behavior and identify expansion opportunities")
st.markdown("_Since its launch in 2013, Citi Bike has grown in popularity, and the demand surged even further during the Covid-19 pandemic as more New York residents embraced bike sharing. However, this increased usage has created distribution challenges, such as shortages at high-traffic stations and overcrowding at others, making bike returns difficult._")
st.markdown("_To address these issues, we need to identify where imbalances are most frequent and understand their underlying causes._")
st.markdown("""
This dashboard provides insights into CitiBike trips, including the most popular routes, seasonal trends, and bike usage patterns.  
Use the filters and visualizations to explore the data!
""")
############################## IMPORT DATA ##############################################
# Define the folder path
folderpath = "../Citibike_Project/Data/Prepared_data"
top20 = pd.read_csv(os.path.join(folderpath, 'top_start_stations.csv'), index_col = 0)
df_temp = pd.read_csv(os.path.join(folderpath, 'DB_line_chart_data.csv'), index_col = 0)

############################## DEFINE THE CHARTS ########################################

####################### BAR CHART #######################
st.header("Top 20 Most Popular Citi Bike Stations in New York 2022")
fig = go.Figure(go.Bar(x = top20['start_station_name'],
                       y = top20['value'],
                       marker = {'color' : top20['value'], 'colorscale' : 'blues'}))

fig.update_layout(
    xaxis_title = dict(text = '<b>Start Stations</b>', 
                        font = dict(size = 22)),
    yaxis_title = dict(text = '<b>Total Trips</b>', 
                        font = dict(size = 22)),
    xaxis = dict(tickfont = dict(size=16)),
    yaxis = dict(tickfont = dict(size=16)),
    width = 900, height = 600
)
fig.update_xaxes(
    automargin = True
)
st.plotly_chart(fig, use_container_width = True)

####################### LINE CHART #######################
st.header("Daily Bike Trips and Avergage NYC Temperature in 2022")
line_fig = make_subplots(specs = [[{"secondary_y": True}]])

line_fig.add_trace(
go.Scatter(x = df_temp.index, 
           y = df_temp['Daily Rides'], 
           name = 'Daily bike rides',
           marker = {'color': df_temp['Daily Rides'],'color': '#2B4B8D'},
           fill = 'tozeroy'),
secondary_y = False
)

line_fig.add_trace(
go.Scatter(x = df_temp.index, 
           y = df_temp['Average Temperature'], 
           name = 'Daily temperature',
           marker={'color': df_temp['Average Temperature'],'color': '#EB392A'}),
secondary_y = True
)

line_fig.update_layout(
    xaxis_title = '',
    yaxis1_title = dict(text = '<b>Bike Rides Daily</b>', 
                        font = dict(size = 22, color = '#2B4B8D')),
    yaxis2_title = dict(text = '<b>Average Temperature (in C)</b>', 
                        font = dict(size = 22, color = '#EB392A')),
    xaxis = dict(showgrid = False,
                 range = [dt(2022, 1, 1), dt(2023, 1, 1)],
                 tickfont = dict(size=16)),
    yaxis1 = dict(showgrid = False,
                  tickfont = dict(size=14)),
    yaxis2 = dict(showgrid = False,
                  zeroline = False,
                  tickfont = dict(size=14)),
    showlegend = False,
    margin = dict(pad = 10),
    width = 900, height = 500
)

line_fig.update_yaxes(
    automargin = True
)
st.plotly_chart(line_fig, use_container_width=True)


####################### GEOSPATIAL VISUALIZATION #######################
path_to_html = "./Citi_Bike_Trips.html"
# Read file and keep in variable
with open(path_to_html, 'r', encoding='utf-8') as f:
    html_data = f.read()


## Show in webpage
st.header("Aggregated Bike Trips in New York")
st.components.v1.html(html_data,height=1000)