import pandas as pd
from connector import create_connection

def extract_data():
    conn = create_connection()
    athlete_medals = pd.read_sql_query('select * from athlete_medals', conn)
    country_medal_tally = pd.read_sql_query('select * from country_medal_tally', conn)
    yearly_medal_count = pd.read_sql_query('select * from yearly_medal_count', conn)
    top_athletes = pd.read_sql_query('select * from top_athletes', conn)
    conn.close()
    return athlete_medals, country_medal_tally, yearly_medal_count, top_athletes

def transform_data(athlete_medals, country_medal_tally, yearly_medal_count, top_athletes):
    athlete_medals['born'] = pd.to_datetime(athlete_medals['born'], errors='coerce')
    yearly_medal_count['year'] = pd.to_datetime(yearly_medal_count['year'], format='%Y')
    return athlete_medals, country_medal_tally, yearly_medal_count, top_athletes

if __name__ == "__main__":
    athlete_medals, country_medal_tally, yearly_medal_count, top_athletes = extract_data()
    athlete_medals, country_medal_tally, yearly_medal_count, top_athletes = transform_data(athlete_medals, country_medal_tally, yearly_medal_count, top_athletes)
    print(athlete_medals.head())
    print(country_medal_tally.head())
    print(yearly_medal_count.head())
    print(top_athletes.head())
