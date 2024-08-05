import pandas as pd
import duckdb
from connector import create_connection

def create_tables():
    conn = duckdb.connect('my.db')
    with open('queries/create_tables.sql', 'r') as f:
        conn.execute(f.read())
    conn.close()

def create_views():
    conn = duckdb.connect('my.db')
    with open('queries/create_views.sql', 'r') as f:
        conn.execute(f.read())
    conn.close()
    
def load_data():
    conn = create_connection()
    # Загрузка данных из excel файлов
    olympic_athlete_bio_df = pd.read_excel('source/Olympic_Athlete_Bio.xlsx')
    olympic_athlete_event_results_df = pd.read_excel('source/Olympic_Athlete_Event_Results.xlsx')
    olympic_games_medal_tally_df = pd.read_excel('source/Olympic_Games_Medal_Tally.xlsx')
    olympics_country_df = pd.read_excel('source/Olympics_Country.xlsx')
    olympics_games_df = pd.read_excel('source/Olympics_Games.xlsx')

    # Заполнение таблиц данными
    conn.execute("INSERT INTO olympics_country (noc, country) SELECT noc, country FROM olympics_country_df")
    conn.execute("INSERT INTO olympic_athlete_bio (athlete_id, name, sex, born, height, weight, country, country_noc) SELECT athlete_id, name, sex, born, height, weight, country, country_noc FROM olympic_athlete_bio_df")
    conn.execute("INSERT INTO olympics_games (edition, edition_id, year, city, country_noc, start_date, end_date, competition_date, isHeld) SELECT edition, edition_id, year, city, country_noc, start_date, end_date, competition_date, isHeld FROM olympics_games_df")
    conn.execute("INSERT INTO olympic_athlete_event_results (edition, edition_id, country_noc, sport, event, result_id, athlete, athlete_id, pos, medal, isTeamSport) SELECT edition, edition_id, country_noc, sport, event, result_id, athlete, athlete_id, pos, medal, isTeamSport FROM olympic_athlete_event_results_df")
    conn.execute("INSERT INTO olympic_games_medal_tally (edition, edition_id, year, country, country_noc, gold, silver, bronze, total) SELECT edition, edition_id, year, country, country_noc, gold, silver, bronze, total FROM olympic_games_medal_tally_df")

    conn.close()


if __name__ == "__main__":
    create_tables()
    load_data()
    create_views()
