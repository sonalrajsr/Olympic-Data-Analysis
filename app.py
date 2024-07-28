import streamlit as st
import pandas as pd
import preprocessor, helper
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff
import scipy

df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')

df = preprocessor.preprocess(df, region_df)

st.title("Olympics Data Analysis")
st.logo("8baf0a4c95c8ba2e591448b1f000617a.jpg")

st.sidebar.title('Olympics Analysis')
user_menu = st.sidebar.radio(
    'Selection an Option',
    ('Medal Tally', 'Overall Analysis', 'Country-Wise', 'Athlete Wise')
)

if user_menu == 'Medal Tally':
    st.header("Total Medals Wons by Countries:")

    countries, years = helper.country_year_list(df=df)
    selected_year = st.sidebar.selectbox("Year", years)
    selected_country = st.sidebar.selectbox("Country", countries)
    medal_table = helper.medal_tally(df=df, year=selected_year, countries=selected_country)
    st.subheader(f"Performance of {selected_country} in year {selected_year}", divider="green")
    st.table(medal_table)


if user_menu == 'Overall Analysis':

    editions = df['Year'].unique().shape[0] - 1
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]

    st.title("Overall Stats of Olympics")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.header("Total Editions")
        st.subheader(editions)

    with col2:
        st.header("Total Cities")
        st.subheader(cities)

    with col3:
        st.header("Total Sports")
        st.subheader(sports)
    col1, col2, col3 = st.columns(3)

    with col1:
        st.header("Total Events")
        st.subheader(events)

    with col2:
        st.header("Total Athletes")
        st.subheader(athletes)

    with col3:
        st.header("Total Nations")
        st.subheader(nations)
    year_df_countries = df.drop_duplicates(subset=['Year', 'region'])['Year'].value_counts().reset_index().sort_values('Year')
    year_df_countries.rename(columns={'Year': 'Olympic Years', 'count': 'Total Countries Participated'}, inplace=True)
    st.subheader("Graph of total countries parcipated in different years")
    st.line_chart(year_df_countries, x="Olympic Years", y="Total Countries Participated", x_label="Olympic Years", y_label='Total Countries Participated')
    
    year_df_events = df.drop_duplicates(subset=['Year', 'Event'])['Year'].value_counts().reset_index().sort_values('Year')
    year_df_events.rename(columns={'Year': 'Olympic Years', 'count': 'Total Games Played'}, inplace=True)
    st.subheader("Graph of total Games played in different years")
    st.line_chart(year_df_events, x="Olympic Years", y="Total Games Played", x_label="Olympic Years", y_label='Total Games')

if user_menu == 'Country-Wise':
    countries, years = helper.country_year_list(df=df)
    selected_country = st.sidebar.selectbox("Country", countries)
    country_df = df.dropna(subset=['Medal'])
    country_df = country_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    performance_count = helper.countries_performance(country_df, selected_country)
    st.subheader(f"Total medal won by {selected_country} in different years")
    st.table(performance_count)
    st.subheader(f"Graph of total Medels won by {selected_country} in different years")
    st.line_chart(performance_count, x="Year", y="Medal", x_label="Olympic Years", y_label='Total Medels')

    #Plotting heatmap
    st.subheader(f"Performance of {selected_country} in different Sports")
    pt = helper.country_heatmap(country_df, selected_country)
    fig, ax = plt.subplots(figsize=(20, 20))
    if not pt.empty:
        ax = sns.heatmap(pt, annot=True)
        st.pyplot(fig)

    st.subheader(f"Top 10 Players of {selected_country}")
    best_player = helper.get_best_player(country_df, selected_country)
    st.table(best_player)

if user_menu == "Athlete Wise":
    age_df = df.drop_duplicates(subset=['Name', 'Games', 'Event', 'Team'])
    age = age_df['Age'].dropna()
    gold = age_df[age_df['Medal'] == 'Gold']['Age'].dropna()
    silver = age_df[age_df['Medal'] == 'Silver']['Age'].dropna()
    bronze = age_df[age_df['Medal'] == 'Bronze']['Age'].dropna()
    fig = ff.create_distplot([age, gold, silver, bronze], ['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'], show_hist=False, show_rug=False)
    st.subheader("Distribution of Age for different sports")
    st.plotly_chart(fig)



