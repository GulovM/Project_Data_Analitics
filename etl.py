import pandas as pd
from connector import create_connection

def extract_data():
    """
    Функция для извлечения данных из базы данных.
    Извлекает данные из представлений athlete_medals, country_medal_tally, yearly_medal_count и top_athletes.
    """
    conn = create_connection()  # Создание подключения к базе данных
    athlete_medals = pd.read_sql_query('select * from athlete_medals', conn)
    country_medal_tally = pd.read_sql_query('select * from country_medal_tally', conn)
    yearly_medal_count = pd.read_sql_query('select * from yearly_medal_count', conn)
    top_athletes = pd.read_sql_query('select * from top_athletes', conn)
    conn.close()
    return athlete_medals, country_medal_tally, yearly_medal_count, top_athletes

def transform_data(athlete_medals, country_medal_tally, yearly_medal_count, top_athletes):
    """
    Функция для трансформации данных.
    Преобразует столбец born в athlete_medals в формат даты и столбец year в yearly_medal_count в формат года.
    """
    athlete_medals['born'] = pd.to_datetime(athlete_medals['born'], errors='coerce').dt.date  # Преобразование столбца born в формат даты
    yearly_medal_count['year'] = pd.to_datetime(yearly_medal_count['year'], format='%Y').dt.year  # Преобразование столбца year в формат года
    return athlete_medals, country_medal_tally, yearly_medal_count, top_athletes

if __name__ == "__main__":
    """
    Основной блок программы для извлечения и трансформации данных.
    Извлекает данные из базы данных, трансформирует их и выводит первые несколько строк каждого набора данных.
    """
    athlete_medals, country_medal_tally, yearly_medal_count, top_athletes = extract_data()  # Извлечение данных
    athlete_medals, country_medal_tally, yearly_medal_count, top_athletes = transform_data(athlete_medals, country_medal_tally, yearly_medal_count, top_athletes)  # Трансформация данных
    print(athlete_medals.head())
    print(country_medal_tally.head())
    print(yearly_medal_count.head())
    print(top_athletes.head())
