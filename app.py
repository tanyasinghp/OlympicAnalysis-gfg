import streamlit as st
import pandas as pd
import geo as ge
import country_analysis as ca
import event_analysis as ea
import medal_analysis as ma
import player_analysis as pa
import about as abt
import Dataset_prep as dap
from streamlit.components.v1 import html

df = dap.dset()


# Hide Default streamlit functions
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """

st.markdown(hide_st_style, unsafe_allow_html = True)

#title
st.title('Olympics Data Analysis')

#sidebar with options
with st.sidebar:
    add_radio = st.radio(
        "Olympic Analysis", 
        ("About-page","Event Analysis", "Medal Analysis", "Player Analysis", "Country Analysis", "Geospatial Analysis", "Dataset")
    )

#About Section
if add_radio == "About-page":
    abt.render_html_file()

    
#event analysis page
if add_radio == "Event Analysis":
    st.subheader("Event Analysis")
    balanced_orientation_df,male_orientation_df,female_orientation_df = ea.analyze_gender_orientation(df)
    ea.plot_gender_orientation(balanced_orientation_df, male_orientation_df, female_orientation_df)

#medal analysis page
if add_radio == "Medal Analysis":
    st.subheader("Medal Analysis")
    medal_radio = st.radio(
        "What type of analysis would you like to perform?", 
        ("Single Country", "Two Country")
    )
    if medal_radio == 'Single Country':
        country_name = st.text_input("Enter the country of Interest:")
        discipline_title = st.text_input("Enter the discipline:")
        if st.button("Analyse Medals"):
            ma.create_slider_plot(df, country_name, discipline_title)

    if medal_radio == 'Two Country':
        country1_name = st.text_input("Enter the first country: ")
        country2_name = st.text_input("Enter the second country: ")
        discipline_title = st.text_input("Enter the discipline title: ")
        if st.button("Perform analysis"):
            ma.compare_plot(df, country1_name, country2_name, discipline_title)

#player analysys page
if add_radio == "Player Analysis":
    st.subheader("Player Analysis")
    player_radio = st.radio(
        "What type of analysis would you like to perform?", 
        ("Single Player", "Multi Player")
    )
    if player_radio == 'Single Player':
        name = st.text_input("Enter player name: ")
        if st.button("Analyse player"):
            pa.create_medal_count_plot(name,df)
    
    if player_radio == 'Multi Player':
        athlete1 = st.text_input("Enter the name of the first athlete: ").strip()
        athlete2 = st.text_input("Enter the name of the second athlete: ").strip()
        if st.button('Compare Players'):
            pa.medal_compare(athlete1, df)
            pa.medal_compare(athlete2, df)

#contry analysys page
if add_radio == "Country Analysis":
    st.subheader("Country Analysis")
    country_radio = st.radio(
        "What type of analysis would you like to perform?", 
        ("Performance", "Total Medal count","Individual Medal count")
    )

    if country_radio == 'Performance':
        st.subheader('Country analysis of performance')
        country = st.text_input("Enter the Country to be considered:")  # Specify the country of interest
        if st.button('Analyse performance'):
            ca.country_analysis(df,country)

    if country_radio == 'Total Medal count':
        st.subheader('Country analysis based on medal count')
        col1,col2 = st.columns(2)
        with col1:
            country_name = st.text_input("Enter the country of Interest:")
        with col2:
            discipline_title = st.text_input("Enter the discipline:")

        if st.button('Analyse medal count'):
            ca.create_slider_plot(df, country_name, discipline_title)
    
    if country_radio == 'Individual Medal count':
        st.subheader('Country analysis based on Individual medals')
        col1,col2 = st.columns(2)
        with col1:
            country_name = st.text_input("Enter the country of Interest:")
        with col2:
            discipline_title = st.text_input("Enter the discipline:")

        if st.button('Analyse medal count'):
            ca.create(df, country_name, discipline_title)


#geospatial analysis page
if add_radio == "Geospatial Analysis":
    geo_radio = st.radio(
        "What Visualization are you looking for?", 
        ("Total Medals","Individual Medals","Top Disciplines")
    )
    if geo_radio=='Total Medals':
        st.subheader("Geospatial Analysis of Total Medal Count")
        ge.geo(df)
    
    if geo_radio=='Individual Medals':
        st.subheader("Geospatial Analysis of Individual Medal Count")
        ge.create_choropleth_map(df)
        
    if geo_radio=='Top Disciplines':
        st.subheader("Geospatial Analysis of Top Disciplines")
        ge.geo_dis(df)

#dataset display page
if add_radio == "Dataset":
    data_radio = st.radio(
        "What Data are you looking for?", 
        ("Entire Data Set","Discipline Wise","Country Wise","Participant wise")
    )
    if data_radio=='Entire Data Set':
        st.subheader('Complete Dataset:')
        if st.button('GENERATE'):
            df=dap.dset()
            st.dataframe(df)
    
    if data_radio=='Discipline Wise':
        st.subheader('Discipline wise:')
        Discipline_name = st.text_input("Enter the Discipline of Interest:")
        if st.button('GENERATE'):
            df=dap.dset()
            st.dataframe(df[df['discipline_title']==Discipline_name])

    if data_radio=='Country Wise':
        st.subheader('Country wise:')
        country = st.text_input("Enter the Country of Interest:")
        if st.button('GENERATE'):
            df=dap.dset()
            st.dataframe(df[df['country_name']==country])
            
    if data_radio=='Participant wise':
        st.subheader('Participant wise:')
        player = st.text_input("Enter the player of Interest:")
        if st.button('GENERATE'):
            df=dap.dset()
            st.dataframe(df[df['athlete_full_name']==player])
    
    