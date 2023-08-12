import plotly.express as px
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import streamlit as st

def geo(df):
# Group the DataFrame by country_name and medal_type, and calculate the total number of medals
    grouped = df.groupby(['country_name', 'medal_type']).size().unstack().reset_index()

# Calculate the total number of medals for each country
    grouped['Total Medals'] = grouped.sum(axis=1)

# Create a choropleth map using Plotly
    fig = px.choropleth(grouped, 
                        locations='country_name', 
                        locationmode='country names',
                        color='Total Medals',
                        color_continuous_scale='YlGnBu',
                        title='Total Medals by Country',
                        hover_name='country_name')

# Display the interactive plot
    st.plotly_chart(fig)
    
#   


def create_choropleth_map(df):
    # Group the DataFrame by country_name and medal_type, and calculate the total number of medals
    grouped = df.groupby(['country_name', 'medal_type']).size().unstack().reset_index()

    # Create separate columns for gold, silver, and bronze counts
    grouped['Gold'] = grouped['GOLD']
    grouped['Silver'] = grouped['SILVER']
    grouped['Bronze'] = grouped['BRONZE']

    grouped['Total Medals'] = grouped[['Gold', 'Silver', 'Bronze']].sum(axis=1)

    # Create a choropleth map using Plotly
    fig = px.choropleth(grouped, 
                        locations='country_name', 
                        locationmode='country names',
                        color='Total Medals',
                        color_continuous_scale='YlGnBu',
                        title='Individual Medals won by each Country',
                        hover_name='country_name',
                        hover_data=['Gold', 'Silver', 'Bronze'])

    # Display the interactive plot
    st.plotly_chart(fig)



def geo_dis(df):
# Group the DataFrame by country_name and medal_type, and calculate the total number of medals
    grouped = df.groupby(['country_name', 'discipline_title']).size().unstack().reset_index()
    grouped['discipline_title']=grouped['Athletics']
    grouped['discipline_title']=grouped['Swimming']
    grouped['discipline_title']=grouped['Wrestling']
    grouped['discipline_title']=grouped['Rowing']
    grouped['discipline_title']=grouped['Boxing']

# Calculate the total number of medals for each country
    grouped['discipline_title'] = grouped[['Athletics','Swimming','Wrestling','Rowing','Boxing']].sum(axis=1)

# Create a choropleth map using Plotly
    fig = px.choropleth(grouped, 
                        locations='country_name', 
                        locationmode='country names',
                        color='discipline_title',
                        color_continuous_scale='YlGnBu',
                        title='Top 5 Disciplines by Country',
                        hover_name='country_name',
                        hover_data=['Athletics','Swimming','Wrestling','Rowing','Boxing'])
                        

# Display the interactive plot
    st.plotly_chart(fig)