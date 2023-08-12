import plotly.express as px
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import streamlit as st
import plotly.graph_objects as go

def determine_most_participated_sport(df, country):
    """
    Determine the most participated sport for a given country.

    Parameters:
        df (pandas.DataFrame): The DataFrame containing the data.
        country (str): The country for which to determine the most participated sport.

    Returns:
        str: The most participated sport for the given country.
    """
    # Group the DataFrame by 'country_name' and 'discipline_title' and count the occurrences
    country_sport_count = df.groupby(['country_name', 'discipline_title']).size().reset_index(name='participation_count')

    # Pivot the DataFrame to have 'country_name' as the index and 'discipline_title' as the columns
    pivot_df = pd.pivot_table(country_sport_count, index='country_name', columns='discipline_title', values='participation_count', fill_value=0)

    # Determine the most participated sport for the given country
    most_participated_sport = pivot_df.loc[country].idxmax()

    return most_participated_sport

def determine_best_medals_by_discipline(df, country):
    """
    Determine the countries with the best overall medal count in each discipline for a given country.

    Parameters:
        df (pandas.DataFrame): The DataFrame containing the data.
        country (str): The country for which to determine the best overall medal count.

    Returns:
        pandas.DataFrame: A DataFrame showing the countries with the best overall medal count in each discipline.
    """
    # Group the DataFrame by 'country_name', 'discipline_title', and 'medal_type' and count the occurrences
    medal_count = df.groupby(['country_name', 'discipline_title', 'medal_type']).size().reset_index(name='medal_count')

    # Determine the total medal count for each country in each discipline
    total_medals = medal_count.groupby(['country_name', 'discipline_title'])['medal_count'].sum().reset_index()

    # Determine the country with the best overall medal count in each discipline
    best_medals_country = total_medals.groupby('discipline_title')['medal_count'].idxmax()
    country_best_medals_df = total_medals.loc[best_medals_country, ['country_name', 'discipline_title', 'medal_count']]
    country_best_medals_df.sort_values(by='country_name', inplace=True)

    return country_best_medals_df[country_best_medals_df['country_name']==country]

def country_analysis(df,country):
# Assuming df is your DataFrame
    most_participated_sport = determine_most_participated_sport(df, country)
    country_best_medals = determine_best_medals_by_discipline(df, country)

# Calculate the count of participants for the most participated sport
    participants_count = df[df['discipline_title'] == most_participated_sport].groupby('country_name').size().get(country, 0)

    fig = go.Figure()

# Add a bar for the most participated sport
    fig.add_trace(go.Bar(
        x=[most_participated_sport],
        y=[participants_count],
        name='Most Participated Sport',
        marker_color='blue',
        text=[participants_count],
        textposition='auto',
        hovertemplate=f"Discipline: {most_participated_sport}<br>Participants: {participants_count}",
        showlegend=True
    ))

# Add bars for the disciplines with the highest medal count
    for _, row in country_best_medals.iterrows():
        discipline = row['discipline_title']
        medals_count = row['medal_count']
        fig.add_trace(go.Bar(
            x=[discipline],
            y=[medals_count],
            name=f'Highest Medal Count - {discipline}',
            marker_color='green',
            text=[medals_count],
            textposition='auto',
            hovertemplate=f"Discipline: {discipline}<br>Medals: {medals_count}",
            showlegend=True
        ))

# Update the layout
    fig.update_layout(
        title=f"Sports Analysis for {country}",
        xaxis_title='Discipline',
        yaxis_title='Count',
        showlegend=True,
        barmode='group'
    )

# Show the interactive plot
    st.plotly_chart(fig)




def track_country_performance(df, country_name, discipline_title):
    """
    Track the performance of a country for a given discipline across all slug games.

    Parameters:
        df (pandas.DataFrame): The DataFrame containing the data.
        country_name (str): The country name to track performance.
        discipline_title (str): The discipline title to track performance.

    Returns:
        pandas.DataFrame: A DataFrame with the total medals won for the given country and discipline in each slug game.
    """
    # Filter the DataFrame for the specified country and discipline
    filtered_df = df[(df['country_name'] == country_name) & (df['discipline_title'] == discipline_title)]

    # Group the filtered DataFrame by 'slug_game' and calculate the total medals won
    grouped_df = filtered_df.groupby('slug_game')['medal_type'].count().reset_index(name='total_medals')

    return grouped_df


def create_slider_plot(df, country_name, discipline_title):
    """
    Create a Plotly visualization with a slider for tracking the performance of a country in a discipline across slug games.

    Parameters:
        df (pandas.DataFrame): The DataFrame containing the data.
        country_name (str): The country name to track performance.
        discipline_title (str): The discipline title to track performance.
    """
    # Track the performance of the country for the given discipline across all slug games
    performance_df = track_country_performance(df, country_name, discipline_title)

    # Create a figure
    fig = go.Figure()

    # Add an initial bar trace for the first slug game
    fig.add_trace(go.Bar(
        x=[performance_df['slug_game'].values[0]],
        y=[performance_df['total_medals'].values[0]],
        name='Total Medals',
    ))

    # Set the layout
    fig.update_layout(
        title=f'Performance of {country_name} in {discipline_title} as per total medal count',
        xaxis_title='Slug Game',
        yaxis_title='Total Medals',
        barmode='stack',
    )

    # Add a slider
    fig.update_layout(
        sliders=[
            {
                'currentvalue': {'prefix': 'Slug Game: '},
                'steps': [
                    {'method': 'animate', 'args': [[f'frame{i}']] ,'label': f'{game}'} for i, game in enumerate(performance_df['slug_game'])
                ],
                'transition': {'duration': 500, 'easing': 'linear'},
                'x': 0.1, 'len': 0.9,
                'y': 0, 'yanchor': 'top',
                'pad': {'t': 50, 'b': 10},
                'active': 0,
            }
        ],
    )

    # Add frames for each slug game
    frames = []
    for i, slug_game in enumerate(performance_df['slug_game']):
        frame = go.Frame(
            name=f'frame{i}',
            data=[go.Bar(x=[slug_game], y=[performance_df.loc[performance_df['slug_game'] == slug_game, 'total_medals'].values[0]])]
        )
        frames.append(frame)

    fig.frames = frames

    # Show the interactive plot
    st.plotly_chart(fig)

    
#MEDAL COUNT DISTRIBUTION
def track_performance(df, country_name, discipline_title):
    """
    Track the performance of a country for a given discipline across all slug games.

    Parameters:
        df (pandas.DataFrame): The DataFrame containing the data.
        country_name (str): The country name to track performance.
        discipline_title (str): The discipline title to track performance.

    Returns:
        pandas.DataFrame: A DataFrame with the total medals won for the given country and discipline in each slug game.
    """
    # Filter the DataFrame for the specified country and discipline
    filtered_df = df[(df['country_name'] == country_name) & (df['discipline_title'] == discipline_title)]

    # Group the filtered DataFrame by 'slug_game' and calculate the total medals won
    grouped_df = filtered_df.groupby('slug_game')['medal_type'].value_counts().unstack(fill_value=0)

    return grouped_df


def create(df, country_name, discipline_title):
    """
    Create a Plotly visualization with a slider for tracking the performance of a country in a discipline across slug games.

    Parameters:
        df (pandas.DataFrame): The DataFrame containing the data.
        country_name (str): The country name to track performance.
        discipline_title (str): The discipline title to track performance.
    """
    # Track the performance of the country for the given discipline across all slug games
    performance_df = track_performance(df, country_name, discipline_title)

    # Create a figure
    fig = go.Figure()

    # Add bar traces for each medal type
    for medal_type in ['GOLD', 'SILVER', 'BRONZE']:
        fig.add_trace(go.Bar(
            x=performance_df.index,
            y=performance_df[medal_type],
            name=medal_type.capitalize(),
        ))

    # Set the layout
    fig.update_layout(
        title=f'Performance of {country_name} in {discipline_title} as per medal distribution',
        xaxis_title='Slug Game',
        yaxis_title='Total Medals',
        barmode='stack',
    )

    # Add a slider
    fig.update_layout(
        sliders=[
            {
                'currentvalue': {'prefix': 'Slug Game: '},
                'steps': [
                    {'method': 'animate', 'args': [[f'frame{i}']] ,'label': f'{game}'} for i, game in enumerate(performance_df.index)
                ],
                'transition': {'duration': 500, 'easing': 'linear'},
                'x': 0.1, 'len': 0.9,
                'y': 0, 'yanchor': 'top',
                'pad': {'t': 50, 'b': 10},
                'active': 0,
            }
        ],
    )

    # Add frames for each slug game
    frames = []
    for i, slug_game in enumerate(performance_df.index):
        frame_data = [
            go.Bar(x=[slug_game], y=[performance_df.loc[slug_game, 'GOLD']], name='Gold', marker=dict(color='gold')),
            go.Bar(x=[slug_game], y=[performance_df.loc[slug_game, 'SILVER']], name='Silver', marker=dict(color='silver')),
            go.Bar(x=[slug_game], y=[performance_df.loc[slug_game, 'BRONZE']], name='Bronze', marker=dict(color='peru'))
        ]
        frame = go.Frame(
            name=f'frame{i}',
            data=frame_data
        )
        frames.append(frame)

    fig.frames = frames

    # Show the interactive plot
    fig.show()

#COMPARE MEDAL PERFORMANCE BTW 2 COUNTRIES IN SMAE DISCIPLINE

import pandas as pd
import plotly.graph_objects as go

def tr_performance(df, country_name, discipline_title):
    """
    Track the performance of a country for a given discipline across all slug games.

    Parameters:
        df (pandas.DataFrame): The DataFrame containing the data.
        country_name (str): The country name to track performance.
        discipline_title (str): The discipline title to track performance.

    Returns:
        pandas.DataFrame: A DataFrame with the total medals won for the given country and discipline in each slug game.
    """
    # Filter the DataFrame for the specified country and discipline
    filtered_df = df[(df['country_name'] == country_name) & (df['discipline_title'] == discipline_title)]

    # Group the filtered DataFrame by 'slug_game' and calculate the total medals won
    grouped_df = filtered_df.groupby('slug_game')['medal_type'].count().reset_index(name='total_medals')

    return grouped_df


def cr_slider_plot(df, country1_name, country2_name, discipline_title):
    """
    Create a Plotly visualization with a slider for tracking the performance of two countries in a discipline across slug games.

    Parameters:
        df (pandas.DataFrame): The DataFrame containing the data.
        country1_name (str): The name of the first country.
        country2_name (str): The name of the second country.
        discipline_title (str): The discipline title to track performance.
    """
    # Track the performance of the first country for the given discipline across all slug games
    performance_country1 = track_country_performance(df, country1_name, discipline_title)

    # Track the performance of the second country for the given discipline across all slug games
    performance_country2 = track_country_performance(df, country2_name, discipline_title)

    # Merge the performance DataFrames to include all slug games
    performance_combined = performance_country1.merge(performance_country2, on='slug_game', suffixes=('_country1', '_country2'))

    # Create a figure
    fig = go.Figure()

    # Add initial bar traces for the first slug game
    fig.add_trace(go.Bar(
        x=[performance_combined['slug_game'].values[0]],
        y=[performance_combined['total_medals_country1'].values[0]],
        name=country1_name,
        marker_color='blue',
        offsetgroup=0,
    ))
    fig.add_trace(go.Bar(
        x=[performance_combined['slug_game'].values[0]],
        y=[performance_combined['total_medals_country2'].values[0]],
        name=country2_name,
        marker_color='green',
        offsetgroup=1,
    ))

    # Set the layout
    fig.update_layout(
        title=f'Performance of {country1_name} vs {country2_name} in {discipline_title}',
        xaxis_title='Slug Game',
        yaxis_title='Total Medals',
        barmode='group',
    )

    # Add a slider
    fig.update_layout(
        sliders=[
            {
                'currentvalue': {'prefix': 'Slug Game: '},
                'steps': [
                    {'method': 'animate', 'args': [[f'frame{i}']], 'label': game} for i, game in enumerate(performance_combined['slug_game'])
                ],
                'transition': {'duration': 500, 'easing': 'linear'},
                'x': 0.1, 'len': 0.9,
                'y': 0, 'yanchor': 'top',
                'pad': {'t': 50, 'b': 10},
                'active': 0,
            }
        ],
    )

    # Add frames for each slug game
    frames = []
    for i, slug_game in enumerate(performance_combined['slug_game']):
        frame = go.Frame(
            name=f'frame{i}',
            data=[
                go.Bar(x=[slug_game], y=[performance_combined.loc[performance_combined['slug_game'] == slug_game, 'total_medals_country1'].values[0]], name=country1_name, marker_color='blue', offsetgroup=0),
                go.Bar(x=[slug_game], y=[performance_combined.loc[performance_combined['slug_game'] == slug_game, 'total_medals_country2'].values[0]], name=country2_name, marker_color='green', offsetgroup=1),
            ],
        )
        frames.append(frame)

    fig.frames = frames

    # Show the interactive plot
    fig.show()