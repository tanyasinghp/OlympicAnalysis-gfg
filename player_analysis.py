import plotly.express as px
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import streamlit as st
import plotly.graph_objects as go
import seaborn as sns

def create_medal_count_plot(name, df):
    # Clone the DataFrame and filter for the specific athlete
    df_clone = df.copy()
    df_clone = df_clone.dropna(subset=['athlete_full_name'])
    df_clone = df_clone[df_clone['athlete_full_name'] == name]

    # Select the desired columns
    filtered_df = df_clone[['slug_game', 'event_title', 'athlete_full_name', 'medal_type']]

    # Group the DataFrame by 'slug_game' and 'medal_type' and count the occurrences
    grouped_df = filtered_df.groupby(['slug_game', 'medal_type']).size().unstack().fillna(0)

    # Create a list of medal types
    medal_types = grouped_df.columns

    # Create a trace for each medal type
    traces = []
    for medal_type in medal_types:
        trace = go.Bar(
            x=grouped_df.index,
            y=grouped_df[medal_type],
            name=medal_type
        )
        traces.append(trace)

    # Create the layout
    layout = go.Layout(
        title=f"Medal Count by Venue Name for {name}",
        xaxis=dict(title='Venue Name'),
        yaxis=dict(title='Medal Count'),
        barmode='stack'
    )

    # Create the figure
    fig = go.Figure(data=traces, layout=layout)

    # Display the interactive plot
    st.plotly_chart(fig)


def medal_compare(name, df):
    # Clone the DataFrame and filter for the specific athlete
    df_clone = df.copy()
    df_clone = df_clone.dropna(subset=['athlete_full_name'])
    df_clone = df_clone[df_clone['athlete_full_name'] == name]

    # Select the desired columns
    filtered_df = df_clone[['slug_game', 'event_title', 'athlete_full_name', 'medal_type']]

    # Group the DataFrame by 'slug_game' and 'medal_type' and count the occurrences
    grouped_df = filtered_df.groupby(['slug_game', 'medal_type']).size().unstack().fillna(0)

    # Create a list of medal types
    medal_types = grouped_df.columns

    # Create a trace for each medal type
    traces = []
    for medal_type in medal_types:
        trace = go.Bar(
            x=grouped_df.index,
            y=grouped_df[medal_type],
            name=medal_type
        )
        traces.append(trace)

    # Create the layout
    layout = go.Layout(
        title=f"Medal Count by Venue Name for {name}",
        xaxis=dict(title='Venue Name'),
        yaxis=dict(title='Medal Count'),
        barmode='stack'
    )

    # Create the figure
    fig = go.Figure(data=traces, layout=layout)

    # Display the interactive plot
    st.plotly_chart(fig)
