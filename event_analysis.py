import plotly.express as px
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import streamlit as st
import plotly.graph_objects as go
import numpy as np

def analyze_gender_orientation(df):
    """
    Analyze the gender orientation of disciplines based on the proportion of male and female competitors.

    Parameters:
        df (pandas.DataFrame): The DataFrame containing the data.

    Returns:
        pandas.DataFrame: The DataFrame with the gender orientation analysis for each discipline.
    """
    # Remove rows with null values in the 'event_gender' column
    df = df.dropna(subset=['event_gender'])

    # Group the DataFrame by 'discipline_title' and 'event_gender'
    grouped_df = df.groupby(['discipline_title', 'event_gender']).size().reset_index(name='competitor_count')

    # Pivot the DataFrame to get the count of male and female competitors for each discipline
    pivot_df = grouped_df.pivot(index='discipline_title', columns='event_gender', values='competitor_count')

    # Calculate the proportion of male and female competitors for each discipline
    pivot_df['total_competitors'] = pivot_df['Men'].fillna(0) + pivot_df['Women'].fillna(0)
    pivot_df['male_proportion'] = pivot_df['Men'].fillna(0) / pivot_df['total_competitors']
    pivot_df['female_proportion'] = pivot_df['Women'].fillna(0) / pivot_df['total_competitors']

    # Categorize disciplines based on gender orientation
    conditions = [
        (pivot_df['male_proportion'] > 0.5),
        (pivot_df['female_proportion'] > 0.5),
        (pivot_df['male_proportion'] == pivot_df['female_proportion']),
        (pivot_df['Men'].isna() & pivot_df['Women'].notna()),
        (pivot_df['Women'].isna() & pivot_df['Men'].notna())
    ]
    choices = ['Male-Oriented', 'Female-Oriented', 'Balanced', 'Female-Oriented', 'Male-Oriented']
    pivot_df['orientation'] = pd.Series(np.select(conditions, choices, default=None), index=pivot_df.index)

    # Filter in 'Balanced' disciplines
    filtered_df = pivot_df[(pivot_df['orientation'] == 'Balanced')]
    male_df = pivot_df[~pivot_df['orientation'].isin(['Balanced', 'Female-Oriented'])]
    female_df= pivot_df[~pivot_df['orientation'].isin(['Balanced', 'Male-Oriented'])]
    return filtered_df,male_df,female_df


def plot_gender_orientation(filtered_df, male_df, female_df):
    """
    Plot the gender orientation of disciplines using Plotly.

    Parameters:
        filtered_df (pandas.DataFrame): The DataFrame containing the filtered disciplines.
        male_df (pandas.DataFrame): The DataFrame containing the male-oriented disciplines.
        female_df (pandas.DataFrame): The DataFrame containing the female-oriented disciplines.
    """
    # Create a scatter plot with labels for the gender orientations
    fig = go.Figure()

    # Add a scatter trace for balanced orientation
    fig.add_trace(
        go.Scatter(
            x=filtered_df.index,
            y=filtered_df['total_competitors'],
            mode='markers',
            hovertemplate='<b>Discipline:</b> %{x}<br><b>Orientation:</b> Balanced',
            marker=dict(color='black', symbol='circle', size=10),
            name='Balanced'
        )
    )

    # Add a scatter trace for male orientation
    fig.add_trace(
        go.Scatter(
            x=male_df.index,
            y=male_df['total_competitors'],
            mode='markers',
            hovertemplate='<b>Discipline:</b> %{x}<br><b>Orientation:</b> Male-Oriented',
            marker=dict(color='blue', symbol='circle', size=10),
            name='Male-Oriented'
        )
    )

    # Add a scatter trace for female orientation
    fig.add_trace(
        go.Scatter(
            x=female_df.index,
            y=female_df['total_competitors'],
            mode='markers',
            hovertemplate='<b>Discipline:</b> %{x}<br><b>Orientation:</b> Female-Oriented',
            marker=dict(color='pink', symbol='circle', size=10),
            name='Female-Oriented'
        )
    )

    # Update the layout
    fig.update_layout(
        title='Gender Orientation of Disciplines',
        xaxis_title='Discipline',
        yaxis_title='Total Competitors',
        showlegend=True
    )

    # Show the interactive plot
    st.plotly_chart(fig)

