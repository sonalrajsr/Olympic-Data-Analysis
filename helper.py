import numpy as np
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt


def medal_tally(df, year='All Years', countries='All Countries'):
    medal_df = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    temp_df = medal_df
    check = 0

    if year == 'All Years' and countries == 'All Countries':
        temp_df = medal_df
    elif year == 'All Years' and countries != 'All Countries':
        check = 1
        temp_df = medal_df[medal_df['region'] == countries]
    elif year != "All Years" and countries == 'All Countries':
        temp_df = medal_df[medal_df['Year'] == year]
    elif year != 'All Year' and countries != 'All Countries':
        temp_df = medal_df[(medal_df['Year'] == year) & (medal_df['region'] == countries)] 
    
    
    if check == 1:
        temp_df = temp_df.groupby('Year').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Year', ascending=False).reset_index()
    else:
        temp_df = temp_df.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold', ascending=False).reset_index()
        
    temp_df['Total Medals'] = temp_df['Gold'] + temp_df['Silver'] + temp_df['Bronze']
    return temp_df
 
def country_year_list(df):
    all_countries = np.unique(df['region'].dropna().values).tolist()
    all_countries.sort()
    all_countries.insert(0, 'All Countries')

    all_years = df['Year'].unique().tolist()
    all_years.sort()
    all_years.insert(0, 'All Years')

    return all_countries, all_years


def countries_performance(df, country='USA'):
    perf_cun_df = df[df['region'] == country]
    perf_cun_df = perf_cun_df.groupby('Year').count()['Medal'].reset_index().sort_values('Year')
    return perf_cun_df

def country_heatmap(df, country):
    perf_cun_df = df[df['region'] == country]
    pivot_table = perf_cun_df.pivot_table(index='Sport', columns='Year', values='Medal', aggfunc='count').fillna(0)
    return pivot_table

def get_best_player(df, county):
    perf_cun_df = df[df['region'] == county]
    best_player = perf_cun_df.groupby('Name').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold', ascending=False).reset_index().head(10)
    return best_player