############################# CITI BIKES DASHBOARD #####################################
#########################################################################################

import streamlit as st
import streamlit.components.v1 as components
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
from numerize.numerize import numerize
from PIL import Image

############################## INITIAL SETTINGS #########################################
#########################################################################################

st.set_page_config(page_title = 'Citi Bike Strategy Dashboard', page_icon="🚲", layout='wide')
st.title("Citi Bike in New York City 2022 🚲")
st.subheader("Exploring User Behavior & Expansion Opportunities")

## Define side bar
st.sidebar.markdown("## 📍 Navigation")
page = st.sidebar.selectbox('Select an aspect of the analysis',
  ['Intro Page',
   'Seasonality of Bike Usage',
   'Most Popular Stations',
   'Map of Aggregated Bike Trips', 
   'User Behavior Analysis',
   'Recommendations'])

## Theme colors
colors = ['#2B4B8D', '#3881B5']
accent = '#EB392A'

################################## IMPORT DATA ##########################################
#########################################################################################

folderpath = "../Citibike_Project/Data/Prepared_data"
picturepath = "../Citibike_Project/Visualizations"
path_to_html = "./Citi_Bike_Trips.html"

line_chart_data = pd.read_csv(os.path.join(folderpath, 'DB_line_chart_data.csv'), index_col = 0)
bar_chart_start = pd.read_csv(os.path.join(folderpath, 'DB_bar_chart_start.csv'), index_col = 0)
bar_chart_end = pd.read_csv(os.path.join(folderpath, 'DB_bar_chart_end.csv'), index_col = 0)
pie_payment_data = pd.read_csv(os.path.join(folderpath, 'DB_pie_payment.csv'))
hist_duration_data = pd.read_csv(os.path.join(folderpath, 'DB_hist_duration.csv'), index_col = 0)

################################### INTRO PAGE ##########################################
#########################################################################################

if page == 'Intro Page':

    st.markdown(
    "*Since its launch in 2013, Citi Bike has surged in popularity, with demand skyrocketing during the COVID-19 pandemic. However, this growth has led to distribution challenges, where some stations experience shortages while others are overcrowded.*")
    st.markdown("🚴 This dashboard helps explore:")
    st.markdown("✔ *Seasonal demand trends*")
    st.markdown("✔ *Most frequently used stations* ")
    st.markdown("✔ *Common bike routes and distribution issues* ")
    st.markdown("✔ *Actionable recommendations for improvement* ")
    st.markdown("Use the sidebar to explore! 📊")

    col1, col2 = st.columns(2)
    
    with col1:
        with st.expander('🌦️ Weather & Bike Usage'):
            st.markdown("- Is demand seasonal?")
            st.markdown("- Which bike type (Classic/Electric) is preferred?")
        with st.expander('📍 Most Popular Stations'):
            st.write(
                '''What are the most-used starting and ending stations?''')
            st.write(
                '''Is there a difference between where trips begin and end?''')
            st.write(
                '''Do users favor different bike types at different locations?''')
        with st.expander('🗺️ Interactive Map with Aggregated Bike Trips'):
            st.write(
                '''Where are the top 20 busiest stations?''')
            st.write(
                '''What are the most common routes?''')
        with st.expander('🚦 Addressing Distribution Issues'):
            st.write(
                '''Where do imbalances occur?''')
            st.write(
                '''What’s causing these problems?''')
            st.write(
                '''How can we optimize the system to prevent shortages?''')
        st.text("")
    st.markdown(
        """ To see more about these different aspects of the analysis, click on the drop down menu in the left sidebar
"""
    )
       
    with col2:
        myImage = Image.open(os.path.join(picturepath, 'citibike_Dashboard.jpg')) 
        #source: https://www.freepik.com/free-vector/happy-young-family-riding-bikes-park_7416563.htm#fromView=search&page=1&position=30&uuid=f1e4be12-be3f-43c3-9cf6-13f8f06ce3de&query=citibike
        st.image(myImage)

############################# WEATHER COMPONENT AND BIKE USAGE ##########################
#########################################################################################

elif page == 'Seasonality of Bike Usage':
    st.title("Daily Bike Trips and Avergage NYC Temperature")
    st.subheader("How Does Weather Affect Citi Bike Usage?")

    ####################### LINE CHART #######################
    line_fig = make_subplots(specs = [[{"secondary_y": True}]])

    ## Electric bike rides area chart
    line_fig.add_trace(go.Scatter(x = line_chart_data['Date'], 
                                  y = line_chart_data['Daily Rides'], 
                                  fill = 'tozeroy', #fill down to xaxis
                                  fillcolor = 'rgba(56, 129, 181, 0.8)',
                                  mode = 'lines',
                                  line = {'color': '#3881B5'},
                                  name = 'Electric Bikes'),
                        secondary_y = False)

    ## Classic bike rides area chart
    line_fig.add_trace(go.Scatter(x = line_chart_data['Date'], 
                                  y = line_chart_data['Daily Classic Rides'], 
                                  fill = 'tozeroy', #fill down to xaxis
                                  fillcolor = 'rgba(43, 75, 141, 0.8)',
                                  mode = 'lines',
                                  line = {'color': '#2B4B8D'},
                                  name = 'Classic Bikes'),
                       secondary_y = False)

    ## Average temperature line chart
    line_fig.add_trace(
    go.Scatter(x = line_chart_data['Date'], 
               y = line_chart_data['Average Temperature'], 
               name = '',
               showlegend = False,
               marker={'color': line_chart_data['Average Temperature'],'color': accent}),
    secondary_y = True
    )

    ## Formatting axes and titles
    line_fig.update_layout(
        xaxis_title = '',
        yaxis1_title = dict(text = '<b>Bike Rides Daily</b>', 
                            font = dict(size = 22, color = '#2B4B8D')),
        yaxis2_title = dict(text = '<b>Average Temperature (in C)</b>', 
                            font = dict(size = 22, color = accent)),
        xaxis = dict(showgrid = False,
                     range = [dt(2022, 1, 1), dt(2023, 1, 1)],
                     tickfont = dict(size = 16, color = '#2B4B8D')),
        yaxis1 = dict(showgrid = False,
                      tickfont = dict(size = 14, color = '#2B4B8D'),
                      color = '#323232'),
        yaxis2 = dict(showgrid = False,
                      zeroline = False,
                      tickfont = dict(size = 14, color = '#2B4B8D'),
                      color = '#323232'),
        showlegend = True,
        legend = dict(yanchor = 'top',
                      y = 0.95,
                      xanchor = 'left',
                      x = 0.05,
                      font = dict(size = 16)
                     ),
        margin = dict(pad = 10),
        width = 900, height = 500
    )

    line_fig.update_yaxes(
        automargin = True
    )
    
    st.plotly_chart(line_fig, use_container_width=True)


    ####################### ANALYSIS #######################
    # Section Header
    st.markdown("## How Weather Affects Citi Bike Usage 🌡️")

# Summary of Insights
    st.markdown(
    """
    - **Bike usage is strongly correlated with temperature.** Warmer weather leads to more rides, while colder temperatures see a significant drop in activity.
    - **Peak ridership occurs in late spring and summer (March–August)** as temperatures rise, encouraging outdoor activity.
    - **Ridership declines in fall and winter**, with a sharp drop in December as cold weather sets in.
    - **Bike rentals are not strictly seasonal**—users check daily weather conditions before deciding to ride.
    """
    )

# Key Observations
    st.markdown("### Key Observations 🚴‍♂️")
    st.markdown(
    """
    - On **September 27th and October 7th**, high temperatures correlated with strong bike rental numbers.
    - Conversely, when temperatures dropped to **10.3°C**, bike rentals also declined significantly.
    - Despite known **heat sensitivity issues with electric bike batteries**, electric bike usage increases significantly in the summer.
    """
    )

# Possible Reasons for Higher Ridership in Warm Weather
    st.markdown("### Why Do More People Bike in Warm Weather? ☀️")
    st.markdown(
    """
    - **Tourism peaks** in summer, increasing Citi Bike usage by visitors.
    - **Outdoor exercise is more appealing**, making biking a preferred mode of transportation.
    - **Subway usage declines** in affluent areas during the summer, suggesting a shift to biking.
    - **Remote work trends** allow for flexible travel, encouraging bike usage for short local trips.
    - **Schools are out**, leading to increased bike rides by students.
    """
    )

# Actionable Insights
    st.markdown("### Actionable Insights 📊")
    st.markdown(
    """
    - **Expand bike availability during peak months** (March–August) to meet increased demand.
    - **Consider promotions or discounts in colder months** to encourage winter ridership.
    - **Monitor electric bike performance in high temperatures** to address potential battery concerns.
    """
    )
   

################################ MOST POPULAR STATIONS ##################################
#########################################################################################

elif page == 'Most Popular Stations':
    st.title("Top 20 Most Popular Citi Bike Stations in New York")

    ################## START/END TOGGLE #####################
    myKey = 'my_key'
    if myKey not in st.session_state:
        st.session_state[myKey] = False
    
    ####################### BAR CHARTS #######################
    if st.session_state[myKey]:
        col1, col2, col3 = st.columns(3)
        with col1:
            pass
        with col3:
            pass
        with col2:
            myBtn = st.button('Click to see Starting Stations', use_container_width=True)
            st.session_state[myKey] = False
        
        with st.sidebar:
         season_filter = st.multiselect(label= 'Select the season', options=bar_chart_end['season'].unique(),
         default= bar_chart_end['season'].unique())
         df1 = bar_chart_end.query('season == @season_filter')
         total_rides = float(df1['Total'].sum())    
         st.metric(label = 'Total Bike Rides', value= numerize(total_rides))

        ## Ending Stations Bar Chart
        bar_end_fig = go.Figure(px.bar(df1.sort_values(['Grand Total', 'rideable_type'], 
                                                                 ascending=[False, True]),
                                       x = 'end_station_name', 
                                       y = 'Total', 
                                       color = 'rideable_type',
                                       barmode = 'stack',
                                       color_discrete_sequence = colors))

        ## Formatting axes and titles
        bar_end_fig.update_layout(
            xaxis_title = dict(text = '<b>End Stations</b>', 
                               font = dict(size = 22, color = '#2B4B8D')),
            yaxis_title = dict(text = '<b>Total Trips</b>', 
                               font = dict(size = 22, color = '#2B4B8D')),
            xaxis = dict(tickfont = dict(size = 14, color = '#2B4B8D')),
            yaxis = dict(tickfont = dict(size = 14, color = '#2B4B8D')),
            legend_title_text = '',
            legend = dict(yanchor = 'top',
                          y = 0.95,
                          xanchor = 'right',
                          x = 0.95,
                          font = dict(size = 16)
                         ),
            width = 900, height = 600
        )

        bar_end_fig.update_xaxes(
            automargin = True 
        )

        st.plotly_chart(bar_end_fig, use_container_width = True)
        
    else:
        col1, col2, col3 = st.columns(3)
        with col1:
            pass
        with col3:
            pass
        with col2:
            myBtn = st.button('Click to see Ending Stations', use_container_width=True)
            st.session_state[myKey] = True
        
        with st.sidebar:
         season_filter = st.multiselect(label= 'Select the season', options=bar_chart_start['season'].unique(),
         default= bar_chart_start['season'].unique())
         df2 = bar_chart_start.query('season == @season_filter')
         total_rides = float(df2['Total'].sum())    
         st.metric(label = 'Total Bike Rides', value= numerize(total_rides))

        ## Starting Stations Bar Chart
        bar_start_fig = go.Figure(px.bar(df2.sort_values(['Grand Total', 'rideable_type'],
                                                         ascending = [False, True]),
                                         x = 'start_station_name', 
                                         y = 'Total', 
                                         color = 'rideable_type',
                                         barmode = 'stack',
                                         color_discrete_sequence = colors))

        ## Formatting axes and titles
        bar_start_fig.update_layout(
            xaxis_title = dict(text = '<b>Start Stations</b>', 
                               font = dict(size = 22, color = '#2B4B8D')),
            yaxis_title = dict(text = '<b>Total Trips</b>', 
                               font = dict(size = 22, color = '#2B4B8D')),
            xaxis = dict(tickfont = dict(size = 14, color = '#2B4B8D')),
            yaxis = dict(tickfont = dict(size = 14, color = '#2B4B8D')),
            legend_title_text = '',
            legend = dict(yanchor = 'top',
                          y = 0.95,
                          xanchor = 'right',
                          x = 0.95,
                          font = dict(size = 16)
                         ),
            width = 900, height = 600
        )

        bar_start_fig.update_xaxes(
        automargin = True 
        )

        st.plotly_chart(bar_start_fig, use_container_width = True)


    ####################### ANALYSIS #######################
    st.markdown(
    """
    The station at W 21 St & 6 Ave stands out as the most frequented starting and ending point for Citi Bike trips. 
    Interestingly, all of the top 20 stations are located in Manhattan, despite it being the third most populous borough in New York City. 
    This suggests that the popularity of Citi Bike stations isn’t necessarily tied to population density.

    With the exception of one station, the most popular starting stations also happen to be the most popular ending stations, 
    which might point to commuters being a primary user group. However, the concentration of popular stations near major tourist attractions—such as Central Park, Washington Square Park, etc—suggests 
    that tourism is a key driver of demand. These stations likely see high traffic due to their proximity to iconic New York destinations.
    """
    )

    
####################### INTERACTIVE MAP OF AGGREGATED BIKE TRIPS ########################
#########################################################################################

elif page == 'Map of Aggregated Bike Trips':
    st.title("Aggregated Bike Trips in New York")

    ####################### GEOSPATIAL VISUALIZATION #######################

    st.markdown("**Most Popular Bike Trips**")

    with open(path_to_html, 'r', encoding='utf-8') as f:
     html_data = f.read()

    # Show in webpage
    st.header("Aggregated Bike Trips in New York")
    st.components.v1.html(html_data, height=1000) 


    ####################### ANALYSIS #######################
    st.text("")
    st.markdown("### Busy Zones:")
    st.markdown("The densest areas of trips are concentrated in Midtown and Lower Manhattan, with heavy traffic around Times Square and there are significant movements between Manhattan and Brooklyn. These areas are major commercial and transit hubs, which explains the high trip volume.")
    st.text("")
    st.markdown("These patterns align with New York City's transit infrastructure, where business districts and major transportation hubs generate the highest trip activity. The visualization helps understand how people move through the city and which areas see the most traffic.")
   

############################## USER BEHAVIOR ANALYSIS ##############################
elif page == 'User Behavior Analysis':   
    st.markdown("## User Behavior Analysis")
    col1, col2 = st.columns([0.6, 0.4])
    with col1:
        ########################### DURATION HISTOGRAM #########################
        hist_fig = px.histogram(hist_duration_data,
                                x = 'trip_duration',
                                nbins = 50,
                                color = 'member_casual',
                                color_discrete_sequence = ['#2B4B8D', '#3881B5'])

        hist_fig.update_layout(bargap = 0.05)

        ## Calculate median for line label
        member_median_data = hist_duration_data.loc[hist_duration_data['member_casual'] == 'Member']
        member_median = np.median(member_median_data['trip_duration'])
        casual_median_data = hist_duration_data.loc[hist_duration_data['member_casual'] == 'Casual']
        casual_median = np.median(casual_median_data['trip_duration'])

        ## Add median line and annotation for both member and casual charts
        hist_fig.add_vline(x = member_median,
                           line_width = 2,
                           line_dash = 'solid',
                           line_color = accent)
        hist_fig.add_annotation(x = member_median,
                                y = 45000,
                                text = f"<b>Member Median: <br>{member_median:.0f} sec</b>",
                                font = dict(color = '#2B4B8D', size = 14),
                                showarrow = False,
                                xshift = -24,
                                yshift = 0)

        hist_fig.add_vline(x = casual_median,
                           line_width = 2,
                           line_dash = 'solid',
                           line_color = accent)
        hist_fig.add_annotation(x = casual_median,
                                y = 35000,
                                text = f"<b>Casual Median: <br>{casual_median:.0f} sec</b>",
                                font = dict(color = '#2B4B8D', size = 14),
                                showarrow = False,
                                xshift = 24,
                                yshift = 0)

        ## Formatting axes and titles
        hist_fig.update_layout(legend_title_text = '',
                               legend = dict(yanchor = 'top',
                                             y = 0.95,
                                             xanchor = 'right',
                                             x = 0.65,
                                             font = dict(size = 16)),
                               xaxis_title = dict(text = '<b>Trip Duration (in seconds)</b>',
                                                  font = dict(size = 18, color = '#2B4B8D')),
                               yaxis_title = dict(text = ''),
                               xaxis = dict(tickfont = dict(size = 14, color = '#2B4B8D')),
                               yaxis = dict(tickfont = dict(size = 14, color = '#2B4B8D'),
                                            visible = False),
                               width = 900, height = 400)
        
        st.plotly_chart(hist_fig, use_container_width = True)

    with col2:
        ####################### MEMBER STATUS PIE CHART ########################
        pie_fig = px.pie(pie_payment_data,
                         values = 'value',
                         names = 'member_casual',
                         color = 'member_casual',
                         color_discrete_sequence = ['#3881B5', '#2B4B8D'],
                         hole = 0.6,
                         labels = ['<b>Member</b>', '<b>Casual</b>'])

        ## Formatting pie chart and labels
        pie_fig.update_traces(textinfo = 'label+percent',
                              
                              textfont_size = 15,
                              insidetextorientation = 'horizontal',
                              showlegend = False,
                              rotation = 0)

        pie_fig.update_layout(height = 450, width = 450)

        st.plotly_chart(pie_fig, use_container_width = True)

####################### ANALYSIS #######################
    st.text("")
    st.markdown("**Trip Duration Distribution:**")
    st.markdown("The median trip duration for members is 550 seconds, while for casual users, it is significantly higher at 887 seconds. This suggests that casual users tend to take longer trips compared to members.")
    st.text("")
    st.markdown("**Membership Breakdown:**")
    st.markdown("The majority of Citi Bike users are subscribed members, likely using the service for regular commuting or shorter, consistent trips.")
    st.text("")
    st.markdown("**Behavioral Insights**")
    st.markdown(" - Members appear to prioritize shorter, more frequent rides, possibly due to routine travel needs or familiarity with the service.")
    st.markdown(" - Casual users may use the bikes for leisure, sightseeing, or less frequent activities, explaining the longer trip durations.")

################################# RECOMMENDATIONS #######################################
#########################################################################################

else:
    st.markdown("## Recommendations")

    col1, col2 = st.columns(2)
    with col1:
        myImage2 = Image.open(os.path.join(picturepath,'Citibike_Dashboard.jpg')) 
        #source: https://unsplash.com/photos/bicycles-parked-on-the-side-of-a-street-KcOoW1Tv06Q
        st.image(myImage2)

        
    with col2:
        st.text("")
        myImage3 = Image.open(os.path.join(picturepath,'Citibike_Dashboard3.jpg')) 
        #source: https://www.freepik.com/free-vector/businessman-holding-pencil-big-complete-checklist-with-tick-marks_11879344.htm#fromView=search&page=1&position=0&uuid=a12ba572-a4bc-4cfe-afcf-7910198d9cd3&query=recommendations
        st.image(myImage3)
            
    st.text("")
   

    # Weather and Bike Usage Section
    st.header("🌦️ Weather & Bike Usage")
    st.markdown("""
    **Seasonal Demand:**
     - Peak usage occurs in spring and summer (March–August).
     - Usage declines sharply in winter months (December–February).
     - Electric bike usage increases in summer, despite potential battery heat issues.

    **Actionable Insights:**
      1. Increase bike availability during high-demand months (March–August).
      2. Offer winter discounts to boost off-season ridership.
      3. Monitor electric bike batteries during extreme temperatures.
    """)

     # Bike Type Preference
    st.header("🚲 Bike Type Preference")
    st.markdown("""
    **Observations:**
      - Electric bikes dominate usage, year-round, suggestion their convenience and efficency appeal to both members and casual users.
      - Usage of eletric bikes still sees a noticeable increase in summer, likely due to higher tourism and longer trips.

    **Recommendations:**
      1. Expand the fleet of electric bikes to meet growing demand.
      2. Monitor battery performance, especially in extreme weather conditions(both heat in summer and cold in winter).
      3. Highlight the benefits of electric bikes in marketing campaigns to further encourage adoption by casual and new riders.
     """)

     # Most Popular Stations
    st.header("📍 Most Popular Stations")
    st.markdown("""
                **Insights:**
  - The busiest station is W 21 St & 6 Ave.
  - All top 20 stations are located in Manhattan, particularly near tourist attractions like Central Park and Washington Square Park.
  - Starting and ending stations overlap, indicating commuter-driven usage.
                **Recommendations:**
  1. Optimize bike inventory near high-traffic stations.
  2. Reduce congestion at popular stations by incentivizing trips to lesser-used docks.
""")

# Interactive Map Insights
    st.header("🗺️ Interactive Map Insights")
    st.markdown("""
- *Top 20 Busiest Stations:* Concentrated in Midtown and Lower Manhattan.
- *Most Common Routes:* Short trips dominate in commercial hubs, while cross-borough routes see longer trips.

**Recommendations:**
  1. Improve docking availability in Midtown and Lower Manhattan.
  2. Offer route-based promotions for tourists and casual riders.
""")

# Addressing Distribution Issues
    st.header("🔄 Addressing Distribution Issues")
    st.markdown("""
**Challenges:**
  - Dock shortages occur at high-traffic stations during peak hours.
  - Cross-borough trips create imbalances, as bikes move from Brooklyn to Manhattan.

**Optimization Strategies:**
  1. Use predictive analytics to redistribute bikes proactively.
  2. Deploy flexible dockless bikes in areas with persistent shortages.
  3. Incentivize riders to return bikes to underutilized stations.
""")

# User Behavior Insights
    st.header("📊 User Behavior Insights")
    st.markdown("""
**Trip Duration:**
  - Median trip duration for members is *550 seconds, while casual users take longer trips (median: **887 seconds*).

**Membership Breakdown:**
  - 77.9% of users are members, using bikes for routine commutes.
  - 22.1% are casual riders, primarily tourists or occasional users.

**Recommendations:**
  1. Design campaigns to convert casual riders into members.
  2. Enhance availability at transit hubs for member convenience.
  3. Offer leisure-friendly packages for tourists.
""")

# Closing and Key Takeaways
    st.header("📌 Key Takeaways")
    st.markdown("""
1. Expand bike availability during peak demand periods.
2. Optimize dock distribution to address imbalances.
3. Promote electric bike adoption and resolve battery issues.
4. Offer seasonal promotions to boost engagement.
5. Use real-time data for continuous operational improvements.
""")

